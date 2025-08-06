"""
📡 OperacionesFueraSistema Client V2 - Cliente especializado
Cliente que hereda de BaseClient para webservices
"""

try:
    from ..core.base_client import BaseClient
    from ..config.settings import settings
except ImportError:
    raise ImportError(
        "OperacionesFueraSistemaClient V2 requiere BaseClient de imports relativos"
    )


class OperacionesFueraSistemaClient(BaseClient):

    def __init__(self):
        super().__init__(timeout=30)
        self.url_pen = settings.GOOGLE_SHEETS_URLS["operaciones_fuera_sistema_pen"]
        self.url_usd = settings.GOOGLE_SHEETS_URLS["operaciones_fuera_sistema_usd"]

    def fetch_operaciones_fuera_sistema_pen_data(self):
        """Obtiene datos PEN de manera síncrona"""
        try:
            settings.logger("Iniciando obtención de datos OperacionesFueraSistema PEN")
            data = self.get_data_sync(self.url_pen)
            settings.logger(f"Datos PEN obtenidos: {len(data)} registros")
            return data
        except Exception as e:
            settings.logger(f"Error obteniendo datos PEN: {e}")
            raise

    def fetch_operaciones_fuera_sistema_usd_data(self):
        """Obtiene datos USD de manera síncrona"""
        try:
            settings.logger("Iniciando obtención de datos OperacionesFueraSistema USD")
            data = self.get_data_sync(self.url_usd)
            settings.logger(f"Datos USD obtenidos: {len(data)} registros")
            return data
        except Exception as e:
            settings.logger(f"Error obteniendo datos USD: {e}")
            raise
