"""
🏗️ Adelanta Toolbox - Arquitectura Hexagonal
Refactorización modular del sistema financiero ETL

📋 DOCUMENTACIÓN:
- ARCHITECTURE_GUIDE.md - Guía completa de arquitectura hexagonal
- QUICK_REFERENCE.md - Cheat sheet para desarrollo rápido

🚀 IMPORTACIONES SIMPLES:
- from adelanta_toolbox.toolbox.api.fondo_promocional_api import get_fondo_promocional
- from adelanta_toolbox.toolbox.api.fondo_crecer_api import get_fondo_crecer
- from adelanta_toolbox.toolbox.api.comisiones_api import ComisionesCalcular

🏛️ ARQUITECTURA:
api/         → 🌐 Interfaz pública simple
engines/     → ⚙️ Motores especializados (cálculo, validación, datos)
io/          → 📡 Comunicación externa (webservices, archivos)
processing/  → 🔄 Pipelines (transformers, validators)
schemas/     → 📊 Contratos Pydantic
config/      → ⚙️ Configuración centralizada
"""

__version__ = "2.0.0"

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

# Importar otros APIs disponibles
try:
    from .toolbox import (
        DiferidoExternoAPI,
        DiferidoInternoAPI,
        SectorPagadoresAPI,
        VentasAutodetraccionesAPI,
        ReferidosAPI,
    )
except ImportError as e:
    raise ImportError(
        f"Módulos API V2 requieren dependencias de imports relativos: {e}"
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
    # Otros APIs
    "DiferidoExternoAPI",
    "DiferidoInternoAPI",
    "SectorPagadoresAPI",
    "VentasAutodetraccionesAPI",
    "ReferidosAPI",
]
