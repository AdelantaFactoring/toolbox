"""
🧪 Test de importaciones V2 - Verificación básica
"""

import pytest
import sys
import os

# Agregar el directorio padre al path para las importaciones
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


def test_package_structure():
    """Test que la estructura del paquete sea correcta"""
    # Verificar que existe __init__.py principal
    init_file = os.path.join(parent_dir, "__init__.py")
    assert os.path.exists(init_file), "__init__.py principal debe existir"

    # Verificar que existe toolbox
    toolbox_dir = os.path.join(parent_dir, "toolbox")
    assert os.path.exists(toolbox_dir), "Directorio toolbox debe existir"

    # Verificar que existe __init__.py de toolbox
    toolbox_init = os.path.join(toolbox_dir, "__init__.py")
    assert os.path.exists(toolbox_init), "toolbox/__init__.py debe existir"

    print("✅ Test estructura del paquete: PASSED")


def test_toolbox_import():
    """Test que la toolbox se pueda importar"""
    try:
        from toolbox.api import fondo_promocional_api

        assert fondo_promocional_api is not None
        print("✅ Test import toolbox.api.fondo_promocional_api: PASSED")
    except ImportError as e:
        pytest.fail(f"No se pudo importar toolbox.api.fondo_promocional_api: {e}")


def test_fondos_api_functions():
    """Test que las funciones de fondos se puedan importar"""
    try:
        from toolbox.api.fondo_promocional_api import (
            get_fondo_promocional,
            FondoPromocionalAPI,
        )
        from toolbox.api.fondo_crecer_api import (
            get_fondo_crecer,
            FondoCrecerAPI,
        )

        # Verificar que las funciones son callable
        assert callable(get_fondo_promocional)
        assert callable(get_fondo_crecer)
        assert FondoPromocionalAPI is not None
        assert FondoCrecerAPI is not None

        print("✅ Test import fondos functions: PASSED")
    except ImportError as e:
        pytest.fail(f"No se pudo importar funciones fondos: {e}")


def test_main_package_import():
    """Test que el paquete principal se pueda importar desde __init__.py"""
    try:
        # Importar desde el __init__.py principal
        import sys

        sys.path.insert(0, parent_dir)

        # Test importación directa
        from toolbox import get_fondo_promocional, get_fondo_crecer

        assert callable(get_fondo_promocional)
        assert callable(get_fondo_crecer)

        print("✅ Test import desde __init__.py principal: PASSED")
    except ImportError as e:
        pytest.fail(f"No se pudo importar desde __init__.py principal: {e}")


def test_apis_availability():
    """Test que los APIs estén disponibles"""
    api_modules = [
        "comisiones_api",
        "fondo_crecer_api",
        "fondo_promocional_api",
        "ventas_autodetracciones_api",
    ]

    available_modules = []
    for module in api_modules:
        try:
            exec(f"from toolbox.api import {module}")
            available_modules.append(module)
        except ImportError as e:
            print(f"⚠️ {module} no disponible: {e}")

    print(f"✅ Módulos API disponibles: {available_modules}")
    assert len(available_modules) >= 2, "Al menos 2 módulos API deben estar disponibles"


if __name__ == "__main__":
    test_package_structure()
    test_toolbox_import()
    test_fondos_api_functions()
    test_main_package_import()
    test_apis_availability()
    print("🎉 Todos los tests de importación completados")
