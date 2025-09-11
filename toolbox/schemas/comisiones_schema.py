"""
Schemas Pydantic V2 - Comisiones
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, Literal
from datetime import datetime
import pandas as pd
from decimal import Decimal


class ComisionesSchema(BaseModel):
    """Schema principal para datos de comisiones"""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    RUCCliente: Optional[str] = Field(None, description="RUC del cliente")
    RUCPagador: str = Field(..., description="RUC del pagador", min_length=1)
    Tipo: Literal["Nuevo", "Recurrente"] = Field(..., description="Tipo de operación")
    Detalle: str = Field(..., description="Detalle de la operación", min_length=1)
    Mes: str = Field(..., description="Mes de la operación", min_length=1)
    TipoOperacion: Literal["Factoring", "Confirming", "Capital de Trabajo"] = Field(
        ..., description="Tipo de operación financiera"
    )
    Ejecutivo: str = Field(..., description="Ejecutivo responsable", min_length=1)

    # Campos adicionales para cálculos
    MontoComision: Optional[Decimal] = Field(
        None, description="Monto de comisión calculado"
    )
    FechaOperacion: Optional[datetime] = Field(
        None, description="Fecha de la operación"
    )

    @field_validator("RUCCliente", mode="before")
    @classmethod
    def validate_ruc_cliente(cls, v):
        """Convierte NaN o valores missing de pandas en None"""
        if (
            pd.isna(v) if hasattr(pd, "isna") else v != v
        ):  # Compatibilidad con/sin pandas
            return None
        return str(v).strip() if v else None

    @field_validator("RUCPagador", mode="before")
    @classmethod
    def validate_ruc_pagador(cls, v):
        """Normaliza RUC del pagador"""
        if v is None:
            raise ValueError("RUC Pagador no puede ser None")
        return str(v).strip()

    @field_validator("MontoComision", mode="before")
    @classmethod
    def validate_monto_comision(cls, v):
        """Convierte a Decimal para precisión financiera"""
        if v is None:
            return None
        return Decimal(str(v))


class PromocionSchema(BaseModel):
    """Schema para promociones de ejecutivos - COPIADO EXACTO DE V1"""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    Ejecutivo: str = Field(..., description="Ejecutivo en promoción", min_length=1)
    TipoOperacion: Literal["Factoring", "Confirming", "Capital de Trabajo"] = Field(
        ..., description="Tipo de operación en promoción"
    )
    FechaExpiracion: datetime = Field(
        ..., description="Fecha de expiración de la promoción"
    )

    def __init__(self, **data):
        # 🔧 COMPATIBILIDAD V1: Convertir "Fecha de expiración" a "FechaExpiracion"
        if "Fecha de expiración" in data:
            data["FechaExpiracion"] = data.pop("Fecha de expiración")
        super().__init__(**data)

    @field_validator("FechaExpiracion", mode="before")
    @classmethod
    def validate_fecha_expiracion(cls, v):
        """Normaliza fecha de expiración"""
        if isinstance(v, str):
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        return v


class RegistroComisionSchema(BaseModel):
    """Schema para registro individual de comisión - COPIADO EXACTO DE V1"""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    RUCCliente: str
    RUCPagador: str
    Tipo: str  # "Nuevo" o "Recurrente"
    Detalle: str
    Mes: str  # Formato "YYYY-MM"
    TipoOperacion: str  # "Factoring", "Confirming", "Capital de Trabajo"
    Ejecutivo: str

    @field_validator("RUCCliente", mode="before")
    @classmethod
    def validate_ruc_cliente(cls, v):
        """Convierte NaN o valores missing de pandas en string vacío para V1"""
        if pd.isna(v) if hasattr(pd, "isna") else v != v:
            return ""
        return str(v).strip() if v else ""
