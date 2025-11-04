"""
⚙️ Referidos Engine V2

Motor especializado para procesamiento de datos de Referidos
"""

import pandas as pd

try:
    from ..core.base_engine import BaseEngine
except ImportError:
    raise ImportError("No se pudieron importar las dependencias de Referidos Engine V2")


class ReferidosEngine(BaseEngine):
    """Motor especializado para Referidos heredando BaseEngine"""

    def __init__(self):
        super().__init__()

    def obtener_resumen_referidos(self, df: pd.DataFrame) -> None:
        """
        Obtiene resumen específico de datos de Referidos

        Args:
            df: DataFrame con datos de Referidos
        """

        self.obtener_resumen(df)
