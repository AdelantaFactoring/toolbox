"""
🌐 Referidos API V2 - Interfaz pública independiente
"""

import pandas as pd
from typing import List, Dict, Any, Union

try:
    from ..config.settings import V2Settings
    from ..io.referidos_client import (
        ReferidosClient,
    )
    from ..processing.transformers.referidos_transformer import (
        ReferidosTransformer,
    )
    from ..processing.validators.referidos_validator import (
        ReferidosValidator,
    )
    from ..engines.referidos_engine import ReferidosEngine
except ImportError:
    # Retornar error si no se pueden importar las dependencias de Referidos API V2
    raise ImportError("No se pudieron importar las dependencias de Referidos API V2")


logger = V2Settings.logger


class ReferidosAPI:
    """API pública para Referidos V2 independiente"""

    def __init__(self):
        self._client = ReferidosClient()
        self._transformer = ReferidosTransformer()
        self._validator = ReferidosValidator()
        self._engine = ReferidosEngine()

    def get_referidos(
        self, as_df: bool = False
    ) -> Union[pd.DataFrame, List[Dict[str, Any]]]:
        """
        Obtiene datos de Referidos procesados

        Args:
            as_df: Si True retorna DataFrame, si False retorna lista de diccionarios

        Returns:
            DataFrame o lista con datos de referidos
        """
        logger("Iniciando obtención de datos Referidos V2")

        # 1) Obtener datos crudos de cliente
        raw_data = self._client.fetch_referidos_data()

        # 2) Convertir a DataFrame
        df = self._transformer.convertir_a_dataframe(raw_data)

        # 3) Validar columnas esperadas
        self._validator.validar_columnas_referidos(df)

        # 4) Validar schema con Pydantic
        df = self._transformer.renombrar_columnas_referidos(df)

        # 5) Validar DataFrame final
        df = self._transformer.eliminar_duplicados_por_columna_referidos(df)

        # 6) Validar schema con Pydantic
        raw_data_validated = self._validator.validar_schema_referidos(df)

        # 7) Retornar según formato solicitado
        if as_df:
            return self._transformer.convertir_a_dataframe(raw_data_validated)
        return raw_data_validated


# Instancia global para API simple
referidos_api = ReferidosAPI()


# Funciones de conveniencia para API simple
def get_referidos(as_df: bool = False) -> Union[pd.DataFrame, List[Dict[str, Any]]]:
    """Función de conveniencia: af.referidos.get_referidos()"""
    return referidos_api.get_referidos(as_df)
