"""
✅ Referidos Validator V2 - Simplificado con BaseValidator

Validador especializado para Referidos usando BaseValidator simplificado
"""

from typing import List, Dict, Any, Union
import pandas as pd

# Importaciones V2 con imports relativos únicamente
try:
    from ...core.base_validator import BaseValidator
    from ...schemas.referidos_schema import ReferidosSchema
    from ...config.settings import V2Settings
except ImportError:
    raise ImportError(
        "No se pudieron importar las dependencias de Referidos Validator V2"
    )

# Logger desde V2Settings
logger = V2Settings.logger


class ReferidosValidator(BaseValidator):
    """Validador especializado para Referidos heredando BaseValidator"""

    # Columnas esperadas para Referidos
    _cols_esperadas = ["REFERENCIA", "LIQUIDACIÓN", "EJECUTIVO", "MES"]

    def __init__(self):
        # Inicializar BaseValidator con schema específico
        super().__init__(schema_class=ReferidosSchema)

    def validar_columnas_referidos(self, df: pd.DataFrame) -> None:
        """
        Validación específica de columnas para Referidos
        """
        self.validar_columnas(df, self._cols_esperadas)

    def validar_schema_referidos(
        self, raw_data: Union[List[Dict[str, Any]], pd.DataFrame]
    ) -> List[Dict[str, Any]]:
        """
        Validación todo o nada con schema Referidos
        """
        logger(f"Iniciando validación schema Referidos: {len(raw_data)} registros")

        # Usar método base que ya implementa "todo o nada"
        validated_data = self.validar_schema(raw_data)

        logger(
            f"Validación schema Referidos completada: {len(validated_data)} registros válidos"
        )
        return validated_data
