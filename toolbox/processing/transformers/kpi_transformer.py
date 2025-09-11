"""
🔄 KPI Transformer V2 - Transformaciones especializadas

Transformer dedicado para lógica de transformación de datos KPI
"""

import pandas as pd
import numpy as np
import math
from typing import Dict, List
from rapidfuzz import fuzz, process

try:
    from ...core.base_transformer import BaseTransformer
    from ...config.settings import V2Settings
except ImportError:
    raise ImportError("KPITransformer requiere BaseTransformer y V2Settings")

logger = V2Settings.logger


class KPITransformer(BaseTransformer):
    """Transformer especializado para KPI con lógica financiera"""

    def __init__(self):
        super().__init__()

    @property
    def INTERESES_PEN(self) -> float:
        """Tasa de interés PEN (lazy loading)"""
        return V2Settings.get_intereses_pen()

    @property
    def INTERESES_USD(self) -> float:
        """Tasa de interés USD (lazy loading)"""
        return V2Settings.get_intereses_usd()

    def fusionar_operaciones_fuera_sistema(
        self, df_main: pd.DataFrame, df_fuera: pd.DataFrame, tipo_reporte: int = 2
    ) -> pd.DataFrame:
        """
        Fusiona datos principales con operaciones fuera del sistema,
        eliminando duplicados y priorizando datos externos
        """
        # Preparar datasets
        df_main = df_main.assign(FueraSistema="no")
        df_fuera = df_fuera.assign(FueraSistema="si")

        # Convertir fechas según el tipo de reporte
        date_cols = ["FechaOperacion", "FechaConfirmado", "FechaDesembolso"]

        # Para tipo_reporte = 2, el nuevo endpoint devuelve fechas en formato ISO (2025-01-02)
        if tipo_reporte == 2:
            df_main = self._convertir_fechas(
                df_main, date_cols, None
            )  # Formato ISO automático
            df_fuera = self._convertir_fechas(df_fuera, date_cols, None)
        else:
            # Formato legacy para otros tipos de reporte
            df_main = self._convertir_fechas(df_main, date_cols, "%d/%m/%Y")
            df_fuera = self._convertir_fechas(df_fuera, date_cols, None)

        # Limpiar y preparar datos fuera del sistema
        df_fuera = df_fuera.replace({"CodigoLiquidacion": {"": np.nan}}).dropna(
            subset=["CodigoLiquidacion"]
        )
        df_fuera[["GastosDiversosConIGV", "MontoPago"]] = (
            df_fuera[["GastosDiversosConIGV", "MontoPago"]]
            .apply(pd.to_numeric, errors="coerce")
            .fillna(0)
        )

        # Eliminar duplicados priorizando fuera del sistema
        codigos_dentro = set(df_main["CodigoLiquidacion"].dropna().astype(str))
        codigos_fuera = set(df_fuera["CodigoLiquidacion"].dropna().astype(str))
        codigos_duplicados = codigos_dentro.intersection(codigos_fuera)

        if len(codigos_duplicados) > 0:
            logger(
                f"Eliminando {len(codigos_duplicados)} códigos duplicados del dataset interno"
            )
            df_main = df_main[
                ~df_main["CodigoLiquidacion"].astype(str).isin(codigos_duplicados)
            ]

        # Mapear ejecutivos con fuzzy matching
        mapping = self._mapear_ejecutivos(df_main, df_fuera)
        df_fuera["Ejecutivo"] = df_fuera["Ejecutivo"].map(mapping)

        return pd.concat([df_main, df_fuera], ignore_index=True, sort=False)

    def formatear_campos(self, df: pd.DataFrame) -> pd.DataFrame:
        """Formatea campos según requerimientos del negocio KPI"""
        df = df.copy()

        # Formatear fechas
        columnas_fecha = ["FechaOperacion", "FechaConfirmado", "FechaDesembolso"]
        for col in columnas_fecha:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")
                if df[col].dt.tz is not None:
                    df[col] = df[col].dt.tz_localize(None)
                df[col] = df[col].dt.normalize()

        # Limpiar strings y códigos
        df["RUCCliente"] = df["RUCCliente"].astype(str).str.strip()
        df["RUCPagador"] = (
            df["RUCPagador"].astype(str).str.replace("[: ]", "", regex=True).str.strip()
        )
        df["CodigoLiquidacion"] = (
            df["CodigoLiquidacion"]
            .astype(str)
            .str.strip()
            .str.split("-")
            .str[:2]
            .str.join("-")
        )
        df["NroDocumento"] = (
            df["NroDocumento"].astype(str).str.replace(r"\s+", "", regex=True)
        )

        # Convertir tasas
        df["TasaNominalMensualPorc"] = pd.to_numeric(
            df["TasaNominalMensualPorc"], errors="coerce"
        ).fillna(0)
        df["TasaNominalMensualPorc"] = df["TasaNominalMensualPorc"].apply(
            lambda x: x / 100 if x >= 1 else x
        )

        # Crear campos temporales
        if "FechaOperacion" in df.columns and not df["FechaOperacion"].isna().all():
            df["Mes"] = df["FechaOperacion"].dt.strftime("%Y-%m")
            df["Año"] = df["FechaOperacion"].dt.year.astype(str)
            df["MesAño"] = df["FechaOperacion"].dt.strftime("%B-%Y")

        return df

    def calcular_kpis_financieros(
        self, df: pd.DataFrame, tipo_cambio_df: pd.DataFrame, sector_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Calcula métricas financieras, ingresos, costos y utilidades"""
        df = df.copy()

        # Convertir columnas numéricas
        columnas_numericas = [
            "NetoConfirmado",
            "MontoDesembolso",
            "MontoPago",
            "ComisionEstructuracionConIGV",
            "Interes",
            "GastosDiversosConIGV",
            "DiasEfectivo",
            "TipoCambioVenta",
        ]
        for col in columnas_numericas:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        # Preparar tipo de cambio
        tipo_cambio_df_temp = tipo_cambio_df.copy()
        if "TipoCambioFecha" in tipo_cambio_df_temp.columns:
            tipo_cambio_df_temp["TipoCambioFecha"] = pd.to_datetime(
                tipo_cambio_df_temp["TipoCambioFecha"], errors="coerce"
            )

        for col in ["TipoCambioVenta", "TipoCambioCompra"]:
            if col in tipo_cambio_df_temp.columns:
                tipo_cambio_df_temp[col] = pd.to_numeric(
                    tipo_cambio_df_temp[col], errors="coerce"
                ).fillna(1)

        # Merge con tipo de cambio y sector
        df = df.merge(
            tipo_cambio_df_temp,
            left_on="FechaOperacion",
            right_on="TipoCambioFecha",
            how="left",
        )
        df = df.merge(sector_df, on="RUCPagador", how="left")
        df["GrupoEco"] = df["GrupoEco"].fillna(df["RazonSocialPagador"])

        # Conversiones USD → PEN
        factor = np.where(df["Moneda"] == "USD", df["TipoCambioVenta"], 1)
        df["ColocacionSoles"] = df["NetoConfirmado"] * factor
        df["MontoDesembolsoSoles"] = df["MontoDesembolso"] * factor
        df["MontoPagoSoles"] = df["MontoPago"] * factor

        # Calcular ingresos
        df["Ingresos"] = (
            df["ComisionEstructuracionConIGV"] / 1.18
            + df["Interes"]
            + df["GastosDiversosConIGV"] / 1.18
        )
        df["IngresosSoles"] = df["Ingresos"] * factor

        # Calcular costos de fondeo
        cost_rate = np.where(
            df["Moneda"] == "PEN", self.INTERESES_PEN, self.INTERESES_USD
        )
        df["CostosFondo"] = ((1 + cost_rate) ** (df["DiasEfectivo"] / 365) - 1) * df[
            "MontoDesembolso"
        ]
        df["CostosFondoSoles"] = df["CostosFondo"] * factor

        # Totales y utilidad
        df["TotalIngresos"] = df["ComisionEstructuracionConIGV"] / 1.18 + df["Interes"]
        df["TotalIngresosSoles"] = df["TotalIngresos"] * factor
        df["Utilidad"] = df["TotalIngresosSoles"] - df["CostosFondoSoles"]

        # Calcular semana del mes
        if "FechaOperacion" in df.columns and not df["FechaOperacion"].isna().all():
            df["MesSemana"] = (
                df["FechaOperacion"]
                .apply(self._calcular_semana_mes)
                .apply(lambda w: f"Semana {w}")
            )
        else:
            df["MesSemana"] = "Semana 1"

        return df

    def _convertir_fechas(
        self, df: pd.DataFrame, columns: List[str], fmt: str = None
    ) -> pd.DataFrame:
        """Convierte columnas a datetime con formato específico"""
        for col in columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], format=fmt, errors="coerce")
                df[col] = df[col].dt.tz_localize(None)
                df[col] = df[col].dt.normalize()
        return df

    def _mapear_ejecutivos(
        self, df_in: pd.DataFrame, df_out: pd.DataFrame, threshold: int = 75
    ) -> Dict[str, str]:
        """
        Mapea nombres de ejecutivos usando fuzzy matching

        CORREGIDO: Ahora mantiene los nombres originales de df_out cuando no hay match suficiente
        en lugar de transformarlos incorrectamente
        """
        nombres_in = df_in["Ejecutivo"].str.lower().tolist()
        mapping = {}

        for name_out in df_out["Ejecutivo"].unique():
            name_out_lower = name_out.lower()
            best = process.extractOne(
                name_out_lower, nombres_in, scorer=fuzz.partial_ratio
            )

            if best and best[1] >= threshold:
                # Encontrar el nombre original que corresponde al match
                idx_matched = nombres_in.index(best[0])
                matched_original = df_in.iloc[idx_matched]["Ejecutivo"]
                mapping[name_out] = matched_original
                logger(
                    f"Mapeo ejecutivo: '{name_out}' -> '{matched_original}' (score: {best[1]})"
                )
            else:
                # CORREGIDO: Mantener el nombre original en lugar de hacer .title()
                mapping[name_out] = name_out
                logger(
                    f"Sin mapeo suficiente para '{name_out}' (mejor score: {best[1] if best else 0}), manteniendo original"
                )

        return mapping

    @staticmethod
    def _calcular_semana_mes(dt) -> int:
        """Calcula número de semana dentro del mes"""
        if pd.isna(dt) or dt is None:
            return 1

        if isinstance(dt, str):
            try:
                dt = pd.to_datetime(dt)
            except (ValueError, TypeError, pd.errors.ParserError):
                return 1

        try:
            first = dt.replace(day=1)
            dom = dt.day + first.weekday()
            return math.ceil(dom / 7)
        except (AttributeError, ValueError, TypeError):
            return 1
