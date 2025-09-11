"""
🌐 Fondo Crecer API V2 - Interfaz pública independiente
"""

import pandas as pd
from typing import List, Dict, Any, Union

try:
    from ..config.settings import V2Settings
    from ..io.fondo_crecer_client import (
        FondoCrecerClient,
    )
    from ..processing.transformers.fondo_crecer_transformer import (
        FondoCrecerTransformer,
    )
    from ..processing.validators.fondo_crecer_validator import (
        FondoCrecerValidator,
    )
    from ..engines.fondo_crecer_engine import FondoCrecerEngine
except ImportError:
    # Retornar error si no se pueden importar las dependencias de Fondo Crecer API V2
    raise ImportError("No se pudieron importar las dependencias de Fondo Crecer API V2")


logger = V2Settings.logger


class FondoCrecerAPI:
    """API pública para FondoCrecer V2 independiente"""

    def __init__(self):
        self._client = FondoCrecerClient()
        self._transformer = FondoCrecerTransformer()
        self._validator = FondoCrecerValidator()
        self._engine = FondoCrecerEngine()

    def get_fondo_crecer(
        self, as_df: bool = False
    ) -> Union[pd.DataFrame, List[Dict[str, Any]]]:
        """
        Obtiene datos de FondoCrecer procesados

        Args:
            as_df: Si True retorna DataFrame, si False retorna lista de diccionarios

        Returns:
            DataFrame o lista con datos de fondo crecer
        """
        logger("Iniciando obtención de datos FondoCrecer V2")

        # 1) Obtener datos crudos de cliente
        raw_data = self._client.fetch_fondo_crecer_data()

        # 2) Convertir a DataFrame
        df = self._transformer.convertir_a_dataframe(raw_data)

        # 3) Validar columnas esperadas
        self._validator.validar_columnas_fondo_crecer(df)

        # 4) Validar schema con Pydantic
        df = self._transformer.renombrar_columnas_fondo_crecer(df)

        # 5) Validar DataFrame final
        df = self._transformer.eliminar_duplicados_por_columna_fondo_crecer(df)

        # 6) Validar schema con Pydantic
        raw_data_validated = self._validator.validar_schema_fondo_crecer(df)

        # 7) Retornar según formato solicitado
        if as_df:
            return self._transformer.convertir_a_dataframe(raw_data_validated)
        return raw_data_validated


# Instancia global para API simple
fondo_crecer_api = FondoCrecerAPI()


# Funciones de conveniencia para API simple
def get_fondo_crecer(as_df: bool = False) -> Union[pd.DataFrame, List[Dict[str, Any]]]:
    """Función de conveniencia: af.fondo_crecer.get_fondo_crecer()"""
    return fondo_crecer_api.get_fondo_crecer(as_df)
