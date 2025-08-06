"""
🧪 Test OperacionesFueraSistema V2 - Solo get_operaciones_fuera_sistema()
"""

import pandas as pd
import sys
from pathlib import Path

try:
    from toolbox.api.operaciones_fuera_sistema_api import OperacionesFueraSistemaAPI
except ImportError as e:
    raise ImportError(
        f"OperacionesFueraSistemaAPI V2 requiere dependencias de imports relativos: {e}"
    )
# Agregar el path del proyecto si no está
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


def test_operaciones_fuera_sistema_get_method():
    """Test simple y directo del método get_operaciones_fuera_sistema()"""

    # Constructor
    api = OperacionesFueraSistemaAPI()

    # Test del método get_operaciones_fuera_sistema()
    try:
        resultado = api.get_operaciones_fuera_sistema(as_df=True)

        # Verificar que es un DataFrame
        assert isinstance(
            resultado, pd.DataFrame
        ), f"Expected DataFrame, got {type(resultado)}"

        print("✅ get_operaciones_fuera_sistema() funciona correctamente")
        print(f"   - Tipo: {type(resultado)}")
        print(f"   - Shape: {resultado.shape}")
        print(
            f"   - Columnas: {list(resultado.columns) if not resultado.empty else 'DataFrame vacío'}"
        )
        print(
            f"   - info:\n{resultado.info() if not resultado.empty else 'DataFrame vacío'}"
        )

    except Exception as e:
        print(f"❌ Error en get_operaciones_fuera_sistema(): {e}")
        raise
