"""
🏗️ Core V2 - Adelanta Factoring

Componentes base para la arquitectura hexagonal V2.
Mantiene únicamente las clases base esenciales.
"""

try:
    from .base import Base
    from .base_transformer import BaseTransformer
    from .base_validator import BaseValidator
except ImportError:
    raise ImportError("V2 core requires relative imports from base modules")

__all__ = [
    "Base",
    "BaseTransformer",
    "BaseValidator",
]
