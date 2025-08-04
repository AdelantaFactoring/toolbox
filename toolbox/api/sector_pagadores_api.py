"""
🌐 API V2 - Sector Pagadores
INTERFAZ IDÉNTICA A V1
"""

import pandas as pd

try:
    from ..engines.sector_pagadores_engine import SectorPagadoresEngine
    from ..io.sector_pagadores_client import SectorPagadoresClient
    from ..processing.transformers.sector_pagadores_transformer import (
        SectorPagadoresTransformer,
    )
    from ..processing.validators.sector_pagadores_validator import (
        SectorPagadoresValidator,
    )
except ImportError:
    raise ImportError(
        "SectorPagadoresAPI V2 requiere dependencias de imports relativos"
    )


class SectorPagadoresAPI:
    """Wrapper que mantiene interfaz exacta de V1"""

    def __init__(self):
        """Constructor IDÉNTICO a V1"""
        self._engine = SectorPagadoresEngine()
        self._client = SectorPagadoresClient()
        self._transformer = SectorPagadoresTransformer()
        self._validator = SectorPagadoresValidator()

    def get_sectores_pagadores(self, as_df: bool = False) -> pd.DataFrame:
        """
        Obtiene datos de Sector Pagadores procesados

        Args:
            as_df: Si True retorna DataFrame, si False retorna lista de diccionarios

        Returns:
            DataFrame con datos de sector pagadores
        """
        # 1) Obtener datos crudos de cliente
        raw_data = self._client.fetch_sector_pagadores_data()

        # 2) Convertir a DataFrame
        df = self._transformer.convertir_a_dataframe(raw_data)

        # 3) Validar columnas esperadas
        self._transformer.procesar_datos_sector_pagadores(df)

        # 4) Validar schema con Pydantic
        self._validator.validar_schema_sector_pagadores(df)

        if as_df:
            return df
        else:
            return df.to_dict(orient="records")
