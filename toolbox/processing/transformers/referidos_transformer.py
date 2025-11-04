"""
🔄 Referidos Transformer V2 - Procesamiento especializado

Transformer dedicado para lógica de negocio de Referidos
"""

import pandas as pd

try:
    from ...core.base_transformer import BaseTransformer
except ImportError:
    raise ImportError(
        "Referidos Transformer V2 requiere BaseTransformer de imports relativos"
    )


class ReferidosTransformer(BaseTransformer):
    """Transformer especializado para Referidos"""

    def __init__(self):

        self.column_mapping = {
            "referencia": "Referencia",
            "liquidacion": "CodigoLiquidacion",
            "ejecutivo": "Ejecutivo",
            "mes": "Mes",
        }

    def renombrar_columnas_referidos(self, df: pd.DataFrame) -> pd.DataFrame:
        """Renombra columnas según mapping de Referidos"""
        return self.renombrar_columnas(df, self.column_mapping)

    def formatear_fecha_mes_referidos(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Formatea la columna 'Mes' a tipo fecha con formato específico
        """
        return self.formatear_fecha_mes(df, columna="%d/%m/%Y")

    def eliminar_duplicados_por_columna_referidos(
        self, df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Elimina duplicados por columna 'CodigoLiquidacion'
        Mantiene el último registro encontrado
        """
        return self.eliminar_duplicados_por_columna(
            df, columna="CodigoLiquidacion", keep="last"
        )
