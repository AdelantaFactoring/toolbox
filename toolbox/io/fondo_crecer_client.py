"""
📡 Webservice FondoCrecer V2 - Cliente especializado

Cliente optimizado para obtener datos de Fondo Crecer que hereda de BaseClient
"""

from typing import List, Dict, Any

try:
    from ..core.base_client import BaseClient
    from ..config.settings import V2Settings
except ImportError:
    raise ImportError(
        "V2 fondo_crecer_client requires BaseClient and V2Settings from relative imports"
    )


class FondoCrecerClient(BaseClient):
    """Cliente especializado para FondoCrecer que hereda de BaseClient"""

    def __init__(self):
        super().__init__(timeout=30)

    @property
    def url(self) -> str:
        """URL de Google Sheets para fondo crecer (lazy loading)"""
        return V2Settings.get_google_sheets_urls()["fondo_crecer"]

    def fetch_fondo_crecer_data(self) -> List[Dict[str, Any]]:
        """
        Obtiene datos de FondoCrecer de manera síncrona

        Returns:
            Lista de diccionarios con datos de fondo crecer
        """
        try:
            V2Settings.logger("Iniciando obtención de datos FondoCrecer")
            data = self.get_data_sync(self.url)

            V2Settings.logger(
                f"Datos FondoCrecer obtenidos exitosamente: {len(data)} registros"
            )
            return data

        except Exception as e:
            V2Settings.logger(f"Error obteniendo datos FondoCrecer: {e}")
            raise

    async def fetch_fondo_crecer_data_async(self) -> List[Dict[str, Any]]:
        """
        Obtiene datos de FondoCrecer de manera asíncrona

        Returns:
            Lista de diccionarios con datos de fondo crecer
        """
        try:
            V2Settings.logger("Iniciando obtención async de datos FondoCrecer")
            data = await self.get_data_async(self.url)

            V2Settings.logger(
                f"Datos FondoCrecer async obtenidos: {len(data)} registros"
            )
            return data

        except Exception as e:
            V2Settings.logger(f"Error obteniendo datos FondoCrecer async: {e}")
            raise
