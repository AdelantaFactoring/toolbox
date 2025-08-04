"""
🏷️ Referidos Schema V2 - Adelanta Factoring Financial ETL

Schema único para el sistema de referidos con validación RUST-powered.
Mantiene compatibilidad completa con el sistema legacy.
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime


class ReferidosSchema(BaseModel):
    """
    📊 Schema único para datos de referidos V2
    Compatible 100% con el sistema legacy
    """

    Referencia: str = Field(..., description="Referencia del referido")
    CodigoLiquidacion: str = Field(..., description="Código de liquidación")
    Ejecutivo: str = Field(..., description="Ejecutivo asignado")
    Mes: datetime = Field(..., description="Mes de referencia")

    @field_validator("Mes", mode="before")
    @classmethod
    def parsear_mes(cls, v):
        """
        🗓️ Acepta cadena 'dd/mm/yyyy' y la convierte a datetime.
        Mantiene compatibilidad con el formato original.
        """
        if isinstance(v, str):
            return datetime.strptime(v, "%d/%m/%Y")
        if isinstance(v, datetime):
            return v
        raise ValueError(f"Formato de fecha no soportado: {type(v)}")

    @field_validator("Referencia", "CodigoLiquidacion", "Ejecutivo", mode="before")
    @classmethod
    def validar_strings(cls, v):
        """🔧 Valida y limpia campos de texto"""
        if not v or not isinstance(v, str):
            raise ValueError("Campo de texto no puede estar vacío")
        return v.strip()

    model_config = ConfigDict(arbitrary_types_allowed=True)
