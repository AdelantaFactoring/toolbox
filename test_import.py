"""
Test simple para verificar que la importación funciona correctamente
"""

print("🧪 Iniciando test de importación...")

try:
    print("1️⃣ Importando toolbox...")
    import toolbox

    print("✅ Importación exitosa!")

    print("2️⃣ Creando configuración de prueba...")
    TOOLBOX_CONFIG = {
        "WEBSERVICE_BASE_URL": "https://test.com",
        "KPI_CREDENTIALS": {"username": "test", "password": "test"},
        "GOOGLE_SHEETS_URLS": {
            "referidos": "https://sheets.googleapis.com/test1",
            "fondo_promocional": "https://sheets.googleapis.com/test2",
            "fondo_crecer": "https://sheets.googleapis.com/test3",
            "sector_pagadores": "https://sheets.googleapis.com/test4",
        },
        "INTERESES_PEN": 0.12,
        "INTERESES_USD": 0.08,
    }

    print("3️⃣ Configurando toolbox...")
    toolbox.configure(TOOLBOX_CONFIG)
    print("✅ Configuración exitosa!")

    print("4️⃣ Verificando acceso a configuración...")
    # Esto debería funcionar ahora
    from toolbox.io.referidos_client import ReferidosClient

    client = ReferidosClient()
    url = client.url  # Esto ahora usa lazy loading
    print(f"✅ URL obtenida: {url}")

    print("🎉 TODAS LAS PRUEBAS PASARON!")

except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback

    traceback.print_exc()
