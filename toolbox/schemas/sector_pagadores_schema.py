"""
📊 Schemas Pydantic V2 - Sector Pagadores
Mantiene compatibilidad con v1 mientras mejora validación
"""

from pydantic import BaseModel, ConfigDict, field_validator


class SectorPagadoresSchema(BaseModel):
    """Schema base para Sector Pagadores"""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    RUCPagador: str
    Sector: str
    GrupoEco: str | None

    @field_validator("GrupoEco", mode="before")
    def convertir_valores_vacios_a_none(cls, v):
        """COPIADO EXACTO DE V1"""
        if v == "":
            return None
        return v


# Alias para compatibilidad con v1
SectorPagadoresCalcularSchema = SectorPagadoresSchema
