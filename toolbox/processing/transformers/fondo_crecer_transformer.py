"""
🔄 FondoCrecer Transformer V2 - Procesamiento especializado

Transformer dedicado para lógica de negocio de FondoCrecer con parseo de garantías
"""

import pandas as pd

# from typing import List, Dict, Any
# from config.logger import logger

try:
    from ...core.base_transformer import BaseTransformer
except ImportError:
    raise ImportError(
        "FondoCrecer Transformer V2 requiere BaseTransformer de imports relativos"
    )


class FondoCrecerTransformer(BaseTransformer):
    """Transformer especializado para FondoCrecer"""

    def __init__(self):

        self.column_mapping = {
            "liquidacion": "CodigoLiquidacion",
            "garantia": "Garantia",
        }

    def renombrar_columnas_fondo_crecer(self, df: pd.DataFrame) -> pd.DataFrame:
        """Renombra columnas según mapping de FondoCrecer"""
        return self.renombrar_columnas(df, self.column_mapping)

    def formatear_fecha_mes_fondo_crecer(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Formatea la columna 'Mes' a tipo fecha con formato específico
        """
        return self.formatear_fecha_mes(df, columna="%d/%m/%Y")

    def eliminar_duplicados_por_columna_fondo_crecer(
        self, df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Elimina duplicados por columna 'CodigoLiquidacion'
        Mantiene el último registro encontrado
        """
        return self.eliminar_duplicados_por_columna(
            df, columna="CodigoLiquidacion", keep="last"
        )
