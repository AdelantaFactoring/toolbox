import pandas as pd
from typing import List, Dict, Any, Union

try:
    from ..engines.operaciones_fuera_sistema_engine import OperacionesFueraSistemaEngine
    from ..io.operaciones_fuera_sistema_client import OperacionesFueraSistemaClient
    from ..processing.transformers.operaciones_fuera_sistema_transformer import (
        OperacionesFueraSistemaTransformer,
    )
    from ..processing.validators.operaciones_fuera_sistema_validator import (
        OperacionesFueraSistemaValidator,
    )
except ImportError as e:
    raise ImportError(
        f"OperacionesFueraSistemaAPI V2 requiere dependencias de imports relativos: {e}"
    )


class OperacionesFueraSistemaAPI:

    def __init__(self):
        # Componentes de arquitectura hexagonal
        self._engine = OperacionesFueraSistemaEngine()
        self._client = OperacionesFueraSistemaClient()
        self._transformer = OperacionesFueraSistemaTransformer()
        self._validator = OperacionesFueraSistemaValidator()

    def get_operaciones_fuera_sistema(
        self, as_df: bool = False
    ) -> Union[pd.DataFrame, List[Dict[str, Any]]]:
        """
        Obtiene datos de OperacionesFueraSistema procesados

        Args:
            as_df: Si True retorna DataFrame, si False retorna lista de diccionarios

        Returns:
            DataFrame o lista con datos de OperacionesFueraSistema
        """
        # 1) Obtener datos crudos de cliente (PEN y USD)
        raw_data_pen = self._client.fetch_operaciones_fuera_sistema_pen_data()
        raw_data_usd = self._client.fetch_operaciones_fuera_sistema_usd_data()

        # 2) Combinar datos PEN y USD
        df_combined = self._transformer.combinar_datos_pen_usd(
            raw_data_pen, raw_data_usd
        )

        # 3) Renombrar columnas para consistencia
        df_combined = self._transformer.renombrar_columnas_operaciones(df_combined)

        # 4) Limpiar datos (eliminar registros con RUC vacíos)
        df_cleaned = self._transformer.limpiar_datos_operaciones(df_combined)

        # 5) Validar schema con Pydantic (todo o nada)
        validated_data = self._validator.validar_schema_operaciones(df_cleaned)

        if as_df:
            return pd.DataFrame(validated_data)

        return validated_data


operaciones_fuera_sistema_api = OperacionesFueraSistemaAPI()


def get_operaciones_fuera_sistema(
    as_df: bool = False,
) -> Union[pd.DataFrame, List[Dict[str, Any]]]:
    return operaciones_fuera_sistema_api.get_operaciones_fuera_sistema(as_df=as_df)
