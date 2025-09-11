"""
Configuración V2 - Settings centralizados para arquitectura hexagonal
"""

import logging
from pprint import pprint
import os


class V2Settings:
    """
    Configuración centralizada para v2 - REQUIERE INICIALIZACIÓN
    """

    # Estado de configuración
    _initialized = False
    _config = None

    # 🔧 Logger Configuration
    @staticmethod
    def logger(message: str) -> None:
        """Logger callable mejorado para compatibilidad V1"""
        print("🔧 ADELANTA TOOLBOX DEBUG:")
        pprint(message)
        print("-" * 50)

        _logger = logging.getLogger(__name__)
        _logger.warning(message)

    @classmethod
    def initialize(cls, config: dict) -> None:
        """
        Inicializa la configuración con settings personalizados

        Args:
            config: Diccionario con toda la configuración necesaria
        """
        required_keys = [
            "WEBSERVICE_BASE_URL",
            "KPI_CREDENTIALS",
            "GOOGLE_SHEETS_URLS",
            "INTERESES_PEN",
            "INTERESES_USD",
        ]

        missing_keys = [key for key in required_keys if key not in config]
        if missing_keys:
            raise ValueError(f"Configuración incompleta. Faltan: {missing_keys}")

        cls._config = config
        cls._initialized = True
        cls.logger("✅ Adelanta Toolbox configurado correctamente")

    @classmethod
    def _ensure_initialized(cls):
        """Verifica que la configuración haya sido inicializada"""
        if not cls._initialized:
            raise RuntimeError(
                "❌ Adelanta Toolbox no inicializado. "
                "Debe llamar toolbox.configure(config) primero."
            )

    # Métodos de configuración que requieren inicialización
    @classmethod
    def get_webservice_base_url(cls) -> str:
        """Obtiene la URL base del webservice"""
        cls._ensure_initialized()
        return cls._config["WEBSERVICE_BASE_URL"]

    @classmethod
    def get_kpi_token_url(cls) -> str:
        """Obtiene la URL del token KPI"""
        cls._ensure_initialized()
        return f"{cls._config['WEBSERVICE_BASE_URL']}/webservice/token"

    @classmethod
    def get_kpi_colocaciones_url(cls) -> str:
        """Obtiene la URL de colocaciones KPI"""
        cls._ensure_initialized()
        return f"{cls._config['WEBSERVICE_BASE_URL']}/webservice/liquidacionCab/subquery-cab-con-anticipos"

    @classmethod
    def get_kpi_credentials(cls) -> dict:
        """Obtiene las credenciales KPI"""
        cls._ensure_initialized()
        return cls._config["KPI_CREDENTIALS"]

    @classmethod
    def get_intereses_pen(cls) -> float:
        """Obtiene la tasa de interés PEN"""
        cls._ensure_initialized()
        return cls._config["INTERESES_PEN"]

    @classmethod
    def get_intereses_usd(cls) -> float:
        """Obtiene la tasa de interés USD"""
        cls._ensure_initialized()
        return cls._config["INTERESES_USD"]

    @classmethod
    def get_google_sheets_urls(cls) -> dict:
        """Obtiene las URLs de Google Sheets"""
        cls._ensure_initialized()
        return cls._config["GOOGLE_SHEETS_URLS"]

    @classmethod
    def get_webservice_endpoints(cls) -> dict:
        """Obtiene los endpoints del webservice"""
        cls._ensure_initialized()
        base_url = cls._config["WEBSERVICE_BASE_URL"]
        return {
            "operaciones_fuera_sistema_pen": f"{base_url}/webservice/consultas/operacionesfuerasistema/PEN",
            "operaciones_fuera_sistema_usd": f"{base_url}/webservice/consultas/operacionesfuerasistema/USD",
            "comisiones": f"{base_url}/webservice",
        }

    # Propiedades de compatibilidad (mantienen API existente)
    @property
    def WEBSERVICE_BASE_URL(self) -> str:
        return self.__class__.get_webservice_base_url()

    @property
    def KPI_TOKEN_URL(self) -> str:
        return self.__class__.get_kpi_token_url()

    @property
    def KPI_COLOCACIONES_URL(self) -> str:
        return self.__class__.get_kpi_colocaciones_url()

    @property
    def KPI_CREDENTIALS(self) -> dict:
        return self.__class__.get_kpi_credentials()

    @property
    def INTERESES_PEN(self) -> float:
        return self.__class__.get_intereses_pen()

    @property
    def INTERESES_USD(self) -> float:
        return self.__class__.get_intereses_usd()

    @property
    def GOOGLE_SHEETS_URLS(self) -> dict:
        return self.__class__.get_google_sheets_urls()

    @property
    def WEBSERVICE_ENDPOINTS(self) -> dict:
        return self.__class__.get_webservice_endpoints()

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
