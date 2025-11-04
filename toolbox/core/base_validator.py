"""
Base Validator V2 - Validador base simplificado

Validador base con solo 2 métodos esenciales para V2
"""

import pandas as pd
import unicodedata
from typing import List, Dict, Any, Union

try:
    from .base import Base
except ImportError:
    raise ImportError("V2 base_validator requires Base from relative core")


class BaseValidator(Base):
    """
    Validador base V2 simplificado
    Hereda el decorador timeit de Base

    Solo 2 métodos esenciales:
    - validar_columnas: Validación de columnas de DataFrame
    - validar_schema: Validación todo o nada con Pydantic
    """

    def __init__(self, schema_class=None):
        """
        Inicializa el validador base

        Args:
            schema_class: Clase de schema Pydantic para validación (opcional)
        """
        super().__init__()
        self.schema_class = schema_class

    def _normalize(self, text: str) -> str:
        """
        Normaliza texto eliminando diacríticos y convirtiendo a minúsculas
        Migrado exacto desde BaseCalcular V1
        """
        nf = unicodedata.normalize("NFD", text)
        return "".join(c for c in nf if unicodedata.category(c) != "Mn").lower()

    def validar_columnas(self, df: pd.DataFrame, expected: List[str]) -> None:
        """
        Valida que DataFrame tenga todas las columnas requeridas
        Migrado exacto desde BaseCalcular V1
        """
        present = {self._normalize(c) for c in df.columns}
        faltan = [col for col in expected if self._normalize(col) not in present]
        if faltan:
            raise ValueError(f"Faltan columnas requeridas: {faltan}")

    def validar_schema(
        self, raw_data: Union[List[Dict[str, Any]], pd.DataFrame]
    ) -> List[Dict[str, Any]]:
        """
        Validación todo o nada con Pydantic schema

        Args:
            raw_data: Lista de diccionarios o DataFrame a validar

        Returns:
            Lista de registros válidos (todos o error)
        """
        if not self.schema_class:
            raise ValueError("Schema class no está configurado")

        # Convertir DataFrame a List[Dict] si es necesario
        if isinstance(raw_data, pd.DataFrame):
            raw_data = raw_data.to_dict("records")

        try:
            # TODO O NADA - si uno falla, todo falla
            validated_data = [
                self.schema_class(**item).model_dump() for item in raw_data
            ]
            return validated_data
        except Exception as e:
            raise ValueError(f"Validación schema falló: {str(e)}")
