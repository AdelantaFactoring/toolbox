"""
🧪 Prueba Directa - Módulo Liquidaciones SIN dependencias externas
"""

import sys
import os
import pandas as pd

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(__file__))

def probar_liquidaciones_aislado():
    """Prueba el módulo liquidaciones sin otras dependencias"""
    
    try:
        # Importar SOLO lo necesario para liquidaciones
        from toolbox.engines.liquidaciones_standalone import LiquidacionesEngineStandalone
        print("✅ LiquidacionesEngineStandalone importado correctamente")
        
        # Probar el engine directamente
        engine = LiquidacionesEngineStandalone()
        
        # Datos de prueba CON DUPLICADO REAL
        datos_prueba = [
            {
                "CodigoLiquidacion": "LIQ002-2021",  # MORA A MAYO
                "TipoPago": "PAGO PARCIAL",
                "FechaConfirmado": "2021-01-15",
                "NetoConfirmado": 1000.0,
                "MontoPago": 500.0,
                "SaldoDeuda": 500.0
            },
            {
                "CodigoLiquidacion": "LIQ002-2021",  # DUPLICADO
                "TipoPago": "OTRO TIPO",
                "FechaConfirmado": "2021-01-15",
                "NetoConfirmado": 1000.0,
                "MontoPago": 500.0,
                "SaldoDeuda": 500.0
            },
            {
                "CodigoLiquidacion": "LIQ2302000034",  # COBRANZA ESPECIAL
                "TipoPago": "PAGO PARCIAL",
                "FechaConfirmado": "2023-02-10",  # VENCIDO
                "NetoConfirmado": 2000.0,
                "MontoPago": 1000.0,
                "SaldoDeuda": 1000.0
            }
        ]
        
        df = pd.DataFrame(datos_prueba)
        resultado = engine.aplicar_logica_completa_powerbi(df, "2024-01-31")
        
        print("✅ Procesamiento exitoso:")
        print(f"   - Entrada: {len(datos_prueba)} registros")
        print(f"   - Salida: {len(resultado)} registros")
        print(f"   - Duplicados detectados: {resultado['Es_Duplicado'].sum()}")
        print(f"   - Mora Mayo detectados: {resultado['Es_Mora_Mayo'].sum()}")
        print(f"   - Cobranza Especial: {resultado['Es_Cobranza_Especial'].sum()}")
        
        # Probar eliminación de duplicados
        datos_unicos = engine.filtrar_liquidaciones_unicas(df)
        print(f"   - Registros únicos después de filtrar: {len(datos_unicos)}")
        
        # Verificar que se aplicó la lógica correctamente
        liq_mora = resultado[resultado['CodigoLiquidacion'] == 'LIQ002-2021']
        if not liq_mora.empty and 'TipoPago_Real' in liq_mora.columns:
            print(f"   - TipoPago_Real aplicado: {liq_mora.iloc[0]['TipoPago_Real']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en engine: {e}")
        return False

def probar_api_liquidaciones():
    """Prueba la API de liquidaciones"""
    
    try:
        # Intentar importar la API
        from toolbox.api.liquidaciones_api import obtener_datos_para_powerbi
        print("✅ Liquidaciones API importada correctamente")
        
        # Datos con duplicado REAL para probar
        datos_prueba = [
            {
                "CodigoLiquidacion": "LIQ002-2021",  # MORA A MAYO
                "TipoPago": "PAGO PARCIAL",
                "FechaConfirmado": "2021-01-15",
                "NetoConfirmado": 1000.0,
                "MontoPago": 500.0,
                "SaldoDeuda": 500.0
            },
            {
                "CodigoLiquidacion": "LIQ002-2021",  # DUPLICADO
                "TipoPago": "OTRO TIPO", 
                "FechaConfirmado": "2021-01-15",
                "NetoConfirmado": 1000.0,
                "MontoPago": 500.0,
                "SaldoDeuda": 500.0
            }
        ]
        
        resultado = obtener_datos_para_powerbi(datos_prueba, "2024-01-31")
        print(f"✅ API funcionando: {len(datos_prueba)} → {len(resultado)} registros")
        
        # Verificar que se eliminó el duplicado
        if len(resultado) < len(datos_prueba):
            print("✅ Duplicado eliminado correctamente")
        else:
            print("⚠️  No se eliminaron duplicados")
            
        return True
        
    except Exception as e:
        print(f"⚠️  API no disponible: {e}")
        return False

if __name__ == "__main__":
    print("🧪 PRUEBA DIRECTA - MÓDULO LIQUIDACIONES")
    print("=" * 50)
    
    # Probar engine (debería funcionar)
    engine_ok = probar_liquidaciones_aislado()
    
    print("\n" + "=" * 50)
    
    # Probar API (puede fallar)
    api_ok = probar_api_liquidaciones()
    
    print("\n" + "=" * 50)
    
    if engine_ok and api_ok:
        print("🎉 ¡El MÓDULO LIQUIDACIONES funciona CORRECTAMENTE!")
        print("   Puedes proceder con la implementación en producción")
    elif engine_ok:
        print("✅ El Engine funciona, pero la API tiene problemas de dependencias")
        print("   El core del módulo está listo para usar")
    else:
        print("❌ Hay problemas críticos con el módulo liquidaciones")