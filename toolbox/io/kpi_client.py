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
        try:
            logger(f"Llamando WebService: {start_date} a {end_date}")
            
            data = await self._obtener_data_con_autenticacion(
                url=V2Settings.get_kpi_colocaciones_url(),
                params={
                    "desde": start_date.strftime("%Y%m%d"),
                    "hasta": end_date.strftime("%Y%m%d"),
                    "fechaCorte": fecha_corte.strftime("%Y%m%d"),
                    "reporte": tipo_reporte,
                },
            )

            logger(f"📥 Datos CRUDOS del WebService: {len(data)} registros")
            
            liq_2510000109_raw = [r for r in data if r.get('CodigoLiquidacion') == 'LIQ2510000109']
            logger(f"🔍 LIQ2510000109 en datos CRUDOS: {len(liq_2510000109_raw)} registros")
            
            for i, record in enumerate(liq_2510000109_raw):
                logger(f"LIQ2510000109 CRUDO [{i+1}] - "
                    f"Documento: {record.get('NroDocumento')}, "
                    f"Neto: {record.get('NetoConfirmado')}, "
                    f"Desembolso: {record.get('MontoDesembolso')}, "
                    f"Fecha: {record.get('FechaOperacion')}")

            return data

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
                logger("=== INICIANDO PROCESO DE AUTENTICACIÓN ===")

                # Debug: mostrar URL y credenciales (sin password completo)
                url = V2Settings.get_kpi_token_url()

                logger(f"🌐 URL TOKEN: {url}")

                logger("📋 HEADERS: Content-Type=application/x-www-form-urlencoded")
                logger("📦 DATA FORMAT: form-data")

                logger("⚡ Enviando primera petición...")
                # HARDCODED CREDENTIALS PARA PRUEBA EN PRODUCCIÓN
                hardcoded_credentials = {
                    "username": V2Settings.get_kpi_credentials_username(),
                    "password": V2Settings.get_kpi_credentials_password(),
                }
                logger(f"🔧 USANDO CREDENCIALES HARDCODEADAS: {hardcoded_credentials}")
                response = await client.post(
                    url,
                    data=hardcoded_credentials,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )

                logger(f"📊 RESPONSE STATUS: {response.status_code}")
                logger(f"📋 RESPONSE HEADERS: {dict(response.headers)}")

                # Mostrar cuerpo de respuesta para errores
                if response.status_code != 200:
                    try:
                        response_body = response.text
                        logger(f"📄 RESPONSE BODY: {response_body[:300]}...")
                    except Exception as e:
                        logger(f"❌ Error leyendo response body: {e}")

                # Si falla con form-data, intentar con JSON
                if response.status_code == 401:
                    logger("🔄 REINTENTANDO CON JSON FORMAT...")
                    logger("📋 NEW HEADERS: Content-Type=application/json")
                    logger("📦 NEW DATA FORMAT: json")

                    # HARDCODED CREDENTIALS PARA PRUEBA EN PRODUCCIÓN (JSON)
                    hardcoded_credentials_json = {
                        "username": "adelantafactoring",
                        "password": "jSB@$M5tR9pAXsUy",
                    }
                    response = await client.post(
                        url,
                        json=hardcoded_credentials_json,
                        headers={"Content-Type": "application/json"},
                    )
                    logger(f"📊 JSON RESPONSE STATUS: {response.status_code}")

                    if response.status_code != 200:
                        try:
                            json_response_body = response.text
                            logger(
                                f"📄 JSON RESPONSE BODY: {json_response_body[:300]}..."
                            )
                        except Exception as e:
                            logger(f"❌ Error leyendo JSON response body: {e}")

                response.raise_for_status()

                logger("✅ AUTENTICACIÓN EXITOSA - Procesando token...")
                token_data = response.json()
                self.token = token_data.get("access_token")

                if not self.token:
                    logger("❌ TOKEN NO ENCONTRADO EN RESPUESTA")
                    logger(f"📄 Token data recibido: {token_data}")
                    raise ValueError("Token no encontrado en respuesta")

                logger(f"🎯 TOKEN OBTENIDO: {self.token[:10]}...{self.token[-10:]}")
                logger("=== AUTENTICACIÓN COMPLETADA EXITOSAMENTE ===")

        except httpx.TimeoutException:
            logger("❌ TIMEOUT EN AUTENTICACIÓN")
            logger(f"🌐 URL que falló: {V2Settings.get_kpi_token_url()}")
            raise Exception(
                f"Timeout obteniendo token: {V2Settings.get_kpi_token_url()}"
            )
        except httpx.HTTPStatusError as e:
            logger("❌ ERROR HTTP EN AUTENTICACIÓN")
            logger(f"📊 Status Code: {e.response.status_code}")
            logger(f"🌐 URL: {e.response.url}")
            logger(f"📋 Request Headers: {dict(e.request.headers)}")
            logger(f"📋 Response Headers: {dict(e.response.headers)}")

            error_details = f"HTTP {e.response.status_code}"
            try:
                error_body = e.response.text
                logger(f"📄 Error Body: {error_body}")
                error_details += f" - Body: {error_body[:200]}"
            except Exception as read_error:
                logger(f"❌ Error leyendo body: {read_error}")

            raise Exception(f"Error autenticación: {error_details}")
        except Exception as e:
            logger("❌ ERROR INESPERADO EN AUTENTICACIÓN")
            logger(f"🐛 Tipo de error: {type(e).__name__}")
            logger(f"📝 Mensaje: {str(e)}")
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
