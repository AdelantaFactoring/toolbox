"""
Adelanta Toolbox - Paquete interno
Paquete interno con arquitectura hexagonal
"""

__version__ = "1.0.0"

# Aliases para compatibilidad y API simple
__all__ = [
    # Comisiones
    "ComisionesAPI",
    # Fondos individuales
    "FondoPromocionalAPI",
    "get_fondo_promocional",
    "FondoCrecerAPI",
    "get_fondo_crecer",
    # Otros APIs
    "DiferidoExternoAPI",
    "DiferidoInternoAPI",
    "SectorPagadoresAPI",
    "VentasAutodetraccionesAPI",
    "ReferidosAPI",
    "OperacionesFueraSistemaAPI",
]

# Imports principales de la toolbox
try:
    from .api.comisiones_api import ComisionesAPI
except ImportError as e:
    raise ImportError(
        f"Módulos comisiones API V2 requieren dependencias de imports relativos: {e}"
    )

try:
    from .api.fondo_promocional_api import (
        FondoPromocionalAPI,
        get_fondo_promocional,
    )
except ImportError as e:
    raise ImportError(
        f"Módulos fondo promocional API V2 requieren dependencias de imports relativos: {e}"
    )

try:
    from .api.fondo_crecer_api import (
        FondoCrecerAPI,
        get_fondo_crecer,
    )
except ImportError as e:
    raise ImportError(
        f"Módulos fondo crecer API V2 requieren dependencias de imports relativos: {e}"
    )

# Otros APIs disponibles
try:
    from .api.diferido_externo_api import DiferidoExternoAPI
except ImportError as e:
    raise ImportError(
        f"DiferidoExternoAPI V2 requiere dependencias de imports relativos: {e}"
    )

try:
    from .api.diferido_interno_api import DiferidoInternoAPI
except ImportError as e:
    raise ImportError(
        f"DiferidoInternoAPI V2 requiere dependencias de imports relativos: {e}"
    )

try:
    from .api.sector_pagadores_api import SectorPagadoresAPI
except ImportError as e:
    raise ImportError(
        f"SectorPagadoresAPI V2 requiere dependencias de imports relativos: {e}"
    )

try:
    from .api.ventas_autodetracciones_api import VentasAutodetraccionesAPI
except ImportError as e:
    raise ImportError(
        f"VentasAutodetraccionesAPI V2 requiere dependencias de imports relativos: {e}"
    )

try:
    from .api.referidos_api import ReferidosAPI
except ImportError as e:
    raise ImportError(
        f"ReferidosAPI V2 requiere dependencias de imports relativos: {e}"
    )

try:
    from .api.operaciones_fuera_sistema_api import OperacionesFueraSistemaAPI
except ImportError as e:
    raise ImportError(
        f"OperacionesFueraSistemaAPI V2 requiere dependencias de imports relativos: {e}"
    )

# Exports públicos
__all__ = [
    # Comisiones
    "ComisionesAPI",
    # Fondos individuales
    "FondoPromocionalAPI",
    "get_fondo_promocional",
    "FondoCrecerAPI",
    "get_fondo_crecer",
    # Otros APIs
    "DiferidoExternoAPI",
    "DiferidoInternoAPI",
    "SectorPagadoresAPI",
    "VentasAutodetraccionesAPI",
    "ReferidosAPI",
]
