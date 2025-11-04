"""
📊 Schemas Pydantic V2 - Diferido Interno
Mantiene compatibilidad con v1 mientras mejora validación
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class DiferidoInternoSchema(BaseModel):
    """Schema base para Diferido Interno"""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    CodigoLiquidacion: Optional[str] = None
    NroDocumento: Optional[str] = None
    FechaOperacion: datetime
    FechaConfirmado: datetime
    Moneda: str
    Interes: float
    DiasEfectivo: int


# Alias para compatibilidad con v1
DiferidoInternoCalcularSchema = DiferidoInternoSchema
