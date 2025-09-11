"""
📊 Schemas Pydantic V2 - FondoPromocional

Mantiene compatibilidad con v1 mientras mejora validación
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict


class FondoPromocionalSchema(BaseModel):
    """Schema para datos de Fondo Promocional"""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    CodigoLiquidacion: str = Field(
        ..., description="Código de liquidación", min_length=1
    )

    @field_validator("CodigoLiquidacion", mode="before")
    @classmethod
    def validate_liquidacion(cls, v):
        """Normaliza el código de liquidación"""
        if v is None:
            raise ValueError("CodigoLiquidacion no puede ser None")
        return str(v).strip().upper()
