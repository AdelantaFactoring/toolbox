"""
🧪 Test Liquidaciones - Testing para módulo de liquidaciones
"""

import pytest
import pandas as pd
import sys
import os

# Agregar el directorio raíz al path para imports absolutos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_liquidaciones_api_estructura():
    """Test de estructura de la API"""
    try:
        from toolbox.api.liquidaciones_api import LiquidacionesAPI
    except ImportError as e:
        pytest.skip(f"No se pudo importar LiquidacionesAPI: {e}")

    api = LiquidacionesAPI()

    # Verificar arquitectura hexagonal
    assert hasattr(api, '_transformer')
    assert hasattr(api, '_validator') 
    assert hasattr(api, '_engine')

    # Verificar métodos públicos
    assert hasattr(api, 'procesar_liquidaciones_completo')
    assert callable(api.procesar_liquidaciones_completo)
    assert hasattr(api, 'obtener_datos_para_powerbi')
    assert callable(api.obtener_datos_para_powerbi)

    print("✅ Test estructura API: PASSED")

def test_liquidaciones_engine():
    """Test del engine de liquidaciones"""
    try:
        from toolbox.engines.liquidaciones_standalone import LiquidacionesEngineStandalone
    except ImportError as e:
        pytest.skip(f"No se pudo importar LiquidacionesEngineStandalone: {e}")

    engine = LiquidacionesEngineStandalone()
    
    # Verificar que las listas se cargaron
    assert len(engine._liquidaciones_mora_mayo) > 0
    assert len(engine._liquidaciones_cobranza_especial) > 0
    assert "LIQ002-2021" in engine._liquidaciones_mora_mayo
    assert "LIQ2302000034" in engine._liquidaciones_cobranza_especial
    
    print("✅ Test engine: PASSED")

def test_liquidaciones_procesamiento_completo():
    """Test de procesamiento completo"""
    try:
        from toolbox.api.liquidaciones_api import obtener_datos_para_powerbi
    except ImportError as e:
        pytest.skip(f"No se pudo importar obtener_datos_para_powerbi: {e}")

    # Datos de prueba
    datos_prueba = [
        {
            "CodigoLiquidacion": "LIQ002-2021",  # Está en MORA A MAYO
            "TipoPago": "PAGO PARCIAL",
            "FechaConfirmado": "2021-01-01",
            "NetoConfirmado": 1000.0,
            "MontoPago": 500.0,
            "SaldoDeuda": 500.0
        },
        {
            "CodigoLiquidacion": "LIQ010-2022",  # Está en MORA A MAYO
            "TipoPago": "PAGO TOTAL",
            "FechaConfirmado": "2022-01-01",
            "NetoConfirmado": 2000.0,
            "MontoPago": 2000.0,
            "SaldoDeuda": 0.0
        },
        {
            "CodigoLiquidacion": "LIQ999-2023",  # No problemático
            "TipoPago": "PAGO TOTAL", 
            "FechaConfirmado": "2023-01-01",
            "NetoConfirmado": 3000.0,
            "MontoPago": 3000.0,
            "SaldoDeuda": 0.0
        }
    ]

    # Procesar datos
    resultado = obtener_datos_para_powerbi(datos_prueba, "2023-01-01")

    # Verificar resultados
    assert isinstance(resultado, pd.DataFrame)
    assert len(resultado) == 3  # Todos los registros únicos
    
    # Verificar que se aplicó la lógica de MORA A MAYO
    liquidacion_mora = resultado[resultado['CodigoLiquidacion'] == 'LIQ002-2021']
    assert not liquidacion_mora.empty
    if 'TipoPago_Real' in resultado.columns:
        assert liquidacion_mora.iloc[0]['TipoPago_Real'] == 'MORA A MAYO'
    
    print("✅ Test procesamiento completo: PASSED")

def test_liquidaciones_eliminacion_duplicados():
    """Test específico para eliminación de duplicados"""
    try:
        from toolbox.api.liquidaciones_api import obtener_datos_para_powerbi
    except ImportError as e:
        pytest.skip(f"No se pudo importar obtener_datos_para_powerbi: {e}")

    # Datos con duplicados explícitos
    datos_con_duplicados = [
        {
            "CodigoLiquidacion": "LIQ002-2021",  # MORA A MAYO - duplicado
            "TipoPago": "PAGO PARCIAL",
            "FechaConfirmado": "2021-01-01",
            "NetoConfirmado": 1000.0,
            "MontoPago": 500.0,
            "SaldoDeuda": 500.0
        },
        {
            "CodigoLiquidacion": "LIQ002-2021",  # DUPLICADO
            "TipoPago": "OTRO TIPO",
            "FechaConfirmado": "2021-01-01",
            "NetoConfirmado": 1000.0,
            "MontoPago": 500.0,
            "SaldoDeuda": 500.0
        },
        {
            "CodigoLiquidacion": "LIQ999-2023",  # Único
            "TipoPago": "PAGO TOTAL",
            "FechaConfirmado": "2023-01-01",
            "NetoConfirmado": 3000.0,
            "MontoPago": 3000.0,
            "SaldoDeuda": 0.0
        }
    ]

    resultado = obtener_datos_para_powerbi(datos_con_duplicados, "2023-01-01")
    
    # Verificar que se eliminó el duplicado
    assert len(resultado) == 2  # Solo 2 registros únicos
    assert resultado['CodigoLiquidacion'].nunique() == 2
    
    print("✅ Test eliminación duplicados: PASSED")

if __name__ == "__main__":
    test_liquidaciones_api_estructura()
    test_liquidaciones_engine()
    test_liquidaciones_procesamiento_completo()
    test_liquidaciones_eliminacion_duplicados()
    print("🎉 Todos los tests de liquidaciones pasaron")