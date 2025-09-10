"""
Configuración V2 - Settings centralizados para arquitectura hexagonal
"""

import logging
from pprint import pprint
import os


class V2Settings:
    """
    Configuración centralizada para v2
    Mantiene compatibilidad con v1 durante la transición
    """

    # 🔧 Logger Configuration
    @staticmethod
    def logger(message: str) -> None:
        """
        Logger callable mejorado para compatibilidad V1

        En desarrollo usa pprint para mejor visualización
        En producción usa logging estándar
        """
        # Detectar si estamos en desarrollo o producción

        # En desarrollo: usar pprint para mejor visualización
        print("🔧 ADELANTA TOOLBOX DEBUG:")
        pprint(message)
        print("-" * 50)

        # En producción: usar logging estándar
        _logger = logging.getLogger(__name__)
        _logger.warning(message)

    # 🌐 Webservice Configuration
    WEBSERVICE_BASE_URL = "https://webservice.adelantafactoring.com"

    # 📊 KPI Configuration
    KPI_TOKEN_URL = f"{WEBSERVICE_BASE_URL}/webservice/token"
    KPI_COLOCACIONES_URL = f"{WEBSERVICE_BASE_URL}/webservice/colocaciones"
    KPI_CREDENTIALS = {
        "username": "adelantafactoring",
        "password": "CHANGE_ME_IN_PRODUCTION",  # ⚠️ Usar variables de entorno
    }

    # 💰 Financial Constants
    INTERESES_PEN: float = 0.14
    INTERESES_USD: float = 0.12

    # 📅 Date Formats
    DATE_FORMATS = {
        "webservice": "%d/%m/%Y",
        "standard": "%Y-%m-%d",
        "display": "%d/%m/%Y",
    }

    # 🔗 Google Sheets URLs - Centralizadas
    GOOGLE_SHEETS_URLS = {
        "fondo_promocional": "https://script.google.com/macros/s/AKfycbzpX9RKtvJwN1QgFMU15hi1DXHtRhFlIC6jW8_QYTB-sQQIntsDO7fG6jWgKJb95V6X/exec",
        "fondo_crecer": "https://script.google.com/macros/s/AKfycbyFKvZcqZNBm2XktdOR4lrv5Wwd_PwovO85INFieEqzQexXgwXD5XuF-nPWPME1sjGFlQ/exec",
        "saldos": "https://script.google.com/macros/s/AKfycbzSFKR3DyDo9Ezxsq_75DDJ1vze76Lj_kC4iXiFMvAE_t6Xbi9rHrejT9v8CnWqWV9UKw/exec",
        "ventas_autodetraccion": "https://script.google.com/macros/s/AKfycbxZS8ahi8BnlBJcRx4H9E_qy1JHbhIATqnNUx_P-OJGrDstcGjDtACpeftKozeOCp0_/exec",
        "referidos": "https://script.google.com/macros/s/AKfycbxZS8ahi8BnlBJcRx4H9E_qy1JHbhIATqnNUx_P-OJGrDstcGjDtACpeftKozeOCp0_/exec",
        "sector_pagadores": "https://script.google.com/macros/s/AKfycbxxdJazJbEJ7qbGgi8oBAJrzIZjpnD1cYKv1RkcBQtQSx7KA60UGaXMYHTKxKOeRC3c/exec",
        "operaciones_fuera_sistema_pen": "https://script.google.com/macros/s/AKfycbyWsLb2hCr7cuXJIUorkmQJZEPnH-7i24Zy2yRlSfOwb4BZGPs01zdmiRVKuzRN8uKCtg/exec",
        "operaciones_fuera_sistema_usd": "https://script.google.com/macros/s/AKfycbz3Jt1zj_29QPEM4hexYdlvcgSMNUICsF9xNsEPlDaGSF-0VXv7JPouSkhGH8AubU5-/exec",
    }

    # 🔗 Webservice Endpoints
    WEBSERVICE_ENDPOINTS = {
        "operaciones_fuera_sistema_pen": f"{WEBSERVICE_BASE_URL}/webservice/consultas/operacionesfuerasistema/PEN",
        "operaciones_fuera_sistema_usd": f"{WEBSERVICE_BASE_URL}/webservice/consultas/operacionesfuerasistema/USD",
        "comisiones": f"{WEBSERVICE_BASE_URL}/webservice",
    }

    # 🏷️ Field Mappings - Conservar compatibilidad
    FIELD_MAPPINGS = {
        "ejecutivo_unification": {
            # Mapeo de nombres de ejecutivos para unificación
            # Se mantendrá desde v1 para compatibilidad
        }
    }

    # ⚡ Performance Settings
    CACHE_TTL = 300  # 5 minutos
    MAX_RETRIES = 3
    REQUEST_TIMEOUT = 30

    # 🔧 Processing Options
    PROCESSING_OPTIONS = {
        "apply_legacy_date_formatting": True,  # Compatibilidad con CXCETLProcessor
        "validate_financial_precision": True,
        "enable_fuzzy_matching": True,
        "preserve_source_data": True,  # NEVER modify original financial data
    }


# Instancia global para fácil acceso
settings = V2Settings()
