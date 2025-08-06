"""
✅ KPI Validator V2 - Validación especializada

Validador especializado para KPI con lógica de negocio específica
"""

from typing import List, Dict, Any, Union
import pandas as pd

try:
    from ...core.base_validator import BaseValidator
    from ...schemas.kpi_schema import KPICalcularSchema, KPIAcumuladoCalcularSchema
    from ...config.settings import V2Settings
except ImportError:
    raise ImportError("KPIValidator requiere dependencias base")

logger = V2Settings.logger


class KPIValidator(BaseValidator):
    """Validador especializado para KPI con selección de schema"""

    def __init__(self):
        # Inicializar con schema por defecto
        super().__init__(schema_class=KPICalcularSchema)

    def validar_columnas_minimas(self, df: pd.DataFrame) -> pd.DataFrame:
        """Asegura que existan las columnas mínimas esperadas para KPI"""
        required = [
            "Ejecutivo",
            "FechaOperacion",
            "NetoConfirmado",
            "Moneda",
            "MontoDesembolso",
            "DiasEfectivo",
            "ComisionEstructuracionConIGV",
            "Interes",
            "GastosDiversosConIGV",
            "RUCCliente",
            "RUCPagador",
            "RazonSocialPagador",
            "CodigoLiquidacion",
            "NroDocumento",
        ]
        missing = set(required) - set(df.columns)
        if missing:
            msg = f"Faltan columnas obligatorias: {missing}"
            logger(msg)
            raise ValueError(msg)
        return df

    def validar_columnas_kpi(self, df: pd.DataFrame, tipo_reporte: int = 2) -> None:
        """
        Validación específica de columnas para KPI según tipo de reporte
        """
        if tipo_reporte == 0:
            # Columnas para reporte acumulado
            cols_esperadas = [
                "CodigoLiquidacion",
                "RUCCliente",
                "RazonSocialCliente",
                "RUCPagador",
                "RazonSocialPagador",
                "Moneda",
                "TipoOperacion",
                "Estado",
                "NroDocumento",
                "FechaOperacion",
                "NetoConfirmado",
                "MontoDesembolso",
                "Ejecutivo",
                "FechaInteresConfirming",
                "TipoOperacionDetalle",
                "FechaPago",
                "FechaPagoCreacion",
                "FechaPagoModificacion",
                "DiasMora",
                "MontoCobrarPago",
            ]
        else:
            # Columnas para reporte normal
            cols_esperadas = [
                "CodigoLiquidacion",
                "RUCCliente",
                "RazonSocialCliente",
                "RUCPagador",
                "RazonSocialPagador",
                "Moneda",
                "TipoOperacion",
                "Estado",
                "NroDocumento",
                "FechaOperacion",
                "NetoConfirmado",
                "MontoDesembolso",
                "Ejecutivo",
                "DiasEfectivo",
                "ComisionEstructuracionConIGV",
                "Interes",
                "GastosDiversosConIGV",
            ]

        self.validar_columnas(df, cols_esperadas)

    def validar_schema_kpi(
        self, raw_data: Union[List[Dict[str, Any]], pd.DataFrame], tipo_reporte: int = 2
    ) -> List[Dict[str, Any]]:
        """
        Validación todo o nada con schema KPI apropiado según tipo_reporte
        """
        logger(
            f"Iniciando validación schema KPI tipo_reporte={tipo_reporte}: {len(raw_data)} registros"
        )

        # Seleccionar schema según tipo de reporte
        if tipo_reporte == 0:
            schema_class = KPIAcumuladoCalcularSchema
            logger("Usando KPIAcumuladoCalcularSchema para validación")
        else:
            schema_class = KPICalcularSchema
            logger("Usando KPICalcularSchema para validación")

        # Cambiar temporalmente el schema según tipo_reporte
        schema_original = self.schema_class
        self.schema_class = schema_class

        try:
            # Usar método base que implementa "todo o nada"
            validated_data = self.validar_schema(raw_data)
            logger(
                f"Validación schema KPI completada exitosamente: {len(validated_data)} registros válidos"
            )
            return validated_data
        finally:
            # Restaurar schema original
            self.schema_class = schema_original

    def validar_integridad_kpi(self, df: pd.DataFrame) -> bool:
        """
        Validaciones de integridad específicas para datos KPI
        """
        try:
            # Validar que no haya duplicados por CodigoLiquidacion
            if df["CodigoLiquidacion"].duplicated().any():
                duplicados = df[df["CodigoLiquidacion"].duplicated(keep=False)]
                logger(f"ADVERTENCIA: Encontrados {len(duplicados)} códigos duplicados")

            # Validar fechas coherentes
            if "FechaOperacion" in df.columns and "FechaConfirmado" in df.columns:
                fechas_invalidas = df[
                    (df["FechaConfirmado"].notna())
                    & (df["FechaOperacion"] > df["FechaConfirmado"])
                ]
                if not fechas_invalidas.empty:
                    logger(
                        f"ADVERTENCIA: {len(fechas_invalidas)} registros con FechaOperacion > FechaConfirmado"
                    )

            # Validar montos coherentes
            if "NetoConfirmado" in df.columns and "MontoDesembolso" in df.columns:
                montos_invalidos = df[
                    (df["NetoConfirmado"] > 0)
                    & (df["MontoDesembolso"] > df["NetoConfirmado"] * 1.1)
                ]
                if not montos_invalidos.empty:
                    logger(
                        f"ADVERTENCIA: {len(montos_invalidos)} registros con MontoDesembolso > NetoConfirmado*1.1"
                    )

            # Validar monedas válidas
            if "Moneda" in df.columns:
                monedas_validas = {"PEN", "USD"}
                monedas_invalidas = df[~df["Moneda"].isin(monedas_validas)]
                if not monedas_invalidas.empty:
                    logger(
                        f"ERROR: {len(monedas_invalidas)} registros con moneda inválida"
                    )
                    return False

            logger("Validación de integridad KPI completada exitosamente")
            return True

        except Exception as e:
            logger(f"Error en validación de integridad KPI: {str(e)}")
            return False

    def validar_campos_obligatorios_kpi(
        self, df: pd.DataFrame, tipo_reporte: int = 2
    ) -> bool:
        """
        Valida que los campos obligatorios estén presentes y no sean nulos
        """
        campos_base_obligatorios = [
            "CodigoLiquidacion",
            "RUCCliente",
            "RUCPagador",
            "Moneda",
            "FechaOperacion",
            "NetoConfirmado",
            "Ejecutivo",
        ]

        if tipo_reporte == 0:
            # Campos adicionales para reporte acumulado
            campos_obligatorios = campos_base_obligatorios + ["Estado", "TipoOperacion"]
        else:
            # Campos adicionales para reporte normal
            campos_obligatorios = campos_base_obligatorios + [
                "MontoDesembolso",
                "DiasEfectivo",
            ]

        for campo in campos_obligatorios:
            if campo not in df.columns:
                logger(f"ERROR: Campo obligatorio ausente: {campo}")
                return False

            if df[campo].isna().all():
                logger(f"ERROR: Campo obligatorio completamente nulo: {campo}")
                return False

            valores_nulos = df[campo].isna().sum()
            if valores_nulos > 0:
                logger(
                    f"ADVERTENCIA: Campo {campo} tiene {valores_nulos} valores nulos"
                )

        logger("Validación de campos obligatorios KPI completada")
        return True
