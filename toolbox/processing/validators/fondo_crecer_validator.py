"""
✅ FondoCrecer Validator V2 - Simplificado con BaseValidator

Validador especializado para FondoCrecer usando BaseValidator simplificado
"""

from typing import List, Dict, Any, Union
import pandas as pd

# Importaciones V2 con imports relativos únicamente
try:
    from ...core.base_validator import BaseValidator
    from ...schemas.fondo_crecer_schema import FondoCrecerSchema
    from ...config.settings import V2Settings
except ImportError:
    raise ImportError(
        "No se pudieron importar las dependencias de FondoCrecer Validator V2"
    )

# Logger desde V2Settings
logger = V2Settings.logger


class FondoCrecerValidator(BaseValidator):
    """Validador especializado para FondoCrecer heredando BaseValidator"""

    # Columnas esperadas para FondoCrecer (originales de la fuente, como V1)
    _cols_esperadas = ["LIQUIDACION", "GARANTIA"]

    def __init__(self):
        # Inicializar BaseValidator con schema específico
        super().__init__(schema_class=FondoCrecerSchema)

    def validar_columnas_fondo_crecer(self, df: pd.DataFrame) -> None:
        """
        Validación específica de columnas para FondoCrecer
        """
        self.validar_columnas(df, self._cols_esperadas)

    def validar_schema_fondo_crecer(
        self, raw_data: Union[List[Dict[str, Any]], pd.DataFrame]
    ) -> List[Dict[str, Any]]:
        """
        Validación todo o nada con schema FondoCrecer
        """
        logger(f"Iniciando validación schema FondoCrecer: {len(raw_data)} registros")

        # Usar método base que ya implementa "todo o nada"
        validated_data = self.validar_schema(raw_data)

        logger(
            f"Validación schema FondoCrecer completada: {len(validated_data)} registros válidos"
        )
        return validated_data
