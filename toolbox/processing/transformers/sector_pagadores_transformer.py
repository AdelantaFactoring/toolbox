"""
🔄 Sector Pagadores Transformer V2 - Procesamiento de datos

Transformer especializado para procesamiento de datos de Sector Pagadores
"""

import pandas as pd

try:
    from ...core.base_transformer import BaseTransformer
except ImportError:
    raise ImportError(
        "SectorPagadoresTransformer V2 requiere BaseTransformer de imports relativos"
    )


class SectorPagadoresTransformer(BaseTransformer):
    def __init__(self):
        super().__init__()

    def procesar_datos_sector_pagadores(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Procesa datos de sectores pagadores
        Args:
            df: DataFrame con datos de sectores pagadores
        Returns:
            DataFrame procesado con columnas esperadas
        """

        df["RUCPagador"] = df["RUC"].astype(str).str.strip()
        df["Sector"] = df["SECTOR"].str.strip()
        df["GrupoEco"] = df["GRUPO ECO."].str.strip().replace({"": pd.NA})
        df = df[["RUCPagador", "Sector", "GrupoEco"]].drop_duplicates(
            subset=["RUCPagador"]
        )
        return df
