"""
🌐 Fondo Promocional API V2 - Interfaz pública independiente
"""

import pandas as pd
from typing import List, Dict, Any, Union

try:
    from ..config.settings import V2Settings
    from ..io.fondo_promocional_client import (
        FondoPromocionalClient,
    )
    from ..processing.transformers.fondo_promocional_transformer import (
        FondoPromocionalTransformer,
    )
    from ..processing.validators.fondo_promocional_validator import (
        FondoPromocionalValidator,
    )
    from ..engines.fondo_promocional_engine import FondoPromocionalEngine
except ImportError:
    # Retornar error si no se pueden importar las dependencias de Fondo Promocional API V2
    raise ImportError(
        "No se pudieron importar las dependencias de Fondo Promocional API V2"
    )

logger = V2Settings.logger


class FondoPromocionalAPI:
    """API pública para FondoPromocional V2 independiente"""

    def __init__(self):
        self._client = FondoPromocionalClient()
        self._transformer = FondoPromocionalTransformer()
        self._validator = FondoPromocionalValidator()
        self._engine = FondoPromocionalEngine()

    def get_fondo_promocional(
        self, as_df: bool = False
    ) -> Union[pd.DataFrame, List[Dict[str, Any]]]:
        """
        Obtiene datos de FondoPromocional procesados

        Args:
            as_df: Si True retorna DataFrame, si False retorna lista de diccionarios

        Returns:
            DataFrame o lista con datos de fondo promocional
        """
        logger("Iniciando obtención de datos FondoPromocional V2")

        # 1) Obtener datos crudos de cliente
        raw_data = self._client.fetch_fondo_promocional_data()

        # 2) Convertir a DataFrame
        df = self._transformer.convertir_a_dataframe(raw_data)

        # 3) Validar columnas esperadas
        self._validator.validar_columnas_fondo_promocional(df)

        # 4) Validar schema con Pydantic
        df = self._transformer.renombrar_columnas_fondo_promocional(df)

        # 5) Validar DataFrame final
        df = self._transformer.eliminar_duplicados_por_columna_fondo_promocional(df)

        # 6) Validar schema con Pydantic
        raw_data_validated = self._validator.validar_schema_fondo_promocional(df)

        # 7) Retornar según formato solicitado
        if as_df:
            return self._transformer.convertir_a_dataframe(raw_data_validated)
        return raw_data_validated


# Instancia global para API simple
fondo_promocional_api = FondoPromocionalAPI()


# Funciones de conveniencia para API simple
def get_fondo_promocional(
    as_df: bool = False,
) -> Union[pd.DataFrame, List[Dict[str, Any]]]:
    """Función de conveniencia: af.fondo_promocional.get_fondo_promocional()"""
    return fondo_promocional_api.get_fondo_promocional(as_df)
