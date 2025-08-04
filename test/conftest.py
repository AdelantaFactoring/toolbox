"""
🧪 Conftest V2 - Configuración optimizada para tests
Configuración centralizada para pytest con fixtures útiles y setup del entorno.
"""

import pytest
import sys
from pathlib import Path

# Configuración de paths para imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


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
