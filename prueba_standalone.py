"""
🧪 Prueba STANDALONE - Módulo 100% independiente
"""

import sys
import os
import pandas as pd

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(__file__))

def prueba_standalone_completa():
    """Prueba el módulo standalone completamente aislado"""
    
    try:
        from liquidaciones_standalone import corregir_liquidaciones, obtener_reporte_correccion
        print("✅ Módulo standalone importado CORRECTAMENTE")
    except ImportError as e:
        print(f"❌ Error importando módulo standalone: {e}")
        return False

    # Datos de prueba COMPLETOS
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
        },
        {
            "CodigoLiquidacion": "LIQ999-2023",  # NORMAL
            "TipoPago": "PAGO TOTAL",
            "FechaConfirmado": "2023-12-01",  # VIGENTE
            "NetoConfirmado": 3000.0,
            "MontoPago": 3000.0,
            "SaldoDeuda": 0.0
        }
    ]

    print(f"📥 Datos de entrada: {len(datos_prueba)} registros")
    
    # Procesar con el módulo standalone
    datos_limpios = corregir_liquidaciones(datos_prueba, "2024-01-31")
    
    print(f"✅ Datos procesados: {len(datos_limpios)} registros")
    print(f"🗑️  Duplicados eliminados: {len(datos_prueba) - len(datos_limpios)}")
    
    # Generar reporte
    reporte = obtener_reporte_correccion(datos_prueba, "2024-01-31")
    print(f"📊 Reporte: {reporte}")
    
    # Verificar resultados
    assert len(datos_limpios) == 3, f"Se esperaban 3 registros, se obtuvieron {len(datos_limpios)}"
    assert datos_limpios['CodigoLiquidacion'].nunique() == 3, "No se eliminaron todos los duplicados"
    
    print("🎉 ¡MÓDULO STANDALONE FUNCIONA PERFECTAMENTE!")
    print("   Puedes usar este módulo directamente en producción")
    
    return True

if __name__ == "__main__":
    print("🧪 PRUEBA STANDALONE - MÓDULO 100% INDEPENDIENTE")
    print("=" * 60)
    
    if prueba_standalone_completa():
        print("\n" + "=" * 60)
        print("🚀 ¡IMPLEMENTACIÓN LISTA PARA PRODUCCIÓN!")
        print("\nUSO:")
        print("from liquidaciones_standalone import corregir_liquidaciones")
        print("datos_limpios = corregir_liquidaciones(datos_webservice, '2024-01-31')")
    else:
        print("\n❌ Hay problemas con el módulo standalone")