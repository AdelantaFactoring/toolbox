"""
✅ Sector Pagadores Validator V2 - Validación de datos

Validator especializado para validación de datos de Sector Pagadores
"""

from typing import List, Dict, Any, Union
import pandas as pd


try:
    from ...core.base_validator import BaseValidator
    from ...schemas.sector_pagadores_schema import SectorPagadoresSchema
except ImportError:
    raise ImportError(
        "SectorPagadoresValidator V2 requiere BaseValidator y SectorPagadoresSchema de imports relativos"
    )


class SectorPagadoresValidator(BaseValidator):
    def __init__(self):
        super().__init__(schema_class=SectorPagadoresSchema)

    def validar_schema_sector_pagadores(
        self, raw_data: Union[List[Dict[str, Any]], pd.DataFrame]
    ) -> List[Dict[str, Any]]:
        return self.validar_schema(raw_data)
