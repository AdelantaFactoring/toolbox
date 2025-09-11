"""
⚙️ KPI Engine V2 - Motor simple

Motor especializado SIMPLE para KPI heredando BaseEngine
Sin lógica de negocio compleja - solo operaciones básicas
"""

import pandas as pd

try:
    from ..core.base_engine import BaseEngine
except ImportError:
    raise ImportError("KPIEngine requiere BaseEngine de imports relativos")


class KPIEngine(BaseEngine):
    """Motor especializado simple para KPI heredando BaseEngine"""

    def __init__(self):
        super().__init__()

    def obtener_resumen_kpi(self, df: pd.DataFrame) -> None:
        """
        Obtiene resumen específico de datos de KPI

        Args:
            df: DataFrame con datos de KPI
        """
        self.obtener_resumen(df)
        # Resumen específico de KPI
        if "Moneda" in df.columns:
            resumen_moneda = df["Moneda"].value_counts()
            print(f"Distribución por moneda: {resumen_moneda.to_dict()}")

        if "Ejecutivo" in df.columns:
            total_ejecutivos = df["Ejecutivo"].nunique()
            print(f"Total ejecutivos únicos: {total_ejecutivos}")

        if "NetoConfirmado" in df.columns:
            total_colocaciones = df["NetoConfirmado"].sum()
            print(f"Total colocaciones: {total_colocaciones:,.2f}")

    async def obtener_datos_completos(self) -> pd.DataFrame:
        """Método heredado de BaseEngine para compatibilidad"""
        raise NotImplementedError(
            "KPIEngine es simple - usar KPIAPI para lógica compleja"
        )
