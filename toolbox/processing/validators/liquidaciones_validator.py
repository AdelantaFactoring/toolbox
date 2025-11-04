"""
✅ Liquidaciones Validator - Validación para datos de liquidaciones
"""

import pandas as pd

try:
    from ...core.base_validator import BaseValidator
    from ...schemas.liquidaciones_schema import LiquidacionSchema
    from ...config.settings import V2Settings
except ImportError:
    class BaseValidator:
        def __init__(self, schema_class=None): 
            self.schema_class = schema_class

    class LiquidacionSchema:
        pass

    class V2Settings:
        @staticmethod
        def logger(msg): print(f"LOG: {msg}")

class LiquidacionesValidator(BaseValidator):
    """Validador especializado para liquidaciones"""

    _cols_requeridas = ["CodigoLiquidacion"]

    def __init__(self):
        super().__init__(schema_class=LiquidacionSchema)

    def validar_estructura_liquidaciones(self, df: pd.DataFrame):
        """Valida la estructura básica del DataFrame"""
        if df.empty:
            raise ValueError("DataFrame de liquidaciones está vacío")
        
        missing_cols = set(self._cols_requeridas) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Columnas requeridas faltantes: {missing_cols}")

    def validar_integridad_datos(self, df: pd.DataFrame):
        """Valida la integridad de los datos"""
        # Verificar que no hay códigos de liquidación nulos
        if df['CodigoLiquidacion'].isnull().any():
            V2Settings.logger("Advertencia: Hay códigos de liquidación nulos")
        
        # Verificar duplicados antes de procesar
        duplicados = df['CodigoLiquidacion'].duplicated().sum()
        if duplicados > 0:
            V2Settings.logger(f"Se detectaron {duplicados} códigos duplicados antes de procesar")