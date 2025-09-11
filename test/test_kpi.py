"""
🧪 Test KPI V2 - Test limpio usando configuración automática

Test para la función de conveniencia get_kpi con configuración automática desde conftest.py
"""

import pytest
import pandas as pd
from datetime import datetime
import asyncio

# Importación limpia sin configuración hardcodeada
try:
    from toolbox.api.kpi_api import get_kpi
    from toolbox.config.settings import V2Settings

    print(
        "✅ Toolbox importado correctamente - configuración automática desde conftest.py"
    )

except ImportError as e:
    print(f"Error: No se pudo importar dependencias: {e}")
    get_kpi = None


def crear_datos_tipo_cambio_mock():
    """Crea datos de prueba para tipo de cambio"""
    fechas = pd.date_range("2024-01-01", "2024-12-31", freq="D")
    return pd.DataFrame(
        {
            "TipoCambioFecha": fechas,
            "TipoCambioVenta": [3.8 + (i % 10) * 0.01 for i in range(len(fechas))],
            "TipoCambioCompra": [3.7 + (i % 10) * 0.01 for i in range(len(fechas))],
        }
    )


@pytest.mark.asyncio
async def test_get_kpi_function():
    """
    Test específico para la función get_kpi con configuración real

    Verifica que la función de conveniencia get_kpi funcione con datos reales
    """

    if get_kpi is None:
        pytest.skip("get_kpi no disponible - problema de importación")

    try:
        print("🧪 Iniciando test KPI con configuración automática...")
        print(f"🌐 URL Webservice: {V2Settings.get_webservice_base_url()}")
        print(f"👤 Usuario KPI: {V2Settings.get_kpi_credentials()['username']}")

        # Preparar datos de prueba - fechas más recientes y realistas
        tipo_cambio_df = crear_datos_tipo_cambio_mock()
        start_date = datetime(2019, 7, 1)
        end_date = datetime(2025, 9, 11)
        fecha_corte = datetime(2025, 9, 11)

        print("📍 Iniciando test de función get_kpi...")
        print(f"📅 Fechas: {start_date} a {end_date}")
        print(f"📊 Tipo cambio DF shape: {tipo_cambio_df.shape}")

        # Llamar función con as_df=True
        print("🔄 Test: Llamando get_kpi con credenciales reales...")
        resultado_df = await get_kpi(
            tipo_cambio_df=tipo_cambio_df,
            start_date=start_date,
            end_date=end_date,
            fecha_corte=fecha_corte,
            tipo_reporte=2,
            as_df=True,
        )

        # Guardar resultado
        output_file = "test_kpi_resultado_real.xlsx"
        resultado_df.to_excel(output_file, index=False)
        print(f"📁 Resultado guardado en: {output_file}")

        print(f"✅ Test completado. Tipo resultado: {type(resultado_df)}")
        print(f"📊 Shape del resultado: {resultado_df.shape}")

        if len(resultado_df) > 0:
            print(f"📋 Columnas: {list(resultado_df.columns)}")
            print("🎯 Primeras 3 filas:")
            print(resultado_df.head(3).to_string())

        # Verificar que retorna DataFrame
        assert isinstance(resultado_df, pd.DataFrame)
        print("✅ Test función get_kpi con datos reales: PASSED")
        return True

    except Exception as e:
        print(f"❌ Test función get_kpi: FAILED - {e}")
        print(f"🔍 Tipo de error: {type(e)}")
        import traceback

        print("🔍 Traceback completo:")
        traceback.print_exc()

        # Análisis específico del error
        if "can't be used in 'await' expression" in str(e):
            print("🚨 Error: El objeto no es awaitable - problema en la implementación")
        elif "401" in str(e) or "Unauthorized" in str(e):
            print("🔐 Error de autenticación - verificar credenciales")
        elif "timeout" in str(e).lower():
            print("⏰ Error de timeout - servidor demoró mucho")
        elif "connection" in str(e).lower():
            print("🌐 Error de conexión - verificar URL del webservice")

        # Para test continuar, solo hacemos skip si es error de configuración
        pytest.fail(f"Test falló con error: {e}")


if __name__ == "__main__":
    # Ejecutar test directamente
    import asyncio

    asyncio.run(test_get_kpi_function())
