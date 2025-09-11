"""
KPI Client V2 - Cliente especializado para colocaciones
"""

import httpx
from datetime import datetime
from typing import List, Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential

try:
    from ..core.base_client import BaseClient
    from ..config.settings import V2Settings
except ImportError:
    raise ImportError("KPI Client requiere BaseClient y V2Settings")

logger = V2Settings.logger


class KPIClient(BaseClient):
    """Cliente especializado para KPI/Colocaciones con autenticación Bearer"""

    def __init__(self):
        super().__init__(timeout=60)
        self.token = None

    async def fetch_colocaciones_data(
        self,
        start_date: datetime,
        end_date: datetime,
        fecha_corte: datetime,
        tipo_reporte: int = 2,
    ) -> List[Dict[str, Any]]:
        """
        Obtiene datos de colocaciones del webservice

        Args:
            start_date: Fecha inicio del reporte
            end_date: Fecha fin del reporte
            fecha_corte: Fecha de corte para el reporte
            tipo_reporte: Tipo de reporte (2 = detalle de anticipos sin detalle de pagos)

        Returns:
            Lista de diccionarios con datos de colocaciones
        """
        try:
            data = await self._obtener_data_con_autenticacion(
                url=V2Settings.get_kpi_colocaciones_url(),
                params={
                    "desde": start_date.strftime("%Y%m%d"),
                    "hasta": end_date.strftime("%Y%m%d"),
                    "fechaCorte": fecha_corte.strftime("%Y%m%d"),
                    "reporte": tipo_reporte,
                },
            )

            if isinstance(data, list):
                logger(f"Colocaciones obtenidas: {len(data)} registros")
                return data
            else:
                logger("Respuesta no es lista, devolviendo lista vacía")
                return []

        except Exception as e:
            logger(f"Error obteniendo colocaciones: {e}")
            raise

    async def _obtener_data_con_autenticacion(
        self, url: str, params: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Obtiene datos con autenticación automática"""
        try:
            if not self._tiene_token():
                await self._obtener_token()

            async with httpx.AsyncClient(timeout=60) as client:
                return await self._obtener_data_async(client, url, params)

        except Exception as e:
            logger(f"Error en autenticación, reintentando: {e}")
            if self._tiene_token():
                self._limpiar_token()
                await self._obtener_token()
                async with httpx.AsyncClient(timeout=60) as client:
                    return await self._obtener_data_async(client, url, params)
            raise

    @retry(
        stop=stop_after_attempt(2), wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def _obtener_token(self) -> None:
        """Obtiene token de autenticación"""
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                logger("Obteniendo token de acceso...")

                # Debug: mostrar URL y credenciales (sin password completo)
                url = V2Settings.get_kpi_token_url()
                credentials = V2Settings.get_kpi_credentials()
                debug_creds = {
                    k: v if k != "password" else f"{v[:3]}***{v[-2:]}"
                    for k, v in credentials.items()
                }
                logger(f"URL: {url}")
                logger(f"Credentials: {debug_creds}")

                response = await client.post(
                    url,
                    data=credentials,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )

                logger(f"Response Status: {response.status_code}")

                # Si falla con form-data, intentar con JSON
                if response.status_code == 401:
                    logger("Intentando con JSON format...")
                    response = await client.post(
                        url,
                        json=credentials,
                        headers={"Content-Type": "application/json"},
                    )
                    logger(f"JSON Response Status: {response.status_code}")

                response.raise_for_status()

                token_data = response.json()
                self.token = token_data.get("access_token")

                if not self.token:
                    raise ValueError("Token no encontrado en respuesta")

                logger("Token obtenido exitosamente")

        except httpx.TimeoutException:
            raise Exception(
                f"Timeout obteniendo token: {V2Settings.get_kpi_token_url()}"
            )
        except httpx.HTTPStatusError as e:
            error_details = f"HTTP {e.response.status_code}"
            try:
                error_body = e.response.text
                error_details += f" - Body: {error_body[:200]}"
            except Exception:
                pass
            raise Exception(f"Error autenticación: {error_details}")
        except Exception as e:
            raise Exception(f"Error inesperado obteniendo token: {e}")

    @BaseClient.timeit
    @retry(
        stop=stop_after_attempt(2), wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def _obtener_data_async(
        self, client: httpx.AsyncClient, url: str, params: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Obtiene datos usando token de autenticación"""
        if not self.token:
            raise ValueError("Token requerido para obtener datos")

        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            logger(f"Consultando: {url}")
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()

            data = response.json()
            logger(
                f"Datos obtenidos: {len(data) if isinstance(data, list) else 'N/A'} registros"
            )
            return data

        except httpx.TimeoutException:
            raise Exception(f"Timeout consultando: {url}")
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error HTTP {e.response.status_code}: {e.response.text}")
        except Exception as e:
            raise Exception(f"Error inesperado: {e}")

    def _tiene_token(self) -> bool:
        """Verifica si hay token válido"""
        return self.token is not None

    def _limpiar_token(self) -> None:
        """Limpia token almacenado"""
        self.token = None
        logger("Token limpiado")
