"""
✅ OperacionesFueraSistema Validator V2 - Validación especializada

Validator especializado para OperacionesFueraSistema usando BaseValidator
"""

from typing import List, Dict, Any, Union
import pandas as pd

try:
    from ...core.base_validator import BaseValidator
    from ...schemas.operaciones_fuera_sistema_schema import (
        OperacionesFueraSistemaSchema,
    )
    from ...config.settings import V2Settings
except ImportError:
    raise ImportError(
        "No se pudieron importar las dependencias de OperacionesFueraSistema Validator V2"
    )

logger = V2Settings.logger


class OperacionesFueraSistemaValidator(BaseValidator):
    """Validator especializado para OperacionesFueraSistema heredando BaseValidator"""

    # Columnas esperadas para OperacionesFueraSistema
    _cols_esperadas = [
        "CodigoLiquidacion",
        "NroDocumento",
        "RazonSocialCliente",
        "RUCCliente",
        "RazonSocialPagador",
        "RUCPagador",
        "DiasEfectivo",
        "Moneda",
        "MontoCobrar",
    ]

    def __init__(self):
        # Inicializar BaseValidator con schema específico
        super().__init__(schema_class=OperacionesFueraSistemaSchema)

    def validar_columnas_operaciones(self, df: pd.DataFrame) -> None:
        """
        Validación específica de columnas para OperacionesFueraSistema
        """
        self.validar_columnas(df, self._cols_esperadas)

    def validar_schema_operaciones(
        self, raw_data: Union[List[Dict[str, Any]], pd.DataFrame]
    ) -> List[Dict[str, Any]]:
        """
        Validación todo o nada con schema OperacionesFueraSistema
        """
        logger(
            f"Iniciando validación schema OperacionesFueraSistema: {len(raw_data)} registros"
        )

        # Usar método base que ya implementa "todo o nada"
        validated_data = self.validar_schema(raw_data)

        logger(
            f"Validación schema OperacionesFueraSistema completada: {len(validated_data)} registros válidos"
        )
        return validated_data
