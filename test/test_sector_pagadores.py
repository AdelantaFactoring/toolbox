"""
🧪 Test Sector Pagadores V2 - Compatibilidad V1
"""

import pytest
import pandas as pd


def test_sector_pagadores_v2_basic():
    """Test que V2 tiene misma interfaz que V1"""
    try:
        from ..api.sector_pagadores_api import SectorPagadoresAPI
    except ImportError:
        pytest.skip("No se pudo importar SectorPagadoresAPI")

    # Constructor igual que V1 (sin parámetros)
    sector_pagadores_api = SectorPagadoresAPI()

    # Verificar interfaz idéntica a V1
    assert hasattr(sector_pagadores_api, "validar_datos")
    assert callable(sector_pagadores_api.validar_datos)

    assert hasattr(sector_pagadores_api, "procesar_datos")
    assert callable(sector_pagadores_api.procesar_datos)

    assert hasattr(sector_pagadores_api, "calcular")
    assert callable(sector_pagadores_api.calcular)

    assert hasattr(sector_pagadores_api, "calcular_df")
    assert callable(sector_pagadores_api.calcular_df)

    # Verificar arquitectura hexagonal
    assert hasattr(sector_pagadores_api, "_engine")
    assert hasattr(sector_pagadores_api, "_client")
    assert hasattr(sector_pagadores_api, "_transformer")
    assert hasattr(sector_pagadores_api, "_validator")

    # Test funcional básico con datos mock
    mock_data = {
        "RUC": ["12345678901", "98765432109"],
        "SECTOR": ["  Retail  ", "  Manufacturing  "],
        "GRUPO ECO.": ["Grupo A", ""],
    }

    # Test procesar_datos
    df_result = sector_pagadores_api.procesar_datos(mock_data)
    assert isinstance(df_result, pd.DataFrame)
    assert "RUCPagador" in df_result.columns
    assert "Sector" in df_result.columns
    assert "GrupoEco" in df_result.columns

    # Test validar_datos
    validated_result = sector_pagadores_api.validar_datos(df_result)
    assert isinstance(validated_result, list)
    assert len(validated_result) == 2
    assert validated_result[0]["RUCPagador"] == "12345678901"
    assert validated_result[0]["Sector"] == "Retail"
    assert validated_result[1]["GrupoEco"] is None  # Campo vacío convertido a None

    print("✅ Test SectorPagadoresAPI: PASSED")


if __name__ == "__main__":
    test_sector_pagadores_v2_basic()
