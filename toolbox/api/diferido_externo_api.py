"""
🌐 API V2 - Diferido Externo
INTERFAZ IDÉNTICA A V1
"""

import pandas as pd
from datetime import datetime
from io import BytesIO

try:
    from ..engines.diferido_externo_engine import DiferidoExternoEngine

    # No hay client real para diferido externo (placeholder)
    from ..processing.transformers.diferido_externo_transformer import (
        DiferidoExternoTransformer,
    )
    from ..processing.validators.diferido_externo_validator import (
        DiferidoExternoValidator,
    )
except ImportError:
    raise ImportError(
        "DiferidoExternoAPI V2 requiere dependencias de imports relativos"
    )


class DiferidoExternoAPI:
    """Wrapper que mantiene interfaz exacta de V1"""

    def __init__(self, file_path: str | BytesIO):
        """Constructor IDÉNTICO a V1"""
        self.file_path = file_path
        self._engine = DiferidoExternoEngine()
        # No hay client real para diferido externo (placeholder)
        self._transformer = DiferidoExternoTransformer()
        self._validator = DiferidoExternoValidator()

    def read_excel_file(self, sheet_name: str, usecols: str, date_col: str):
        """Método IDÉNTICO a V1"""
        return self._engine.read_excel_file(
            self.file_path, sheet_name, usecols, date_col
        )

    def last_day_of_month(self, date: datetime) -> datetime:
        """Método IDÉNTICO a V1"""
        return self._engine.last_day_of_month(date)

    def auto_get_usecols(
        self, sheet_name: str, fixed_range: tuple[str, str], stop_marker: str
    ) -> tuple[str, list[str]]:
        """Método IDÉNTICO a V1"""
        return self._engine.auto_get_usecols(
            self.file_path, sheet_name, fixed_range, stop_marker
        )

    def process_excel_files(
        self,
        pen_end_date: str = "2025-07-31",
        usd_end_date: str = "2025-12-31",
        read_type: str | None = None,
    ):
        """Método IDÉNTICO a V1"""
        return self._engine.process_excel_files(
            self.file_path, pen_end_date, usd_end_date, read_type
        )

    def replace_columns_with_dates(self, df: pd.DataFrame):
        """Método IDÉNTICO a V1"""
        return self._engine.replace_columns_with_dates(df)

    def calcular_diferido_externo(self, hasta: str) -> pd.DataFrame:
        """Método IDÉNTICO a V1"""
        return self._engine.calcular_diferido_externo(self.file_path, hasta)


# Alias para compatibilidad con v1
DiferidoExternoCalcular = DiferidoExternoAPI
