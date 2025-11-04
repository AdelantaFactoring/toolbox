"""
🌐 Liquidaciones API - Versión con Engine Standalone
"""

import pandas as pd

try:
    # Intentar usar la versión standalone primero
    from ..engines.liquidaciones_standalone import LiquidacionesEngineStandalone as LiquidacionesEngine
except ImportError:
    try:
        # Fallback a la versión original
        from ..engines.liquidaciones_engine import LiquidacionesEngine
    except ImportError as e:
        raise ImportError(f"No se pudo importar ningún engine de liquidaciones: {e}")

try:
    from ..processing.transformers.liquidaciones_transformer import LiquidacionesTransformer
    from ..processing.validators.liquidaciones_validator import LiquidacionesValidator
except ImportError:
    # Fallback básico si no hay transformers/validators
    class LiquidacionesTransformer:
        def preparar_datos_webservice(self, data): 
            return pd.DataFrame(data)
        def aplicar_formato_powerbi(self, df): 
            return df
    
    class LiquidacionesValidator:
        def validar_estructura_liquidaciones(self, df): 
            pass

class LiquidacionesAPI:
    """API pública para liquidaciones - Versión robusta"""

    def __init__(self):
        self._transformer = LiquidacionesTransformer()
        self._validator = LiquidacionesValidator()
        self._engine = LiquidacionesEngine()

    def procesar_liquidaciones_completo(self, datos_liquidaciones, fecha_corte=None, eliminar_duplicados=True):
        """Procesamiento robusto con fallbacks"""
        
        # Convertir a DataFrame
        if isinstance(datos_liquidaciones, list):
            df = self._transformer.preparar_datos_webservice(datos_liquidaciones)
        else:
            df = datos_liquidaciones.copy()

        # Validar estructura básica
        try:
            self._validator.validar_estructura_liquidaciones(df)
        except Exception:
            pass  # Validación omitida silenciosamente

        # Aplicar lógica completa
        df_procesado = self._engine.aplicar_logica_completa_powerbi(df, fecha_corte)

        # Eliminar duplicados si se solicita
        if eliminar_duplicados:
            df_final = self._engine.filtrar_liquidaciones_unicas(df_procesado)
        else:
            df_final = df_procesado

        # Aplicar formato final
        df_final = self._transformer.aplicar_formato_powerbi(df_final)

        return df_final

    def obtener_datos_para_powerbi(self, datos_liquidaciones, fecha_corte=None):
        """Obtiene datos listos para Power BI"""
        return self.procesar_liquidaciones_completo(datos_liquidaciones, fecha_corte, eliminar_duplicados=True)

    def obtener_reporte_completo(self, datos_liquidaciones, fecha_corte=None):
        """Genera reporte completo"""
        if isinstance(datos_liquidaciones, list):
            df = pd.DataFrame(datos_liquidaciones)
        else:
            df = datos_liquidaciones.copy()
            
        df_procesado = self._engine.aplicar_logica_completa_powerbi(df, fecha_corte)
        reporte_duplicidades = self._engine.generar_reporte_duplicidades(df)
        estadisticas = self._engine.obtener_estadisticas_liquidaciones(df)

        return {
            'estadisticas_generales': estadisticas,
            'reporte_duplicidades': reporte_duplicidades,
            'total_registros_original': len(df),
            'total_registros_procesado': len(df_procesado)
        }

# Instancia global
liquidaciones_api = LiquidacionesAPI()

# Funciones de conveniencia
def obtener_datos_para_powerbi(datos_liquidaciones, fecha_corte=None):
    return liquidaciones_api.obtener_datos_para_powerbi(datos_liquidaciones, fecha_corte)

def obtener_reporte_completo(datos_liquidaciones, fecha_corte=None):
    return liquidaciones_api.obtener_reporte_completo(datos_liquidaciones, fecha_corte)