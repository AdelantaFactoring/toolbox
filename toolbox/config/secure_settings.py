# ⚠️ SEGURIDAD: Remover credenciales sensibles de settings.py
# Este archivo debe contener las credenciales reales (NO commitear)

"""
🔒 Configuración de Producción Segura
Copiar este archivo como 'production_settings.py' y configurar credenciales reales
"""

import os
from .settings import V2Settings as BaseSettings


class ProductionSettings(BaseSettings):
    """Configuración segura para producción"""

    # 🔐 Credenciales desde variables de entorno
    KPI_CREDENTIALS = {
        "username": os.getenv("ADELANTA_KPI_USERNAME", "adelantafactoring"),
        "password": os.getenv("ADELANTA_KPI_PASSWORD"),  # ⚠️ Definir en .env
    }

    # 🌐 URLs con variables de entorno para flexibilidad
    WEBSERVICE_BASE_URL = os.getenv(
        "ADELANTA_WEBSERVICE_URL", "https://webservice.adelantafactoring.com"
    )

    # 📊 KPI Configuration con URLs dinámicas
    KPI_TOKEN_URL = f"{WEBSERVICE_BASE_URL}/webservice/token"
    KPI_COLOCACIONES_URL = f"{WEBSERVICE_BASE_URL}/webservice/colocaciones"


# 🔧 Auto-detección de entorno
def get_settings():
    """Retorna configuración apropiada según entorno"""
    if os.getenv("ADELANTA_ENV") == "production":
        return ProductionSettings()
    return BaseSettings()


# Instancia global segura
settings = get_settings()
