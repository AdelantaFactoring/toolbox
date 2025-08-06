"""
🔄 Base Transformer V2 - Funcionalidad común migrada desde BaseCalcular
Solo contiene los métodos esenciales solicitados
"""

import pandas as pd
import unicodedata
from datetime import datetime, date
from typing import Union, Dict, List

try:
    from .base import Base
except ImportError:
    raise ImportError("V2 base_transformer requires Base from relative core")


class BaseTransformer(Base):
    """
    Transformador base con funcionalidad común migrada desde BaseCalcular V1
    Contiene únicamente los métodos esenciales solicitados
    Hereda el decorador timeit de Base
    """

    # Constantes para meses en español
    MESES_ES = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre",
    }

    def __init__(self) -> None:
        """Inicialización base"""
        super().__init__()  # Llamar al constructor de Base

    def obtener_nombre_mes_es(self, fecha: Union[str, date, datetime]) -> str:
        """
        Convierte fecha a formato 'Mes_AAAA' en español
        Migrado exacto desde BaseCalcular V1
        """
        if isinstance(fecha, str):
            dt = datetime.strptime(fecha, "%Y-%m-%d").date()
        elif isinstance(fecha, datetime):
            dt = fecha.date()
        else:
            dt = fecha

        nombre = self.MESES_ES.get(dt.month, str(dt.month))
        return f"{nombre}_{dt.year}"

    def obtener_primer_dia_mes_anterior(self, fecha: Union[str, date, datetime]) -> str:
        """
        Retorna primer día del mes anterior en formato YYYY-MM-01
        Migrado exacto desde BaseCalcular V1
        """
        if isinstance(fecha, str):
            dt = datetime.strptime(fecha, "%Y-%m-%d").date()
        elif isinstance(fecha, datetime):
            dt = fecha.date()
        else:
            dt = fecha

        year, month = dt.year, dt.month
        if month == 1:
            new_year, new_month = year - 1, 12
        else:
            new_year, new_month = year, month - 1

        return f"{new_year}-{new_month:02d}-01"

    def _normalize(self, text: str) -> str:
        """Quita diacríticos y deja minúsculas."""
        nf = unicodedata.normalize("NFD", text)
        return "".join(c for c in nf if unicodedata.category(c) != "Mn").lower()

    def renombrar_columnas(
        self, df: pd.DataFrame, mapping: Dict[str, str], normalize: bool = True
    ) -> pd.DataFrame:
        """
        Renombra columnas según mapping normalizado
        Migrado exacto desde BaseCalcular V1
        """
        renames = {
            c: mapping[self._normalize(c) if normalize else c]
            for c in df.columns
            if (self._normalize(c) if normalize else c) in mapping
        }
        return df.rename(columns=renames)

    def formatear_fecha_mes(
        self, df: pd.DataFrame, columna: str = "Mes", formato: str = "%d/%m/%Y"
    ) -> pd.DataFrame:
        """
        Formatea columna de fecha dd/mm/YYYY → datetime
        Método reutilizable para transformaciones de fecha
        """
        df_copy = df.copy()
        df_copy[columna] = pd.to_datetime(
            df_copy[columna], format=formato, dayfirst=True, errors="raise"
        )
        return df_copy

    def eliminar_duplicados_por_columna(
        self, df: pd.DataFrame, columna: str, keep: str = "last"
    ) -> pd.DataFrame:
        """
        Elimina duplicados por columna específica
        Método reutilizable para limpieza de datos

        Args:
            df: DataFrame a procesar
            columna: Columna por la cual eliminar duplicados
            keep: 'first', 'last' o False para mantener/eliminar duplicados
        """
        return df.drop_duplicates(subset=columna, keep=keep)

    def convertir_a_dataframe(self, raw_data: List[Dict]) -> pd.DataFrame:
        """
        Convierte List[Dict] a DataFrame
        Método reutilizable para transformaciones de datos

        Args:
            raw_data: Lista de diccionarios a convertir

        Returns:
            DataFrame con los datos convertidos
        """
        if not raw_data:
            # Si la lista está vacía, retornar DataFrame vacío
            return pd.DataFrame()

        return pd.DataFrame(raw_data)
