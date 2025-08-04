"""
📡 Sector Pagadores Client V2 - Cliente webservice especializado

Cliente optimizado para obtener datos de Sector Pagadores que hereda de BaseClient
"""

from typing import Dict, Any

try:
    from ..config.settings import V2Settings
    from ..core.base_client import BaseClient
except ImportError:
    raise ImportError(
        "SectorPagadoresClient V2 requiere BaseClient de imports relativos"
    )


class SectorPagadoresClient(BaseClient):
    """Cliente especializado para Sector Pagadores que hereda de BaseClient"""

    def __init__(self):
        super().__init__(timeout=30)
        self.url = V2Settings.GOOGLE_SHEETS_URLS["sector_pagadores"]

    def fetch_sector_pagadores_data(self) -> Dict[str, Any]:
        """
        Obtiene datos de Sector Pagadores de manera síncrona

        Returns:
            Diccionario con datos de sector pagadores
        """
        try:
            V2Settings.logger("Iniciando obtención de datos Sector Pagadores")
            data = self.get_data_sync(self.url)

            V2Settings.logger(
                f"Datos Sector Pagadores obtenidos exitosamente: {len(data)} registros"
            )
            return data

        except Exception as e:
            V2Settings.logger(f"Error obteniendo datos Sector Pagadores: {e}")
            raise
