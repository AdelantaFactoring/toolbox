"""
⚙️ Fondo Crecer Engine V2

Motor especializado para procesamiento de datos de Fondo Crecer
"""

import pandas as pd

try:
    from ..core.base_engine import BaseEngine
except ImportError:
    raise ImportError(
        "No se pudieron importar las dependencias de Fondo Crecer Engine V2"
    )


class FondoCrecerEngine(BaseEngine):
    """Motor especializado para Fondo Crecer heredando BaseEngine"""

    def __init__(self):
        super().__init__()

    def obtener_resumen_fondo_crecer(self, df: pd.DataFrame) -> None:
        """
        Obtiene resumen específico de datos de Fondo Crecer

        Args:
            df: DataFrame con datos de Fondo Crecer
        """
        print("\n🎯 Resumen Fondo Crecer:")
        self.obtener_resumen(df)
