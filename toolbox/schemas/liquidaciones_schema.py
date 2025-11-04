"""
🏷️ Liquidaciones Schema - Validación robusta para datos de liquidaciones
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime
from typing import Optional

class LiquidacionSchema(BaseModel):
    """Schema para validación de datos de liquidaciones"""
    
    CodigoLiquidacion: str = Field(..., description="Código único de liquidación")
    TipoPago: Optional[str] = Field(None, description="Tipo de pago")
    FechaConfirmado: Optional[datetime] = Field(None, description="Fecha de confirmación")
    NetoConfirmado: Optional[float] = Field(None, description="Monto neto confirmado")
    MontoPago: Optional[float] = Field(None, description="Monto de pago")
    SaldoDeuda: Optional[float] = Field(None, description="Saldo de deuda")

    @field_validator("FechaConfirmado", mode="before")
    @classmethod
    def parsear_fecha(cls, v):
        """Validador personalizado para fechas"""
        if isinstance(v, str):
            try:
                return datetime.strptime(v, "%Y-%m-%d")
            except ValueError:
                return datetime.strptime(v, "%d/%m/%Y")
        return v

    model_config = ConfigDict(arbitrary_types_allowed=True)