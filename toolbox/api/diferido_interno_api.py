"""
🌐 API V2 - Diferido Interno
INTERFAZ IDÉNTICA A V1
"""

import pandas as pd
from datetime import datetime

try:
    from ..engines.diferido_interno_engine import DiferidoInternoEngine

    # No hay client real para diferido interno (placeholder)
    from ..processing.transformers.diferido_interno_transformer import (
        DiferidoInternoTransformer,
    )
    from ..processing.validators.diferido_interno_validator import (
        DiferidoInternoValidator,
    )
except ImportError:
    raise ImportError(
        "DiferidoInternoAPI V2 requiere dependencias de imports relativos"
    )


class DiferidoInternoAPI:
    """Wrapper que mantiene interfaz exacta de V1"""

    def __init__(self, df: pd.DataFrame):
        """Constructor IDÉNTICO a V1"""
        self.df = df  # cargar el DataFrame desde un archivo Excel o CSV
        self._engine = DiferidoInternoEngine()
        # No hay client real para diferido interno (placeholder)
        self._transformer = DiferidoInternoTransformer()
        self._validator = DiferidoInternoValidator()

    def calcular_monto_por_mes(self, row, mes_inicio, mes_fin):
        """Método IDÉNTICO a V1"""
        return self._engine.calcular_monto_por_mes(row, mes_inicio, mes_fin)

    def last_day_of_month(self, date: datetime):
        """Método IDÉNTICO a V1"""
        return self._engine.last_day_of_month(date)

    def put_dates_in_columns(
        self,
        df: pd.DataFrame,
        fecha_min: datetime,
        fecha_max: datetime,
    ) -> pd.DataFrame:
        """Método IDÉNTICO a V1"""
        return self._engine.put_dates_in_columns(df, fecha_min, fecha_max)

    def calcular_diferido_interno(self, hasta: str) -> pd.DataFrame:
        """Método IDÉNTICO a V1"""
        return self._engine.calcular_diferido_interno(self.df, hasta)

    def obtener_resumen(self) -> pd.DataFrame:
        """Método IDÉNTICO a V1"""
        return self._engine.obtener_resumen(self.df)
