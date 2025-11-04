"""
⚙️ Sector Pagadores Engine V2
ORQUESTADOR que utiliza transformer y validator siguiendo arquitectura hexagonal
"""

import pandas as pd

try:
    from ..core.base_engine import BaseEngine
    from ..processing.transformers.sector_pagadores_transformer import (
        SectorPagadoresTransformer,
    )
    from ..processing.validators.sector_pagadores_validator import (
        SectorPagadoresValidator,
    )
except ImportError:
    raise ImportError(
        "SectorPagadoresEngine V2 requiere BaseEngine, transformer y validator de imports relativos"
    )


class SectorPagadoresEngine(BaseEngine):
    """Motor que orquesta la lógica usando transformer y validator"""

    def __init__(self):
        super().__init__()
        self._transformer = SectorPagadoresTransformer()
        self._validator = SectorPagadoresValidator()

    def calcular(self, data: dict) -> list[dict]:
        """LÓGICA PRINCIPAL usando componentes hexagonales"""
        # Usar transformer para procesar
        datos_procesados = self._transformer.procesar_datos(data)
        # Usar validator para validar
        datos_validados = self._validator.validar_datos(datos_procesados)
        return datos_validados

    def calcular_df(self, data: dict) -> pd.DataFrame:
        """COPIADO EXACTO DE V1"""
        return pd.DataFrame(self.calcular(data))
