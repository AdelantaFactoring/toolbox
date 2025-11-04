"""
🔄 Liquidaciones Transformer - Transformaciones para datos de liquidaciones
"""

import pandas as pd
from typing import Dict, Any, List

try:
    from ...core.base_transformer import BaseTransformer
except ImportError:
    class BaseTransformer:
        def __init__(self): pass

class LiquidacionesTransformer(BaseTransformer):
    """Transformer especializado para datos de liquidaciones"""

    def __init__(self):
        super().__init__()

    def preparar_datos_webservice(self, raw_data: List[Dict[str, Any]]) -> pd.DataFrame:
        """Prepara datos crudos del webservice para procesamiento"""
        df = pd.DataFrame(raw_data)
        
        # Normalizar nombres de columnas
        if 'codigo_liquidacion' in df.columns:
            df.rename(columns={'codigo_liquidacion': 'CodigoLiquidacion'}, inplace=True)
        if 'tipo_pago' in df.columns:
            df.rename(columns={'tipo_pago': 'TipoPago'}, inplace=True)
        if 'fecha_confirmado' in df.columns:
            df.rename(columns={'fecha_confirmado': 'FechaConfirmado'}, inplace=True)
        if 'neto_confirmado' in df.columns:
            df.rename(columns={'neto_confirmado': 'NetoConfirmado'}, inplace=True)
        if 'monto_pago' in df.columns:
            df.rename(columns={'monto_pago': 'MontoPago'}, inplace=True)
        if 'saldo_deuda' in df.columns:
            df.rename(columns={'saldo_deuda': 'SaldoDeuda'}, inplace=True)
        
        # Convertir fechas
        if 'FechaConfirmado' in df.columns:
            df['FechaConfirmado'] = pd.to_datetime(df['FechaConfirmado'], errors='coerce')
        
        # Convertir montos numéricos
        montos_cols = ['NetoConfirmado', 'MontoPago', 'SaldoDeuda']
        for col in montos_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df

    def aplicar_formato_powerbi(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplica formato final para Power BI"""
        # Mantener columnas relevantes para Power BI
        columnas_base = [
            'CodigoLiquidacion', 'TipoPago', 'FechaConfirmado', 
            'NetoConfirmado', 'MontoPago', 'SaldoDeuda'
        ]
        
        # Agregar columnas calculadas si existen
        columnas_calculadas = [
            'TipoPago_Real', 'Estado_Cuenta', 'Estado_Real', 'Saldo_Total'
        ]
        
        columnas_finales = columnas_base + [col for col in columnas_calculadas if col in df.columns]
        
        # Mantener solo columnas existentes
        columnas_existentes = [col for col in columnas_finales if col in df.columns]
        
        return df[columnas_existentes].copy()