"""
⚙️ Fondo Promocional Engine V2

Motor especializado para procesamiento de datos de Fondo Promocional
"""

import pandas as pd

try:
    from ..core.base_engine import BaseEngine
except ImportError:
    raise ImportError(
        "No se pudieron importar las dependencias de Fondo Promocional Engine V2"
    )


class FondoPromocionalEngine(BaseEngine):
    """Motor especializado para FondoPromocional heredando BaseEngine"""

    def __init__(self):
        super().__init__()

    def obtener_resumen_fondo_promocional(self, df: pd.DataFrame) -> None:
        """
        Obtiene resumen específico de datos de Fondo Promocional

        Args:
            df: DataFrame con datos de Fondo Promocional
        """

        self.obtener_resumen(df)
