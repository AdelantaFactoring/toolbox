"""
🧪 Tests aislados que NO importan toolbox - Solo funcionalidad básica
"""

import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path


def test_basic_python():
    """Test que Python básico funciona"""
    assert 1 + 1 == 2
    assert "hello".upper() == "HELLO"
    assert [1, 2, 3][1] == 2
    print("✅ Python básico: PASSED")


def test_pandas_basic():
    """Test que pandas funciona básicamente"""
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

    assert len(df) == 3
    assert list(df.columns) == ["A", "B"]
    assert df["A"].sum() == 6
    assert df["B"].mean() == 5.0

    print("✅ Pandas básico: PASSED")


def test_numpy_basic():
    """Test que numpy funciona básicamente"""
    arr = np.array([1, 2, 3, 4, 5])

    assert len(arr) == 5
    assert arr.sum() == 15
    assert arr.mean() == 3.0
    assert arr.max() == 5

    print("✅ Numpy básico: PASSED")


def test_pathlib_basic():
    """Test que pathlib funciona"""
    current_file = Path(__file__)

    assert current_file.exists()
    assert current_file.name == "test_isolated.py"
    assert current_file.suffix == ".py"

    # Test directorio del proyecto
    project_root = current_file.parent.parent
    assert project_root.exists()

    print("✅ Pathlib básico: PASSED")


def test_project_files_exist():
    """Test que los archivos del proyecto existen (sin importarlos)"""
    project_root = Path(__file__).parent.parent

    # Archivos que deben existir
    required_files = ["pyproject.toml", "README.md", "toolbox/__init__.py"]

    for file_path in required_files:
        full_path = project_root / file_path
        assert full_path.exists(), f"Archivo requerido no encontrado: {file_path}"

    print("✅ Archivos del proyecto existen: PASSED")


def test_python_version():
    """Test que estamos usando una versión soportada de Python"""
    assert sys.version_info.major == 3
    assert sys.version_info.minor >= 8, "Requiere Python 3.8 o superior"

    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}: PASSED")


def test_fixture_usage(sample_data):
    """Test usando fixture del conftest (sin imports de toolbox)"""
    assert isinstance(sample_data, dict)
    assert "codigo" in sample_data
    assert sample_data["codigo"] == "TEST001"
    assert sample_data["monto"] == 1000.0

    print("✅ Fixture usage: PASSED")


@pytest.mark.unit
def test_simple_calculation():
    """Test de cálculo simple"""
    # Test matemáticas básicas
    result = 10 * 2 + 5
    assert result == 25

    # Test con pandas
    df = pd.DataFrame({"values": [1, 2, 3, 4, 5]})
    total = df["values"].sum()
    assert total == 15

    print("✅ Cálculo simple: PASSED")


def test_data_types():
    """Test tipos de datos básicos"""
    # Test string
    text = "adelanta toolbox"
    assert isinstance(text, str)
    assert text.title() == "Adelanta Toolbox"

    # Test list
    numbers = [1, 2, 3]
    assert isinstance(numbers, list)
    assert len(numbers) == 3

    # Test dict
    data = {"key": "value", "number": 42}
    assert isinstance(data, dict)
    assert data["key"] == "value"

    print("✅ Tipos de datos: PASSED")
