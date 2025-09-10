"""
🔧 Template de Configuración - Adelanta Toolbox

COPIA este archivo y completa con tus valores reales ANTES de usar la librería
"""

# 📋 CONFIGURACIÓN COMPLETA REQUERIDA
TOOLBOX_CONFIG = {
    # 🌐 Webservice Configuration
    "WEBSERVICE_BASE_URL": "https://webservice.adelantafactoring.com",
    # 📊 KPI Credentials (CAMBIAR OBLIGATORIO)
    "KPI_CREDENTIALS": {
        "username": "TU_USERNAME_AQUI",
        "password": "TU_PASSWORD_AQUI",
    },
    # 💰 Financial Constants
    "INTERESES_PEN": 0.14,
    "INTERESES_USD": 0.12,
    # 🔗 Google Sheets URLs (CAMBIAR TODAS)
    "GOOGLE_SHEETS_URLS": {
        "fondo_promocional": "TU_URL_FONDO_PROMOCIONAL",
        "fondo_crecer": "TU_URL_FONDO_CRECER",
        "saldos": "TU_URL_SALDOS",
        "ventas_autodetraccion": "TU_URL_VENTAS_AUTODETRACCION",
        "referidos": "TU_URL_REFERIDOS",
        "sector_pagadores": "TU_URL_SECTOR_PAGADORES",
        "operaciones_fuera_sistema_pen": "TU_URL_OPERACIONES_PEN",
        "operaciones_fuera_sistema_usd": "TU_URL_OPERACIONES_USD",
    },
}

# 🚀 USO:
"""
import toolbox
from config_template import TOOLBOX_CONFIG

# 1. CONFIGURAR PRIMERO (obligatorio)
toolbox.configure(TOOLBOX_CONFIG)

# 2. Ahora sí usar la librería
from toolbox.api.kpi_api import get_kpi
resultado = await get_kpi(...)
"""
