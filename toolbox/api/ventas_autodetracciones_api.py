"""
🌐 API V2 - Ventas Autodetracciones
INTERFAZ MIGRADA A POLARS PARA MEJOR PERFORMANCE
"""

import polars as pl
from io import BytesIO

try:
    from ..engines.ventas_autodetracciones_engine import VentasAutodetraccionesEngine
    from ..io.ventas_autodetracciones_client import VentasAutodetraccionesClient
    from ..processing.transformers.ventas_autodetracciones_transformer import (
        VentasAutodetraccionesTransformer,
    )
    from ..processing.validators.ventas_autodetracciones_validator import (
        VentasAutodetraccionesValidator,
    )

except ImportError:
    raise ImportError(
        "V2 ventas_autodetracciones_api requires VentasAutodetraccionesEngine from relative imports"
    )


class VentasAutodetraccionesAPI:
    """Wrapper que mantiene interfaz exacta de V1 + BytesIO para preparar migración a Polars"""

    def __init__(self, tipo_cambio_df: pl.DataFrame, comprobantes_file: BytesIO):
        """Constructor MODIFICADO para usar Polars DataFrame"""
        self.tipo_cambio_df = tipo_cambio_df
        self.comprobantes_df = comprobantes_file  # Ahora es BytesIO, no DataFrame
        self._engine = VentasAutodetraccionesEngine()
        self._client = VentasAutodetraccionesClient()
        self._transformer = VentasAutodetraccionesTransformer()
        self._validator = VentasAutodetraccionesValidator()

    async def generar_excel_autodetraccion(self, hasta: str) -> BytesIO:
        """Método IDÉNTICO a V1"""
        return await self._engine.generar_excel_autodetraccion(
            tipo_cambio_df=self.tipo_cambio_df,
            comprobantes_file=self.comprobantes_df,
            hasta=hasta,
        )


# Alias para compatibilidad con v1
VentasAutodetraccionesCalcular = VentasAutodetraccionesAPI
