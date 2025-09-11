"""
📡 Ventas Autodetracciones Client V2 - Placeholder

Este módulo mantiene la consistencia arquitectónica hexagonal.
VentasAutodetracciones no requiere cliente externo ya que los datos
vienen como parámetros (tipo_cambio_df, comprobantes_df).
"""

# Placeholder para mantener consistencia arquitectónica
# En arquitectura hexagonal, todos los módulos siguen el mismo patrón
# aunque algunos no requieran comunicación externa

try:
    from ..core.base_client import BaseClient
except ImportError:
    raise ImportError(
        "Ventas Autodetracciones Client V2 requires BaseClient from relative imports"
    )


class VentasAutodetraccionesClient(BaseClient):
    """
    Cliente V2 para Ventas Autodetracciones.

    Este cliente no realiza llamadas externas ya que los datos
    son proporcionados directamente como DataFrames.
    """

    def __init__(self):
        super().__init__(timeout=30)
        # No URL ya que no se requiere comunicación externa
        self.url = None
