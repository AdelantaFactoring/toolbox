"""
Adelanta Toolbox - Arquitectura Hexagonal
Refactorización modular del sistema financiero ETL

Documentación:
- ARCHITECTURE_GUIDE.md - Guía completa de arquitectura hexagonal
- DEVELOPMENT_PROMPT.md - Guía de desarrollo

Uso básico:
    from toolbox.api.kpi_api import get_kpi
    from toolbox.api.comisiones_api import ComisionesCalcular
    from toolbox.api.liquidaciones_api import obtener_datos_para_powerbi  # NUEVO
"""

__version__ = "0.5.0"

# Importaciones principales desde toolbox
try:
    from .toolbox.api.comisiones_api import ComisionesCalcular
except ImportError as e:
    raise ImportError(
        f"Módulos comisiones V2 requieren dependencias de imports relativos: {e}"
    )

try:
    from .toolbox.api.fondo_promocional_api import (
        FondoPromocionalAPI,
        get_fondo_promocional,
    )
except ImportError as e:
    raise ImportError(
        f"Módulos fondo promocional V2 requieren dependencias de imports relativos: {e}"
    )

try:
    from .toolbox.api.fondo_crecer_api import (
        FondoCrecerAPI,
        get_fondo_crecer,
    )
except ImportError as e:
    raise ImportError(
        f"Módulos fondo crecer V2 requieren dependencias de imports relativos: {e}"
    )

# NUEVO: Módulo de liquidaciones
try:
    from .toolbox.api.liquidaciones_api import (
        LiquidacionesAPI,
        procesar_liquidaciones_completo,
        obtener_datos_para_powerbi,
        obtener_reporte_completo
    )
except ImportError as e:
    raise ImportError(
        f"Módulos liquidaciones V2 requieren dependencias de imports relativos: {e}"
    )

# Aliases para compatibilidad y API simple
__all__ = [
    # Comisiones
    "ComisionesCalcular",
    # Fondos individuales
    "FondoPromocionalAPI",
    "get_fondo_promocional",
    "FondoCrecerAPI", 
    "get_fondo_crecer",
    # NUEVO: Liquidaciones
    "LiquidacionesAPI",
    "procesar_liquidaciones_completo",
    "obtener_datos_para_powerbi",
    "obtener_reporte_completo",
]