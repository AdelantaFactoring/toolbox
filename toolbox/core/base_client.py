"""
Base Client V2

Cliente base para comunicación con webservices de Adelanta Factoring.
Proporciona funcionalidad común de HTTP requests con retry y logging.
"""

import aiohttp
import asyncio
import requests
from typing import List, Dict, Any
from tenacity import retry, stop_after_attempt, wait_fixed, wait_exponential

try:
    from .base import Base
    from ..config.settings import V2Settings
except ImportError:
    raise ImportError("V2 base requires V2Settings from relative config")

logger = V2Settings.logger


class BaseClient(Base):
    """
    🔌 Cliente base para webservices con funcionalidad async y retry automático.
    """

    def __init__(self, timeout: int = 30):
        self.timeout = aiohttp.ClientTimeout(total=timeout)

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    async def get_data_async(self, url: str) -> List[Dict[str, Any]]:
        """
        📡 Obtiene datos desde URL de forma asíncrona con retry automático.

        Args:
            url: URL del webservice

        Returns:
            Lista de diccionarios con los datos
        """
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger(f"✅ Datos obtenidos exitosamente desde {url}")
                        return data if isinstance(data, list) else []
                    else:
                        logger(f"❌ Error HTTP {response.status} desde {url}")
                        return []

        except asyncio.TimeoutError:
            logger(f"⏰ Timeout al conectar con {url}")
            raise
        except Exception as e:
            logger(f"❌ Error obteniendo datos desde {url}: {str(e)}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True,
    )
    def get_data_sync(self, url: str) -> List[Dict[str, Any]]:
        """
        📡 Obtiene datos síncronos con reintentos automáticos.
        """
        if not url or not url.startswith(("http://", "https://")):
            raise ValueError("URL inválida")

        try:
            response = requests.get(
                url,
                timeout=60,
                headers={
                    "User-Agent": "Adelanta-Toolbox/1.0",
                    "Accept": "application/json",
                },
                verify=True,
            )
            response.raise_for_status()

            if not response.content:
                return []

            return response.json()

        except requests.exceptions.Timeout:
            raise Exception(f"Timeout al obtener datos de {url}")
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response else "N/A"
            raise Exception(f"Error HTTP {status}: {url}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error de conexión: {e}")
        except Exception as e:
            raise Exception(f"Error inesperado: {e}")
