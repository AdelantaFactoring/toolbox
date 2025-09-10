"""
📡 Webservice FondoPromocional V2 - Cliente especializado

Cliente optimizado para obtener datos de Fondo Promocional que hereda de BaseClient
"""

from typing import List, Dict, Any

try:
    from ..core.base_client import BaseClient
    from ..config.settings import V2Settings
except ImportError:
    raise ImportError(
        "V2 fondo_promocional_client requires BaseClient and V2Settings from relative imports"
    )


class FondoPromocionalClient(BaseClient):
    """Cliente especializado para FondoPromocional que hereda de BaseClient"""

    def __init__(self):
        super().__init__(timeout=30)
        self.url = V2Settings.get_google_sheets_urls()["fondo_promocional"]

    def fetch_fondo_promocional_data(self) -> List[Dict[str, Any]]:
        """
        Obtiene datos de FondoPromocional de manera síncrona

        Returns:
            Lista de diccionarios con datos de fondo promocional
        """
        try:
            V2Settings.logger("Iniciando obtención de datos FondoPromocional")
            data = self.get_data_sync(self.url)

            V2Settings.logger(
                f"Datos FondoPromocional obtenidos exitosamente: {len(data)} registros"
            )
            return data

        except Exception as e:
            V2Settings.logger(f"Error obteniendo datos FondoPromocional: {e}")
            raise

    async def fetch_fondo_promocional_data_async(self) -> List[Dict[str, Any]]:
        """
        Obtiene datos de FondoPromocional de manera asíncrona

        Returns:
            Lista de diccionarios con datos de fondo promocional
        """
        try:
            V2Settings.logger("Iniciando obtención async de datos FondoPromocional")
            data = await self.get_data_async(self.url)

            V2Settings.logger(
                f"Datos FondoPromocional async obtenidos: {len(data)} registros"
            )
            return data

        except Exception as e:
            V2Settings.logger(f"Error obteniendo datos FondoPromocional async: {e}")
            raise
