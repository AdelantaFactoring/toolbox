# 🏗️ Adelanta Factoring V2 - Arquitectura Hexagonal ESTRICTA

## 🚨 REGLAS NON-NEGOTIABLES DE MIGRACIÓN V2

### ⚡ PRIORIDAD #1: COMPATIBILIDAD TOTAL

```
V2 = REESTRUCTURACIÓN ARQUITECTÓNICA ÚNICAMENTE
❌ NO cambiar lógica de negocio
❌ NO modificar cálculos financieros
❌ NO inventar validaciones nuevas
❌ NO optimizar performance (aún)
✅ SÍ copiar código exacto de V1
✅ SÍ mantener mismas interfaces públicas
```

## 🎯 ARQUITECTURA HEXAGONAL V2 - 6 ARCHIVOS OBLIGATORIOS

Para **CADA** módulo `XxxCalcular.py` de V1, se deben crear **EXACTAMENTE 6 archivos**:

### 📁 Estructura Obligatoria

```
v2/
├── engines/xxx_engine.py              # ⚙️ Lógica V1 copiada exacta
├── io/xxx_client.py                   # 📡 Cliente externo o placeholder
├── schemas/xxx_schema.py              # 📊 Schema Pydantic con ConfigDict
├── processing/
│   ├── transformers/xxx_transformer.py # 🔄 Transformer o placeholder
│   └── validators/xxx_validator.py     # ✅ Validator o placeholder
├── api/xxx_api.py                     # 🌐 API wrapper con interfaz V1
└── test/test_xxx.py                   # 🧪 Test simple de compatibilidad
```

## 🔒 TEMPLATES OBLIGATORIOS EXACTOS

### 1️⃣ **Engine** (Lógica de negocio)

```python
"""
⚙️ Xxx Engine V2
LÓGICA COPIADA EXACTA DE XxxCalcular V1
"""

class XxxEngine:
    """Motor que contiene TODA la lógica de XxxCalcular V1"""

    def __init__(self):
        # Copiar inicialización de V1 si existe
        pass

    def metodo_principal(self, param1, param2):
        """COPIAR MÉTODO EXACTO DE V1"""
        # TODO: Copiar línea por línea desde V1
        pass
```

### 2️⃣ **Client** (I/O Externa)

```python
"""
📡 Xxx Client V2 - Cliente especializado o Placeholder

[Si NO tiene webservice]: Placeholder para mantener consistencia arquitectónica
[Si SÍ tiene webservice]: Cliente que hereda de BaseClient
"""

# OPCIÓN A: Placeholder (cuando no hay webservice)
pass

# OPCIÓN B: Cliente real (cuando sí hay webservice)
try:
    from ..core.base_client import BaseClient
except ImportError:
    raise ImportError("XxxClient V2 requiere BaseClient de imports relativos")

class XxxClient(BaseClient):
    def __init__(self):
        super().__init__(timeout=30)
        # Configuración específica
```

### 3️⃣ **Schema** (Validación Pydantic)

```python
"""
📊 Schemas Pydantic V2 - Xxx
Mantiene compatibilidad con v1 mientras mejora validación
"""

from pydantic import BaseModel, ConfigDict

class XxxSchema(BaseModel):
    """Schema base para Xxx"""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # [Si no hay campos específicos]: pass
    # [Si sí hay campos]: definir campos con validadores

# Alias para compatibilidad con v1
XxxCalcularSchema = XxxSchema
```

### 4️⃣ **Transformer** (Procesamiento)

```python
"""
🔄 Xxx Transformer V2 - Placeholder o Implementación

Transformer especializado para procesamiento de datos de Xxx
"""

try:
    from ...core.base_transformer import BaseTransformer
except ImportError:
    raise ImportError("XxxTransformer V2 requiere BaseTransformer de imports relativos")

class XxxTransformer(BaseTransformer):
    def __init__(self):
        super().__init__()

    pass  # Placeholder para futura implementación
```

### 5️⃣ **Validator** (Validación de datos)

```python
"""
✅ Xxx Validator V2 - Placeholder o Implementación

Validator especializado para validación de datos de Xxx
"""

try:
    from ...core.base_validator import BaseValidator
except ImportError:
    raise ImportError("XxxValidator V2 requiere BaseValidator de imports relativos")

class XxxValidator(BaseValidator):
    def __init__(self):
        super().__init__()

    pass  # Placeholder para futura implementación
```

### 6️⃣ **API** (Interfaz pública)

```python
"""
🌐 API V2 - Xxx
INTERFAZ IDÉNTICA A V1
"""

try:
    from ..engines.xxx_engine import XxxEngine
    from ..io.xxx_client import XxxClient
    from ..processing.transformers.xxx_transformer import XxxTransformer
    from ..processing.validators.xxx_validator import XxxValidator
except ImportError:
    raise ImportError("XxxAPI V2 requiere dependencias de imports relativos")

class XxxAPI:
    """Wrapper que mantiene interfaz exacta de V1"""

    def __init__(self, param1, param2):  # MISMOS PARÁMETROS QUE V1
        """Constructor IDÉNTICO a V1"""
        self.param1 = param1
        self.param2 = param2
        self._engine = XxxEngine()
        self._client = XxxClient()
        self._transformer = XxxTransformer()
        self._validator = XxxValidator()

    def metodo_v1(self, param):
        """Método IDÉNTICO a V1"""
        return self._engine.metodo_principal(param)

# Alias para compatibilidad con v1
XxxCalcular = XxxAPI
```

### 7️⃣ **Test** (Compatibilidad)

```python
"""
🧪 Test Xxx V2 - Compatibilidad V1
"""

import pytest
import pandas as pd

def test_xxx_v2_basic():
    """Test que V2 tiene misma interfaz que V1"""
    try:
        from ..api.xxx_api import XxxAPI
    except ImportError:
        pytest.skip("No se pudo importar XxxAPI")

    # Datos mínimos para test
    param1 = "test"
    param2 = pd.DataFrame({"col": [1, 2, 3]})

    # Constructor igual que V1
    xxx_api = XxxAPI(param1, param2)

    # Verificar interfaz
    assert hasattr(xxx_api, 'metodo_v1')
    assert callable(xxx_api.metodo_v1)

    # Verificar arquitectura hexagonal
    assert hasattr(xxx_api, '_engine')
    assert hasattr(xxx_api, '_client')
    assert hasattr(xxx_api, '_transformer')
    assert hasattr(xxx_api, '_validator')

    print("✅ Test XxxAPI: PASSED")

if __name__ == "__main__":
    test_xxx_v2_basic()
```

## � PROCESO DE MIGRACIÓN - 4 PASOS EXACTOS

### **PASO 1: ANALIZAR V1** ⏱️ 10 minutos máximo

1. Leer archivo `XxxCalcular.py` completo
2. Identificar constructor: `__init__(self, param1, param2)`
3. Listar métodos públicos: `method1()`, `method2()`
4. Identificar dependencias (obtener, schemas)

### **PASO 2: CREAR ESTRUCTURA** ⏱️ 10 minutos máximo

Crear los **6 archivos obligatorios** siguiendo templates exactos:

-   `engines/xxx_engine.py`
-   `io/xxx_client.py`
-   `schemas/xxx_schema.py`
-   `processing/transformers/xxx_transformer.py`
-   `processing/validators/xxx_validator.py`
-   `api/xxx_api.py`

### **PASO 3: COPIAR LÓGICA** ⏱️ 20 minutos máximo

-   Engine: Copiar **TODO** el código de `XxxCalcular.py`
-   API: Crear wrapper con **misma interfaz** que V1
-   Resto: Implementar como placeholders

### **PASO 4: TEST SIMPLE** ⏱️ 5 minutos máximo

-   Crear `test/test_xxx.py` siguiendo template
-   Verificar que imports funcionan
-   Verificar que interfaz es idéntica a V1

## ⚡ CRITERIOS DE ÉXITO

### ✅ **MIGRACIÓN EXITOSA**

-   6 archivos creados siguiendo templates exactos
-   Constructor idéntico a V1
-   Métodos públicos idénticos a V1
-   Test simple pasa sin errores
-   Tiempo total < 45 minutos

### ❌ **MIGRACIÓN FALLIDA**

-   Faltan archivos (menos de 6)
-   Interfaz diferente a V1
-   Lógica de negocio modificada
-   Tiempo > 1 hora

## 🚫 PROHIBICIONES ABSOLUTAS

-   ❌ Modificar lógica de cálculos financieros
-   ❌ Cambiar nombres de métodos públicos
-   ❌ Modificar signatures de constructores
-   ❌ Agregar validaciones no existentes en V1
-   ❌ Optimizar performance
-   ❌ Crear menos de 6 archivos por módulo

## ✅ PERMITIDO EN V2

-   ✅ Reestructurar código entre archivos
-   ✅ Agregar imports relativos
-   ✅ Agregar placeholders para futura expansión
-   ✅ Agregar docstrings descriptivos
-   ✅ Agregar `model_config = ConfigDict(arbitrary_types_allowed=True)`

## 🚀 COMANDO DE VALIDACIÓN

```bash
cd utils/adelantafactoring/v2
python -m pytest test/test_xxx.py -v

# Resultado esperado:
# ✅ test_xxx_v2_basic PASSED
# ✅ Sin errores de import
# ✅ Tiempo < 5 segundos
```

---

## 🎯 LEMA DE MIGRACIÓN V2

> **"6 archivos obligatorios. Interfaz idéntica. Lógica copiada exacta."**

Esta es una **reestructuración arquitectónica** que facilita el mantenimiento futuro, NO una reescritura de lógica de negocio.
