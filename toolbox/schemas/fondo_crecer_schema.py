"""
📊 Schemas Pydantic V2 - FondoCrecer

Mantiene compatibilidad con v1 mientras mejora validación financiera
"""

from pydantic import BaseModel, Field, field_validator

# from typing import Optional
# from decimal import Decimal


class FondoCrecerSchema(BaseModel):
    """Schema para datos de Fondo Crecer con validación de garantía"""

    CodigoLiquidacion: str = Field(
        ..., description="Código de liquidación", min_length=1
    )

    Garantia: float

    @field_validator("Garantia", mode="before")
    @classmethod
    def parsear_garantia(cls, v):
        """
        Recibe "75%" y devuelve 0.75
        """
        if isinstance(v, str) and v.endswith("%"):
            return float(v.rstrip("%")) / 100
        return float(v)
