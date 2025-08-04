"""
✅ FondoPromocional Validator V2 - Simplificado con BaseValidator

Validador especializado para FondoPromocional usando BaseValidator simplificado
"""

from typing import List, Dict, Any, Union
import pandas as pd

# Importaciones V2 con imports relativos únicamente
try:
    from ...core.base_validator import BaseValidator
    from ...schemas.fondo_promocional_schema import FondoPromocionalSchema
    from ...config.settings import V2Settings
except ImportError:
    raise ImportError(
        "No se pudieron importar las dependencias de FondoPromocional Validator V2"
    )

# Logger desde V2Settings
logger = V2Settings.logger


class FondoPromocionalValidator(BaseValidator):
    """Validador especializado para FondoPromocional heredando BaseValidator"""

    # Columnas esperadas para FondoPromocional
    _cols_esperadas = ["LIQUIDACION"]

    def __init__(self):
        # Inicializar BaseValidator con schema específico
        super().__init__(schema_class=FondoPromocionalSchema)

    def validar_columnas_fondo_promocional(self, df: pd.DataFrame) -> None:
        """
        Validación específica de columnas para FondoPromocional
        """
        self.validar_columnas(df, self._cols_esperadas)

    def validar_schema_fondo_promocional(
        self, raw_data: Union[List[Dict[str, Any]], pd.DataFrame]
    ) -> List[Dict[str, Any]]:
        """
        Validación todo o nada con schema FondoPromocional
        """
        logger(
            f"Iniciando validación schema FondoPromocional: {len(raw_data)} registros"
        )

        # Usar método base que ya implementa "todo o nada"
        validated_data = self.validar_schema(raw_data)

        logger(
            f"Validación schema FondoPromocional completada: {len(validated_data)} registros válidos"
        )
        return validated_data
