"""
📊 Schemas Pydantic V2 - Ventas Autodetracciones

Mantiene compatibilidad con v1 mientras mejora validación
"""

from pydantic import BaseModel, ConfigDict


class VentasAutodetraccionesSchema(BaseModel):
    """Schema base para Ventas Autodetracciones"""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Placeholder - VentasAutodetracciones no requiere schemas específicos
    # ya que trabaja directamente con DataFrames pandas
    pass


# Alias para compatibilidad con v1
VentasAutodetraccionesCalcularSchema = VentasAutodetraccionesSchema
