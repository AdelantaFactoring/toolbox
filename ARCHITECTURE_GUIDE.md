# 🏗️ Adelanta Toolbox - Arquitectura Hexagonal MODERNA

## 🚨 PRINCIPIOS ARQUITECTÓNICOS FUNDAMENTALES

### ⚡ OBJETIVO PRINCIPAL: ARQUITECTURA HEXAGONAL PURA

```
Adelanta Toolbox = ARQUITECTURA HEXAGONAL MODERNA
✅ SÍ implementar lógica de negocio optimizada
✅ SÍ crear interfaces públicas elegantes
✅ SÍ aplicar mejores prácticas de software
✅ SÍ optimizar performance y mantenibilidad
❌ NO copiar código legacy
❌ NO mantener compatibilidad V1
```

## 🎯 ARQUITECTURA HEXAGONAL - 6 ARCHIVOS OBLIGATORIOS

Para **CADA** módulo de negocio, se deben crear **EXACTAMENTE 6 archivos**:

### 📁 Estructura Obligatoria

```
toolbox/
├── engines/xxx_engine.py              # ⚙️ Lógica de negocio optimizada
├── io/xxx_client.py                   # 📡 Cliente para fuentes externas
├── schemas/xxx_schema.py              # 📊 Schema Pydantic robusto
├── processing/
│   ├── transformers/xxx_transformer.py # 🔄 Transformaciones de datos
│   └── validators/xxx_validator.py     # ✅ Validación de datos
├── api/xxx_api.py                     # 🌐 API pública elegante
└── test/test_xxx.py                   # 🧪 Tests comprehensivos
```

## 🔒 TEMPLATES OBLIGATORIOS MODERNOS

### 1️⃣ **Engine** (Lógica de negocio)

```python
"""
⚙️ Xxx Engine V2
LÓGICA DE NEGOCIO OPTIMIZADA
"""

try:
    from ..core.base_engine import BaseEngine
except ImportError:
    raise ImportError("XxxEngine requiere BaseEngine de imports relativos")

class XxxEngine(BaseEngine):
    """Motor especializado que hereda de BaseEngine"""

    def __init__(self):
        super().__init__()

    def metodo_principal(self, data):
        """Implementación optimizada de lógica de negocio"""
        # Lógica de negocio específica del dominio
        pass
```

### 2️⃣ **Client** (I/O Externa)

```python
"""
📡 Xxx Client V2 - Cliente especializado para fuentes externas
"""

try:
    from ..core.base_client import BaseClient
    from ..config.settings import V2Settings
except ImportError:
    raise ImportError("XxxClient requiere BaseClient y V2Settings")

class XxxClient(BaseClient):
    """Cliente especializado para obtener datos externos"""

    def __init__(self):
        super().__init__(timeout=30)
        self.url = V2Settings.GOOGLE_SHEETS_URLS["xxx"]

    def fetch_xxx_data(self):
        """Obtiene datos de fuente externa"""
        try:
            V2Settings.logger("Iniciando obtención de datos Xxx")
            data = self.get_data_sync(self.url)
            V2Settings.logger(f"Datos obtenidos: {len(data)} registros")
            return data
        except Exception as e:
            V2Settings.logger(f"Error obteniendo datos: {e}")
            raise
```

### 3️⃣ **Schema** (Validación Pydantic)

```python
"""
🏷️ Xxx Schema V2 - Validación robusta con Pydantic
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime

class XxxSchema(BaseModel):
    """Schema robusto para validación de datos Xxx"""

    campo1: str = Field(..., description="Campo obligatorio")
    campo2: datetime = Field(..., description="Campo fecha")
    campo3: float = Field(..., gt=0, description="Campo numérico positivo")

    @field_validator("campo2", mode="before")
    @classmethod
    def parsear_fecha(cls, v):
        """Validador personalizado para fechas"""
        if isinstance(v, str):
            return datetime.strptime(v, "%d/%m/%Y")
        return v

    model_config = ConfigDict(arbitrary_types_allowed=True)
```

### 4️⃣ **Transformer** (Procesamiento)

```python
"""
🔄 Xxx Transformer V2 - Transformaciones especializadas
"""

try:
    from ...core.base_transformer import BaseTransformer
except ImportError:
    raise ImportError("XxxTransformer requiere BaseTransformer")

class XxxTransformer(BaseTransformer):
    """Transformer especializado para datos Xxx"""

    def __init__(self):
        super().__init__()
        self.column_mapping = {
            "campo_origen": "CampoDestino",
            "otro_campo": "OtroCampo"
        }

    def renombrar_columnas_xxx(self, df):
        """Renombra columnas según mapping específico"""
        return self.renombrar_columnas(df, self.column_mapping)

    def procesar_datos_xxx(self, df):
        """Procesamiento específico del dominio"""
        # Transformaciones específicas
        return df
```

### 5️⃣ **Validator** (Validación de datos)

```python
"""
✅ Xxx Validator V2 - Validación especializada
"""

try:
    from ...core.base_validator import BaseValidator
    from ...schemas.xxx_schema import XxxSchema
    from ...config.settings import V2Settings
except ImportError:
    raise ImportError("XxxValidator requiere dependencias")

class XxxValidator(BaseValidator):
    """Validador especializado para Xxx"""

    _cols_esperadas = ["CAMPO1", "CAMPO2", "CAMPO3"]

    def __init__(self):
        super().__init__(schema_class=XxxSchema)

    def validar_columnas_xxx(self, df):
        """Validación específica de columnas"""
        self.validar_columnas(df, self._cols_esperadas)

    def validar_schema_xxx(self, raw_data):
        """Validación todo o nada con schema"""
        V2Settings.logger(f"Validando schema Xxx: {len(raw_data)} registros")
        validated_data = self.validar_schema(raw_data)
        V2Settings.logger(f"Validación completada: {len(validated_data)} válidos")
        return validated_data
```

### 6️⃣ **API** (Interfaz pública)

```python
"""
🌐 Xxx API V2 - Interfaz pública elegante
"""

import pandas as pd
from typing import List, Dict, Any, Union

try:
    from ..config.settings import V2Settings
    from ..io.xxx_client import XxxClient
    from ..processing.transformers.xxx_transformer import XxxTransformer
    from ..processing.validators.xxx_validator import XxxValidator
    from ..engines.xxx_engine import XxxEngine
except ImportError:
    raise ImportError("XxxAPI requiere todas las dependencias")

class XxxAPI:
    """API pública para Xxx con interfaz moderna"""

    def __init__(self):
        self._client = XxxClient()
        self._transformer = XxxTransformer()
        self._validator = XxxValidator()
        self._engine = XxxEngine()

    def get_xxx(self, as_df: bool = False) -> Union[pd.DataFrame, List[Dict[str, Any]]]:
        """
        Obtiene datos procesados de Xxx

        Args:
            as_df: Si True retorna DataFrame, si False lista de diccionarios

        Returns:
            Datos procesados y validados
        """
        V2Settings.logger("Iniciando obtención de datos Xxx")

        # 1) Obtener datos crudos
        raw_data = self._client.fetch_xxx_data()

        # 2) Convertir a DataFrame
        df = self._transformer.convertir_a_dataframe(raw_data)

        # 3) Validar columnas
        self._validator.validar_columnas_xxx(df)

        # 4) Transformar datos
        df = self._transformer.renombrar_columnas_xxx(df)
        df = self._transformer.procesar_datos_xxx(df)

        # 5) Validar schema
        validated_data = self._validator.validar_schema_xxx(df)

        # 6) Retornar según formato
        if as_df:
            return self._transformer.convertir_a_dataframe(validated_data)
        return validated_data

# Instancia global
xxx_api = XxxAPI()

# Función de conveniencia
def get_xxx(as_df: bool = False):
    """Función de conveniencia: toolbox.xxx.get_xxx()"""
    return xxx_api.get_xxx(as_df)
```

### 7️⃣ **Test** (Testing comprehensivo)

```python
"""
🧪 Test Xxx V2 - Testing moderno
"""

import pytest
import pandas as pd

def test_xxx_api_basic():
    """Test básico de funcionalidad API"""
    try:
        from ..api.xxx_api import XxxAPI
    except ImportError:
        pytest.skip("No se pudo importar XxxAPI")

    api = XxxAPI()

    # Verificar arquitectura hexagonal
    assert hasattr(api, '_client')
    assert hasattr(api, '_transformer')
    assert hasattr(api, '_validator')
    assert hasattr(api, '_engine')

    # Verificar métodos públicos
    assert hasattr(api, 'get_xxx')
    assert callable(api.get_xxx)

    print("✅ Test XxxAPI: PASSED")

def test_xxx_api_functionality():
    """Test de funcionalidad real"""
    from ..api.xxx_api import get_xxx

    # Test con datos reales
    resultado = get_xxx(as_df=True)
    assert isinstance(resultado, pd.DataFrame)

    # Test con lista
    resultado_list = get_xxx(as_df=False)
    assert isinstance(resultado_list, list)

    print("✅ Test funcionalidad Xxx: PASSED")

if __name__ == "__main__":
    test_xxx_api_basic()
    test_xxx_api_functionality()
```

## 🚀 PROCESO DE DESARROLLO - 4 PASOS MODERNOS

### **PASO 1: DISEÑAR DOMINIO** ⏱️ 15 minutos máximo

1. Identificar entidad de negocio: `Referidos`, `Comisiones`, etc.
2. Definir schema Pydantic robusto con validadores
3. Mapear fuentes de datos (Google Sheets, APIs, etc.)
4. Diseñar interfaz pública elegante

### **PASO 2: CREAR ESTRUCTURA** ⏱️ 15 minutos máximo

Crear los **6 archivos obligatorios** siguiendo templates modernos:

-   `engines/xxx_engine.py` - Lógica de negocio especializada
-   `io/xxx_client.py` - Cliente para fuentes externas
-   `schemas/xxx_schema.py` - Schema Pydantic robusto
-   `processing/transformers/xxx_transformer.py` - Transformaciones
-   `processing/validators/xxx_validator.py` - Validaciones
-   `api/xxx_api.py` - API pública elegante

### **PASO 3: IMPLEMENTAR LÓGICA** ⏱️ 30 minutos máximo

-   Engine: Implementar lógica de negocio optimizada
-   Client: Conectar con fuentes de datos reales
-   Schema: Validadores robustos con Pydantic
-   Transformer: Transformaciones específicas del dominio
-   Validator: Validaciones todo o nada
-   API: Interfaz pública clara y elegante

### **PASO 4: TESTING COMPREHENSIVO** ⏱️ 15 minutos máximo

-   Crear `test/test_xxx.py` con tests modernos
-   Verificar arquitectura hexagonal
-   Probar funcionalidad real con datos
-   Validar performance y robustez

## ⚡ CRITERIOS DE ÉXITO

### ✅ **IMPLEMENTACIÓN EXITOSA**

-   6 archivos creados siguiendo arquitectura hexagonal
-   Schema Pydantic robusto con validadores
-   Cliente funcional para fuentes externas
-   API pública elegante y documentada
-   Tests comprehensivos que pasan
-   Tiempo total < 75 minutos

### ❌ **IMPLEMENTACIÓN FALLIDA**

-   Faltan archivos (menos de 6)
-   Schema sin validadores robustos
-   Cliente no funcional o placeholder vacío
-   API sin documentación clara
-   Tests que no pasan o son insuficientes
-   Tiempo > 2 horas

## 🚫 ANTI-PATTERNS A EVITAR

-   ❌ Copiar código legacy sin refactorizar
-   ❌ Mantener compatibilidad con sistemas antiguos
-   ❌ Placeholders vacíos sin implementación
-   ❌ Schema sin validadores personalizados
-   ❌ APIs sin documentación adecuada
-   ❌ Tests triviales sin valor real

## ✅ BEST PRACTICES OBLIGATORIAS

-   ✅ Implementar lógica de negocio optimizada
-   ✅ Usar Pydantic para validación robusta
-   ✅ Logging centralizado con V2Settings
-   ✅ Imports relativos con manejo de errores
-   ✅ Cliente funcional para fuentes reales
-   ✅ API elegante con type hints completos
-   ✅ Tests que validen funcionalidad real

## 🚀 COMANDO DE VALIDACIÓN

```bash
# Test específico del módulo
python test/test_xxx.py

# Test con pytest
pytest test/test_xxx.py -v

# Test de funcionalidad real
python -c "from toolbox.api.xxx_api import get_xxx; print('✅ Import OK'); result = get_xxx(as_df=True); print(f'✅ Funciona: {result.shape}')"

# Resultado esperado siempre:
# ✅ Import exitoso
# ✅ Funcionalidad real operativa
# ✅ Arquitectura hexagonal completa
# ✅ Performance optimizada
```

---

## 🎯 LEMA DE DESARROLLO MODERNO

> **"6 archivos obligatorios. Arquitectura hexagonal pura. Lógica optimizada. APIs elegantes."**

Esta es una **implementación moderna de arquitectura hexagonal** que maximiza mantenibilidad, testabilidad y escalabilidad sin comprometer la elegancia del código.
