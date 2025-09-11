import pandas as pd

try:
    from .base import Base
    from ..config.settings import V2Settings
except ImportError:
    raise ImportError("V2 base_engine requires Base from relative core")

logger = V2Settings.logger


class BaseEngine(Base):
    """Clase base para motores de transformación V2"""

    def __init__(self):
        super().__init__()

    def obtener_resumen(self, df: pd.DataFrame) -> None:
        """
        Obtiene resumen de información del DataFrame usando df.info()

        Args:
            df: DataFrame para obtener resumen
        """
        if df is not None and not df.empty:
            logger(f"\n📊 Resumen del DataFrame:{df.info}")

        else:
            logger("⚠️ DataFrame vacío o None")
