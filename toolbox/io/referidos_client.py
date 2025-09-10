"""
📡 Webservice Referidos V2 - Cliente especializado

Cliente optimizado para obtener datos de Referidos que hereda de BaseClient
"""

from typing import List, Dict, Any

try:
    from ..core.base_client import BaseClient
    from ..config.settings import V2Settings
except ImportError:
    raise ImportError(
        "V2 referidos_client requires BaseClient and V2Settings from relative imports"
    )


class ReferidosClient(BaseClient):
    """Cliente especializado para Referidos que hereda de BaseClient"""

    def __init__(self):
        super().__init__(timeout=30)
        self.url = V2Settings.get_google_sheets_urls()["referidos"]

    def fetch_referidos_data(self) -> List[Dict[str, Any]]:
        """
        Obtiene datos de Referidos de manera síncrona

        Returns:
            Lista de diccionarios con datos de referidos
        """
        try:
            V2Settings.logger("Iniciando obtención de datos Referidos")
            data = self.get_data_sync(self.url)

            V2Settings.logger(
                f"Datos Referidos obtenidos exitosamente: {len(data)} registros"
            )
            return data

        except Exception as e:
            V2Settings.logger(f"Error obteniendo datos Referidos: {e}")
            raise

    async def fetch_referidos_data_async(self) -> List[Dict[str, Any]]:
        """
        Obtiene datos de Referidos de manera asíncrona

        Returns:
            Lista de diccionarios con datos de referidos
        """
        try:
            V2Settings.logger("Iniciando obtención async de datos Referidos")
            data = await self.get_data_async(self.url)

            V2Settings.logger(f"Datos Referidos async obtenidos: {len(data)} registros")
            return data

        except Exception as e:
            V2Settings.logger(f"Error obteniendo datos Referidos async: {e}")
            raise
