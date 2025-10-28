"""
🌐 KPI API V2 - Interfaz pública con lógica compleja

API pública para KPI con toda la lógica de negocio compleja
Separación de responsabilidades: Engine simple, API complejo
"""

import pandas as pd
from datetime import datetime
from typing import List, Dict, Union

try:
    from ..config.settings import V2Settings
    from ..engines.kpi_engine import KPIEngine
    from ..io.kpi_client import KPIClient
    from ..processing.transformers.kpi_transformer import KPITransformer
    from ..processing.validators.kpi_validator import KPIValidator
    from ..api.referidos_api import ReferidosAPI
    from ..api.operaciones_fuera_sistema_api import OperacionesFueraSistemaAPI
    from ..api.sector_pagadores_api import SectorPagadoresAPI
    from ..engines.comisiones_engine import ComisionesEngine
except ImportError:
    raise ImportError(
        "KPIAPI requiere todas las dependencias de arquitectura hexagonal"
    )

logger = V2Settings.logger


class KPIAPI:
    """
    API pública para KPI con lógica de negocio compleja

    Esta clase contiene toda la lógica compleja que fue removida del Engine
    para mantener una separación apropiada de responsabilidades.
    """

    def __init__(self, tipo_cambio_df: pd.DataFrame = None):
        """
        Inicializa la API de KPI con todos los componentes necesarios

        Args:
            tipo_cambio_df: DataFrame con datos de tipo de cambio
        """
        if tipo_cambio_df is None:
            # Crear DataFrame vacío por defecto
            tipo_cambio_df = pd.DataFrame(
                {"TipoCambioFecha": [], "TipoCambioVenta": [], "TipoCambioCompra": []}
            )

        self.tipo_cambio_df = tipo_cambio_df

        # Inicializar Engine simple
        self._engine = KPIEngine()
        self._comisiones_engine = ComisionesEngine()

        # Inicializar componentes complejos en API
        self._client = KPIClient()
        self._transformer = KPITransformer()
        self._validator = KPIValidator()

        # Engines auxiliares

        self._operaciones_fuera_sistema_api = OperacionesFueraSistemaAPI()
        self._sector_pagadores_api = SectorPagadoresAPI()
        self._referidos_api = ReferidosAPI()

        logger("KPIAPI inicializada con todos los componentes complejos")

    async def get_kpi(
        self,
        start_date: datetime,
        end_date: datetime,
        fecha_corte: datetime,
        tipo_reporte: int = 2,
        as_df: bool = False,
    ) -> Union[pd.DataFrame, List[Dict]]:
        """
        Flujo principal completo de KPI:
        1. Obtener colocaciones via webservice
        2. Validar columnas y tipos mínimos
        3. Obtener operaciones fuera del sistema
        4. Enriquecer con operaciones fuera de sistema
        5. Formatear campos y fechas
        6. Obtener datos de referidos
        7. Enriquecer con referidos
        8. Obtener datos de sector pagadores
        9. Calcular métricas financieras
        10. Validación Pydantic y serialización

        Args:
            start_date: Fecha de inicio del período
            end_date: Fecha de fin del período
            fecha_corte: Fecha de corte para el cálculo
            tipo_reporte: Tipo de reporte (0=acumulado, 2=normal)
            as_df: Si True devuelve DataFrame, si False lista de dicts

        Returns:
            DataFrame o lista de diccionarios con KPIs calculados
        """
        logger(
            f"Iniciando cálculo KPI completo: {start_date} a {end_date}, tipo_reporte={tipo_reporte}"
        )

        try:
            # 1. Obtener datos del webservice
            raw_data = await self._client.fetch_colocaciones_data(
                start_date, end_date, fecha_corte, tipo_reporte
            )
            df = pd.DataFrame(raw_data)
            logger(f"Datos obtenidos del webservice: {len(df)} registros")

            # 2. Validar columnas mínimas
            df = self._validator.validar_columnas_minimas(df)
            logger("Validación de columnas mínimas completada")
            
            liq_2510000109_after_ws = df[df['CodigoLiquidacion'] == 'LIQ2510000109']
            logger.info(f"🔍 LIQ2510000109 después WebService: {len(liq_2510000109_after_ws)} registros")
            # 3. Obtener operaciones fuera del sistema
            df_fuera = (
                self._operaciones_fuera_sistema_api.get_operaciones_fuera_sistema(
                    as_df=True
                )
            )

            # 4. Fusionar con operaciones fuera del sistema
            df = await self._enriquecer_operaciones_fuera_sistema(
                df, df_fuera, tipo_reporte
            )
            logger("Enriquecimiento con operaciones fuera del sistema completado")

            # 5. Formatear campos
            df = self._transformer.formatear_campos(df)
            logger("Formateo de campos completado")

            # 6. Obtener datos de referidos
            referidos_df = self._referidos_api.get_referidos(as_df=True)

            # 7. Enriquecer con referidos
            df = await self._enriquecer_referidos(df=df, referidos_df=referidos_df)
            logger("Enriquecimiento con referidos completado")

            # 8. Obtener datos de sector pagadores
            sector_pagadores_df = self._sector_pagadores_api.get_sectores_pagadores(
                as_df=True
            )
            logger("Datos de sector pagadores obtenidos")

            # 9. Calcular KPIs financieros
            df = await self._calcular_metricas_financieras(df, sector_pagadores_df)
            logger("Cálculo de métricas financieras completado")

            # 10. Validación final y serialización
            validated_data = self._validator.validar_schema_kpi(df, tipo_reporte)
            logger(
                f"Validación Pydantic completada: {len(validated_data)} registros válidos"
            )
            
            validated_df = pd.DataFrame(validated_data)
            liq_2510000109_final = validated_df[validated_df['CodigoLiquidacion'] == 'LIQ2510000109']
            logger.info(f"🔍 LIQ2510000109 FINAL: {len(liq_2510000109_final)} registros")
            
            if as_df:
                return pd.DataFrame(validated_data)

            return validated_data

        except Exception as e:
            error_msg = f"Error en cálculo KPI completo: {str(e)}"
            logger(error_msg)
            raise

    async def obtener_datos_raw(
        self,
        start_date: datetime,
        end_date: datetime,
        fecha_corte: datetime,
        tipo_reporte: int = 2,
    ) -> pd.DataFrame:
        """
        Obtiene datos raw del webservice sin procesamiento

        Args:
            start_date: Fecha de inicio
            end_date: Fecha de fin
            fecha_corte: Fecha de corte
            tipo_reporte: Tipo de reporte

        Returns:
            DataFrame con datos raw del webservice
        """
        try:
            logger("Obteniendo datos raw de KPI")

            resultado = await self._engine.obtener_datos_raw(
                start_date, end_date, fecha_corte, tipo_reporte
            )

            logger(f"Datos raw obtenidos: {len(resultado)} registros")
            return resultado

        except Exception as e:
            error_msg = f"Error obteniendo datos raw: {str(e)}"
            logger(error_msg)
            raise

    def validar_datos(self, df: pd.DataFrame) -> bool:
        """
        Valida la integridad de los datos KPI

        Args:
            df: DataFrame a validar

        Returns:
            True si los datos son válidos, False en caso contrario
        """
        try:
            logger("Validando integridad de datos KPI")

            resultado = self._engine.validar_integridad_datos(df)

            if resultado:
                logger("Validación de datos completada exitosamente")
            else:
                logger("FALLO en validación de datos")

            return resultado

        except Exception as e:
            logger(f"Error en validación de datos: {str(e)}")
            return False

    def obtener_resumen(self, df: pd.DataFrame) -> None:
        """
        Genera un resumen detallado de los datos KPI

        Args:
            df: DataFrame con datos KPI
        """
        try:
            logger("Generando resumen de datos KPI")
            self._engine.obtener_resumen_kpi(df)

        except Exception as e:
            logger(f"Error generando resumen: {str(e)}")

    def obtener_resumen_kpi(self, df: pd.DataFrame) -> None:
        """Obtiene resumen específico de datos KPI usando el Engine simple"""
        self._engine.obtener_resumen_kpi(df)

    async def _enriquecer_operaciones_fuera_sistema(
        self, df: pd.DataFrame, df_fuera: pd.DataFrame, tipo_reporte: int = 2
    ) -> pd.DataFrame:
        """Enriquece con datos de operaciones fuera del sistema"""
        try:
            # Fusionar usando el transformer
            df_enriquecido = self._transformer.fusionar_operaciones_fuera_sistema(
                df, df_fuera, tipo_reporte
            )

            logger(
                f"Enriquecimiento fuera del sistema: {len(df)} → {len(df_enriquecido)} registros"
            )
            return df_enriquecido

        except Exception as e:
            logger(f"Error enriqueciendo operaciones fuera del sistema: {str(e)}")
            # En caso de error, devolver datos originales
            return df.assign(FueraSistema="no")

    async def _enriquecer_referidos(
        self, df: pd.DataFrame, referidos_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Enriquece con datos de referidos (método sincrónico)"""
        return self._comisiones_engine.calcular_referidos(
            referidos_df=referidos_df, kpi_df=df
        )

    async def _calcular_metricas_financieras(
        self, df: pd.DataFrame, sector_pagadores_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Calcula métricas financieras usando otros engines"""
        try:

            # Calcular KPIs financieros
            df_con_kpis = self._transformer.calcular_kpis_financieros(
                df, self.tipo_cambio_df, sector_pagadores_df
            )

            logger(f"Métricas financieras calculadas para {len(df_con_kpis)} registros")
            return df_con_kpis

        except Exception as e:
            error_msg = f"Error calculando métricas financieras: {str(e)}"
            logger(error_msg)
            raise


# Instancia global para uso conveniente
# Nota: El tipo_cambio_df debe ser proporcionado al usar la instancia
kpi_api = None


# Funciones de conveniencia para uso directo
async def get_kpi(
    tipo_cambio_df: pd.DataFrame,
    start_date: datetime,
    end_date: datetime,
    fecha_corte: datetime,
    tipo_reporte: int = 2,
    as_df: bool = False,
) -> Union[pd.DataFrame, List[Dict]]:
    """
    Función de conveniencia para calcular KPIs directamente

    Usage:
        resultado = await toolbox.kpi.get_kpi(tipo_cambio_df, start_date, end_date, fecha_corte)
    """
    api = KPIAPI(tipo_cambio_df)
    return await api.get_kpi(start_date, end_date, fecha_corte, tipo_reporte, as_df)
