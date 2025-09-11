"""
🧪 Conftest V2 - Configuración automática con test_settings.py
Configuración centralizada para pytest con inicialización automática del toolbox.
"""

import pytest
import sys
import os
from pathlib import Path

# Configuración de paths para imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# También agregar al PYTHONPATH para mayor compatibilidad
os.environ["PYTHONPATH"] = (
    str(project_root) + os.pathsep + os.environ.get("PYTHONPATH", "")
)

# Importar configuración de test y toolbox después de configurar paths
from test_settings import test_settings
from toolbox.config.settings import V2Settings


@pytest.fixture(autouse=True)
def auto_configure_toolbox():
    """
    Configuración automática del toolbox usando test_settings.py
    Se ejecuta automáticamente antes de cada test
    """
    try:
        # Convertir test_settings a formato toolbox
        config = test_settings.to_toolbox_config()

        # Inicializar V2Settings con la configuración
        V2Settings.initialize(config)

        print("✅ Toolbox configurado automáticamente desde test_settings.py")

    except Exception as e:
        print(f"❌ Error configurando toolbox: {e}")
        raise

    yield

    # Cleanup después del test si es necesario
    pass


@pytest.fixture
def sample_data():
    """Datos de prueba simples para tests básicos"""
    return {
        "codigo": "TEST001",
        "monto": 1000.0,
        "moneda": "PEN",
        "fecha": "2024-01-01",
        "tipo": "test",
    }


@pytest.fixture
def project_root_path():
    """Path raíz del proyecto"""
    return project_root


@pytest.fixture
def toolbox_path():
    """Path del paquete toolbox"""
    return project_root / "toolbox"


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup automático del entorno de test"""
    # Asegurar que el proyecto esté en el path
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    yield

    # Cleanup después del test si es necesario
    pass


# Configuración de marcadores para diferentes tipos de tests
pytest_plugins = []
