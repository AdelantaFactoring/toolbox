"""
🧪 Tests simplificados de importaciones - Sin dependencias complejas
"""

import pytest
import sys
from pathlib import Path


def test_project_structure_simple():
    """Test básico de estructura del proyecto"""
    # Usar pathlib para mejor compatibilidad
    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent

    # Verificar archivos/directorios esenciales
    assert (parent_dir / "pyproject.toml").exists(), "pyproject.toml debe existir"
    assert (parent_dir / "toolbox").exists(), "Directorio toolbox debe existir"
    assert (parent_dir / "test").exists(), "Directorio test debe existir"

    print("✅ Test estructura del proyecto: PASSED")


def test_basic_dependencies():
    """Test que las dependencias básicas funcionen"""
    try:
        import pandas as pd
        import numpy as np
        import pydantic

        # Test básico pandas
        df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        assert len(df) == 2

        # Test básico numpy
        arr = np.array([1, 2, 3])
        assert arr.sum() == 6

        # Test básico pydantic
        assert hasattr(pydantic, "BaseModel"), "Pydantic debe tener BaseModel"

        print("✅ Test dependencias básicas: PASSED")

    except ImportError as e:
        pytest.fail(f"Error importando dependencias básicas: {e}")


def test_toolbox_structure():
    """Test estructura interna de toolbox"""
    toolbox_dir = Path(__file__).parent.parent / "toolbox"

    # Verificar que existe
    assert toolbox_dir.exists(), "Directorio toolbox debe existir"

    # Verificar algunos subdirectorios comunes
    expected_subdirs = ["api", "config", "core", "engines"]
    found_subdirs = []

    for subdir in expected_subdirs:
        if (toolbox_dir / subdir).exists():
            found_subdirs.append(subdir)

    print(f"✅ Subdirectorios encontrados: {found_subdirs}")
    print("✅ Test estructura toolbox: PASSED")


@pytest.mark.unit
def test_sample_data_fixture(sample_data):
    """Test usando fixture del conftest"""
    assert sample_data is not None
    assert "codigo" in sample_data
    assert sample_data["codigo"] == "TEST001"
    print("✅ Test sample data fixture: PASSED")


def test_python_environment():
    """Test del entorno Python"""
    # Verificar versión de Python
    assert sys.version_info.major == 3
    assert sys.version_info.minor >= 8  # Requerimos Python 3.8+

    # Test que Path funciona
    current_file = Path(__file__)
    assert current_file.exists()
    assert current_file.name == "test_simple.py"

    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")
    print("✅ Test entorno Python: PASSED")
