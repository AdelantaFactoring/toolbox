"""
ComisionesCalcular V2 API
"""

from io import BytesIO
import pandas as pd


try:
    # Imports relativos para V2
    from .referidos_api import get_referidos
    from .fondo_crecer_api import get_fondo_crecer
    from .fondo_promocional_api import get_fondo_promocional
    from ..engines.comisiones_engine import ComisionesEngine
    from ..config.settings import V2Settings
except ImportError:
    raise ImportError("No se pudieron importar las dependencias de Comisiones API V2")

logger = V2Settings.logger


class ComisionesAPI:
    """
    ComisionesCalcular V2
    """

    def __init__(self, kpi_df: pd.DataFrame) -> None:
        """
        🏗️ Constructor IDÉNTICO a V1

        Args:
            kpi_df: DataFrame con datos KPI (mismo formato que V1)
        """
        self.kpi_df = kpi_df

        # 🔧 Inicializar APIs V2 en lugar de V1
        logger("ComisionesCalcular V2: Inicializando dependencias V2...")

        self.referidos_df = get_referidos(as_df=True)
        self.fondo_crecer_df = get_fondo_crecer(as_df=True)
        self.fondo_promocional_df = get_fondo_promocional(as_df=True)
        self._engine = ComisionesEngine()

        logger("ComisionesCalcular V2: Dependencias V2 inicializadas")

    def calcular_comisiones(
        self, start_date: str = "2023-01-01", end_date: str = "2024-05-31"
    ) -> BytesIO:
        """
        Flujo principal para el cálculo y generación de comisiones:
        1. Obtener y enriquecer datos base con referidos --google sheets externo--.
        2. Aplicar costos especiales de fondos (Crecer, Promocional).
        3. Procesar lógica de comisiones por mes y ejecutivo.
        4. Filtrar operaciones por fecha relevante (mes actual y anterior).
        5. Clasificar operaciones como "Lista Actual" o "Lista Anterior".
        6. Determinar si cada operación es "Nueva" o "Recurrente".
        7. Calcular comisiones según reglas específicas por tipo de ejecutivo.
        8. Incorporar operaciones con anticipos.
        9. Obtener resumen de comisiones por ejecutivo.
        10. Generar archivo ZIP con informes Excel (global, por ejecutivo, detalle).

        Parámetros:
        start_date: Fecha inicial en formato 'YYYY-MM-DD'. Default: "2023-01-01"
        end_date: Fecha final en formato 'YYYY-MM-DD'. Default: "2024-05-31"

        Retorna:
        BytesIO: Buffer en memoria conteniendo archivo ZIP con reportes Excel.
        """
        # 1. Obtener datos base con referidos
        kpi_df = self._engine.calcular_referidos(
            referidos_df=self.referidos_df, kpi_df=self.kpi_df
        )

        # 2. Aplicar costos especiales (Fondo Crecer, Promocional)
        kpi_df = self._engine.aplicar_costos_fondos_especiales(
            kpi_df=self.kpi_df,
            fondo_crecer_df=self.fondo_crecer_df,
            fondo_promocional_df=self.fondo_promocional_df,
        )

        # 3. Procesar lógica de comisiones
        comisiones_detalle_df, promos = self._engine.logica_comisiones(
            df=kpi_df,
            start_date=start_date,
            end_date=end_date,
        )

        # 4. Filtrar por fecha relevante
        lower_bound, upper_bound = self._engine.get_filter_bounds(end_date)

        kpi_df = kpi_df[
            (kpi_df["FechaOperacion"] >= lower_bound)
            & (kpi_df["FechaOperacion"] <= upper_bound)
        ]

        # 5. Clasificar operaciones (Lista Actual/Anterior)
        comisiones_df = self._engine.marcar_lista_pasada(
            df=kpi_df,
            comisiones_detalle_df=comisiones_detalle_df,
        )

        # 6. Determinar tipo de operación (Nuevo/Recurrente)
        comisiones_df = self._engine.seleccionar_y_clasificar_operaciones(
            df=comisiones_df, comisiones_detalle_df=comisiones_detalle_df
        )

        # 7. Calcular comisiones según reglas por tipo de ejecutivo
        comisiones_df = self._engine.calcular_comisiones_v1(df=comisiones_df)

        # 8. Incorporar operaciones con anticipos
        comisiones_df = self._engine.obtener_comisiones_con_anticipos(
            df=comisiones_df, end_date=end_date
        )

        # 9. Obtener resumen de comisiones por ejecutivo
        comisiones_detalle_df = self._engine.obtener_detalle_comisiones(
            df=comisiones_df
        )

        zip_bytes = self._engine.generar_zip_con_excels(
            comisiones_df,
            comisiones_detalle_df,
            end_date,
        )

        return zip_bytes


# Alias para compatibilidad con v1
ComisionesCalcular = ComisionesAPI
