"""
Configuración de Test usando pydantic-settings
"""

from pydantic_settings import BaseSettings
from typing import Dict


class TestSettings(BaseSettings):
    """Configuración de test usando variables de entorno"""

    # Webservice
    WEBSERVICE_BASE_URL: str
    KPI_USERNAME: str
    KPI_PASSWORD: str

    # Tasas de interés
    INTERESES_PEN: float
    INTERESES_USD: float

    # URLs Google Sheets
    FONDO_PROMOCIONAL_URL: str
    FONDO_CRECER_URL: str
    SALDOS_URL: str
    VENTAS_AUTODETRACCION_URL: str
    REFERIDOS_URL: str
    SECTOR_PAGADORES_URL: str
    OPERACIONES_FUERA_SISTEMA_PEN_URL: str
    OPERACIONES_FUERA_SISTEMA_USD_URL: str

    # Endpoints webservice
    OPERACIONES_FUERA_SISTEMA_PEN_ENDPOINT: str
    OPERACIONES_FUERA_SISTEMA_USD_ENDPOINT: str
    COMISIONES_ENDPOINT: str

    class Config:
        env_file = ".env"
        extra = "ignore"

    def to_toolbox_config(self) -> Dict:
        return {
            "WEBSERVICE_BASE_URL": self.WEBSERVICE_BASE_URL,
            "KPI_CREDENTIALS_USERNAME": self.KPI_USERNAME,
            "KPI_CREDENTIALS_PASSWORD": self.KPI_PASSWORD,
            "INTERESES_PEN": self.INTERESES_PEN,
            "INTERESES_USD": self.INTERESES_USD,
            "GOOGLE_SHEETS_URLS": {
                "fondo_promocional": self.FONDO_PROMOCIONAL_URL,
                "fondo_crecer": self.FONDO_CRECER_URL,
                "saldos": self.SALDOS_URL,
                "ventas_autodetraccion": self.VENTAS_AUTODETRACCION_URL,
                "referidos": self.REFERIDOS_URL,
                "sector_pagadores": self.SECTOR_PAGADORES_URL,
                "operaciones_fuera_sistema_pen": self.OPERACIONES_FUERA_SISTEMA_PEN_URL,
                "operaciones_fuera_sistema_usd": self.OPERACIONES_FUERA_SISTEMA_USD_URL,
            },
            "DATE_FORMATS": {
                "webservice": "%d/%m/%Y",
                "standard": "%Y-%m-%d",
                "display": "%d/%m/%Y",
            },
            "WEBSERVICE_ENDPOINTS": {
                "operaciones_fuera_sistema_pen": self.OPERACIONES_FUERA_SISTEMA_PEN_ENDPOINT,
                "operaciones_fuera_sistema_usd": self.OPERACIONES_FUERA_SISTEMA_USD_ENDPOINT,
                "comisiones": self.COMISIONES_ENDPOINT,
            },
        }


# Instancia global
test_settings = TestSettings()
