"""
✅ Diferido Externo Validator V2 - Placeholder

Validator especializado para validación de datos de Diferido Externo
"""

try:
    from ...core.base_validator import BaseValidator
except ImportError:
    raise ImportError(
        "DiferidoExternoValidator V2 requiere BaseValidator de imports relativos"
    )


class DiferidoExternoValidator(BaseValidator):
    def __init__(self):
        super().__init__()

    pass  # Placeholder para futura implementación
