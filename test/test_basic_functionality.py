"""
🧪 Tests básicos de funcionalidad - Sin imports complejos
Tests mínimos para verificar que el entorno funciona correctamente.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path


class TestBasicFunctionality:
    """Tests básicos de funcionalidad del proyecto."""

    def test_basic_imports(self):
        """Test que las dependencias básicas se puedan importar"""
        # Test pandas
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        assert len(df) == 3
        assert list(df.columns) == ["a", "b"]

        # Test numpy
        arr = np.array([1, 2, 3])
        assert len(arr) == 3
        assert arr.sum() == 6

        print("✅ Test basic imports: PASSED")

    def test_project_structure(self):
        """Test que la estructura del proyecto sea correcta"""
        project_root = Path(__file__).parent.parent

        # Verificar directorios principales
        assert (project_root / "toolbox").exists(), "Directorio toolbox debe existir"
        assert (project_root / "test").exists(), "Directorio test debe existir"
        assert (project_root / "pyproject.toml").exists(), "pyproject.toml debe existir"

        # Verificar __init__.py files
        assert (
            project_root / "toolbox" / "__init__.py"
        ).exists(), "toolbox/__init__.py debe existir"

        print("✅ Test project structure: PASSED")

    def test_data_processing_basic(self, sample_data):
        """Test procesamiento básico de datos usando fixture"""
        assert sample_data["codigo"] == "TEST001"
        assert sample_data["monto"] == 1000.0
        assert sample_data["moneda"] == "PEN"

        # Test procesamiento básico
        df = pd.DataFrame([sample_data])
        assert len(df) == 1
        assert df["monto"].sum() == 1000.0

        print("✅ Test data processing basic: PASSED")

    def test_environment_setup(self):
        """Test que el entorno esté configurado correctamente"""
        # Test que pytest esté funcionando
        assert True

        # Test que podemos usar Path
        current_path = Path(__file__)
        assert current_path.exists()

        # Test matemáticas básicas
        result = 2 + 2
        assert result == 4

        print("✅ Test environment setup: PASSED")


# Tests funcionales independientes
def test_standalone_functionality():
    """Test independiente de funcionalidad"""
    data = {"test": "value", "number": 42}
    assert data["test"] == "value"
    assert data["number"] == 42
    print("✅ Test standalone functionality: PASSED")


@pytest.mark.unit
def test_unit_example():
    """Ejemplo de test unitario marcado"""
    assert 1 + 1 == 2
    print("✅ Test unit example: PASSED")
