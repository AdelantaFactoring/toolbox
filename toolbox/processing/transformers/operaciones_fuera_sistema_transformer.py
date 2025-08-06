"""
🔄 OperacionesFueraSistema Transformer V2 - Procesamiento especializado

Transformer dedicado para lógica de transformación de datos de OperacionesFueraSistema
"""

import pandas as pd
from typing import List, Dict, Any

try:
    from ...core.base_transformer import BaseTransformer
    from ...config.settings import V2Settings
except ImportError:
    raise ImportError(
        "OperacionesFueraSistema Transformer V2 requiere BaseTransformer y V2Settings de imports relativos"
    )

logger = V2Settings.logger


class OperacionesFueraSistemaTransformer(BaseTransformer):
    """Transformer especializado para OperacionesFueraSistema"""

    def __init__(self):
        super().__init__()

        # Mapeo de columnas específico para OperacionesFueraSistema
        self.column_mapping = {
            "Liquidación": "CodigoLiquidacion",
            "N° Factura/ Letra": "NroDocumento",
            "Nombre Cliente": "RazonSocialCliente",
            "RUC Cliente": "RUCCliente",
            "Nombre Deudor": "RazonSocialPagador",
            "RUC DEUDOR": "RUCPagador",
            "TNM Op": "TasaNominalMensualPorc",
            "TNA Op": "",  # No hay una columna directamente correspondiente
            "% Finan": "FinanciamientoPorc",
            "Fecha de Op": "FechaOperacion",
            "F.Pago Confirmada": "FechaConfirmado",
            "Días Efect": "DiasEfectivo",
            "Moneda": "Moneda",
            "Neto Confirmado": "NetoConfirmado",
            "% Estructuracion": "",  # No hay una columna directamente correspondiente
            "Comisión de Estructuracion": "MontoComisionEstructuracion",
            "IGV Comisión": "ComisionEstructuracionIGV",
            "Comision Con IGV": "ComisionEstructuracionConIGV",
            "Fondo Resguardo": "FondoResguardo",
            "Neto a Financiar": "MontoCobrar",
            "Interés sin IGV": "Interes",
            "IGV Interés": "",  # No hay una columna directamente correspondiente
            "Interés con IGV": "InteresConIGV",
            "Contrato": "GastosContrato",
            "Servicio de custodia sin IGV": "ServicioCustodia",
            "Servicio de cobranza de documentos sin IGV": "ServicioCobranza",
            "Comisión por envío de carta notarial sin IGV": "GastoVigenciaPoder",
            "Gastos Diversos Sin IGV": "GastosDiversosSinIGV",
            "IGV Gastos Diversos": "GastosDiversosIGV",
            "Gastos Diversos con IGV": "GastosDiversosConIGV",
            "Total a ser facturado al desembolso Inc. IGV": "MontoTotalFacturado",
            "N Factura generada": "FacturasGeneradas",
            "Desembolso Neto": "MontoDesembolso",
            "Fecha de pago": "FechaPago",
            "Estado": "Estado",
            "Dias Mora": "DiasMora",
            "TNM Moratorio": "",  # No hay una columna directamente correspondiente
            "TNA Moratorio": "",  # No hay una columna directamente correspondiente
            "Interes Mora - No Afecto IGV": "InteresPago",
            "Factura Int Mora": "",  # No hay una columna directamente correspondiente
            "Gastos Mora Con IGV": "GastosPago",
            "Factura Gastos Mora Con IGV": "",  # No hay una columna directamente correspondiente
            "Importe a Pagar": "MontoCobrarPago",
            "Import. Recaudado": "MontoPago",
            "Excedente Generado a ser devuelto": "ExcesoPago",
            "Fecha de devolución de excedente": "FechaDesembolso",
            "Total factura Mora": "",  # No hay una columna directamente correspondiente
            "EJECUTIVO": "Ejecutivo",
            "TIPO DE OPERACIÓN": "TipoOperacion",
        }

    def renombrar_columnas_operaciones(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Renombra columnas según mapping específico de OperacionesFueraSistema
        Elimina columnas vacías
        """
        logger("Renombrando columnas OperacionesFueraSistema")
        df_renamed = self.renombrar_columnas(df, self.column_mapping, normalize=False)
        logger(f"Columnas renombradas: {list(df_renamed.columns)}")
        # Eliminar columnas vacías (que tienen key "")
        if "" in df_renamed.columns:
            df_renamed = df_renamed.drop(columns=[""])
        return df_renamed

    def combinar_datos_pen_usd(
        self, data_pen: List[Dict[str, Any]], data_usd: List[Dict[str, Any]]
    ) -> pd.DataFrame:
        """
        Combina datos de PEN y USD en un solo DataFrame
        """
        logger(f"Combinando datos: {len(data_pen)} PEN + {len(data_usd)} USD")

        df_pen = self.convertir_a_dataframe(data_pen)
        df_usd = self.convertir_a_dataframe(data_usd)

        # Combinar DataFrames
        df_combined = pd.concat([df_pen, df_usd], ignore_index=True)

        logger(f"Datos combinados: {len(df_combined)} registros totales")
        return df_combined

    def limpiar_datos_operaciones(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpia datos: elimina registros con RUC vacíos
        """
        logger = V2Settings.logger
        logger(f"Limpiando datos: {len(df)} registros iniciales")
        logger(f"Columnas disponibles: {list(df.columns)}")

        # Verificar que las columnas críticas existan
        if "RUCCliente" not in df.columns or "RUCPagador" not in df.columns:
            logger(
                f"❌ Columnas críticas faltantes. Columnas actuales: {list(df.columns)}"
            )
            # Devolver DataFrame vacío si no hay columnas críticas
            return pd.DataFrame()

        # Filtrar filas donde RUCCliente o RUCPagador sean NaN o cadenas vacías
        df = df.dropna(subset=["RUCCliente", "RUCPagador"])
        df = df[
            (df["RUCCliente"].astype(str).str.strip() != "")
            & (df["RUCPagador"].astype(str).str.strip() != "")
        ]

        logger(f"Datos limpiados: {len(df)} registros válidos")
        return df
