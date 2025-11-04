# 🏗️ CONTEXTO COMPLETO: Adelanta Toolbox - Librería Financiera Moderna con Arquitectura Hexagonal

## 📋 **Stack Tecnológico Core**

-   **Python**: 3.12+
-   **Validación**: Pydantic 2.0+ con validadores personalizados y `ConfigDict(arbitrary_types_allowed=True)`
-   **Data Processing**: pandas, polars, numpy optimizados
-   **Database**: SQLAlchemy 2.0+ (async preferred)
-   **Testing**: pytest + testing comprehensivo
-   **Packaging**: pyproject.toml + setuptools build system moderno
-   **Architecture**: Hexagonal pura (6 archivos obligatorios por módulo)

## 🏛️ **Arquitectura Hexagonal PURA**

### **📁 Estructura Obligatoria por Módulo**

Para **CADA** módulo de negocio, crear **EXACTAMENTE** estos 6 archivos:

```
toolbox/
├── engines/xxx_engine.py              # ⚙️ Lógica de negocio optimizada
├── io/xxx_client.py                   # 📡 Cliente para fuentes externas
├── schemas/xxx_schema.py              # 📊 Schema Pydantic robusto
├── processing/
│   ├── transformers/xxx_transformer.py # 🔄 Transformaciones especializadas
│   └── validators/xxx_validator.py     # ✅ Validación robusta
├── api/xxx_api.py                     # 🌐 API pública elegante
└── test/test_xxx.py                   # 🧪 Testing comprehensivo
```

### **🎯 Principios Arquitectónicos FUNDAMENTALES**

-   **Arquitectura Hexagonal Pura**: Separación clara de responsabilidades
-   **APIs Elegantes**: Interfaces públicas intuitivas y documentadas
-   **Lógica Optimizada**: Implementación moderna sin legado
-   **6 archivos obligatorios** por módulo (sin excepciones)
-   **Tiempo desarrollo < 75 min** por módulo completo

## 📋 **Reglas de Desarrollo**

### **Alcance de Tareas**

-   **Estricto**: Si pido "desarrollar A, B y C", solo implementa A, B y C.
-   **Libre**: Cuando indico "desarrollo libre", puedes sugerir módulos extra, pero **SIEMPRE** espera mi aprobación antes de codificar.

### **✅ Buenas Prácticas MODERNAS**

-   **Imports relativos** para módulos internos: `from ..schemas.xxx_schema import XxxSchema`
-   **Manejo robusto** de errores con try/except y logging detallado
-   **Logger centralizado**: `from ..config.settings import V2Settings; V2Settings.logger(mensaje)`
-   **Pydantic schemas** con validadores personalizados y `ConfigDict(arbitrary_types_allowed=True)`
-   **APIs públicas** con type hints completos y documentación clara
-   **Testing comprehensivo** que valide funcionalidad real
-   **Cliente funcional** para fuentes de datos reales (no placeholders)

### **🚨 Consideraciones Críticas MODERNAS**

-   **SIEMPRE implementar** lógica de negocio optimizada y moderna
-   **SIEMPRE crear** interfaces públicas elegantes e intuitivas
-   **SIEMPRE usar** imports relativos con manejo de errores robusto
-   **Logger centralizado** obligatorio desde `V2Settings.logger`
-   **Cliente funcional** para todas las fuentes de datos
-   **Validación Pydantic** robusta en todos los schemas
-   **Tests comprehensivos** que validen arquitectura y funcionalidad

### **🚫 Anti-Patterns A EVITAR**

-   ❌ Copiar código legacy sin refactorizar
-   ❌ Mantener compatibilidad con sistemas antiguos
-   ❌ Crear placeholders vacíos sin implementación
-   ❌ Usar imports absolutos para módulos internos
-   ❌ Schema sin validadores personalizados
-   ❌ APIs sin documentación adecuada
-   ❌ Tests triviales sin validación real
-   ❌ **COMENTARIOS EXCESIVOS**: Evitar comentarios obvios o redundantes

### **📝 Guía de Comentarios MINIMALISTA**

-   **SÍ usar**: Docstrings para clases y métodos públicos
-   **SÍ usar**: Comentarios para lógica compleja no obvia
-   **NO usar**: Comentarios que repiten lo que hace el código
-   **NO usar**: Emojis excesivos en comentarios internos
-   **Ejemplo CORRECTO**:
    ```python
    def renombrar_columnas(self, df: pd.DataFrame) -> pd.DataFrame:
        """Renombra columnas según mapping"""
        return df.rename(columns=self.mapping)
    ```
-   **Ejemplo INCORRECTO**:
    ```python
    def renombrar_columnas(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        🔄 Renombra columnas según mapping específico
        Elimina columnas vacías y normaliza nombres
        """
        # Aplicar mapping de columnas
        df_renamed = df.rename(columns=self.mapping)  # Renombrar
        # Retornar el resultado
        return df_renamed
    ```

### **✅ Best Practices OBLIGATORIAS**

-   ✅ Implementar arquitectura hexagonal pura
-   ✅ APIs elegantes con type hints completos
-   ✅ Schema Pydantic robusto con validadores
-   ✅ Cliente funcional para fuentes reales
-   ✅ Logging centralizado y detallado
-   ✅ Testing comprehensivo con datos reales
-   ✅ Documentación clara y completa
-   ✅ **COMENTARIOS MÍNIMOS**: Solo docstrings esenciales, evitar comentarios excesivos

## 🔧 **Patterns de Implementación MODERNOS**

### **Logger Pattern (Obligatorio)**

```python
# En cualquier módulo - usando V2Settings
try:
    from ..config.settings import V2Settings
    logger = V2Settings.logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__).warning
```

### **Client Pattern para Fuentes Externas**

```python
# Cliente funcional para datos reales
try:
    from ..core.base_client import BaseClient
    from ..config.settings import V2Settings
except ImportError:
    raise ImportError("Cliente requiere dependencias base")

class XxxClient(BaseClient):
    def __init__(self):
        super().__init__(timeout=30)
        self.url = V2Settings.GOOGLE_SHEETS_URLS["xxx"]

    def fetch_xxx_data(self):
        try:
            V2Settings.logger("Obteniendo datos Xxx")
            data = self.get_data_sync(self.url)
            V2Settings.logger(f"Datos obtenidos: {len(data)} registros")
            return data
        except Exception as e:
            V2Settings.logger(f"Error obteniendo datos: {e}")
            raise
```

### **Schema Pattern Robusto**

```python
from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime

class XxxSchema(BaseModel):
    modelo_config = ConfigDict(arbitrary_types_allowed=True)

    campo1: str = Field(..., description="Campo obligatorio")
    fecha: datetime = Field(..., description="Campo fecha validado")

    @field_validator("fecha", mode="before")
    @classmethod
    def parsear_fecha(cls, v):
        if isinstance(v, str):
            return datetime.strptime(v, "%d/%m/%Y")
        return v
```

### **API Pattern Elegante**

```python
class XxxAPI:
    def __init__(self):
        self._client = XxxClient()
        self._transformer = XxxTransformer()
        self._validator = XxxValidator()
        self._engine = XxxEngine()

    def get_xxx(self, as_df: bool = False) -> Union[pd.DataFrame, List[Dict[str, Any]]]:
        """API elegante con documentación completa"""
        V2Settings.logger("Iniciando procesamiento Xxx")

        # Pipeline de procesamiento claro
        raw_data = self._client.fetch_xxx_data()
        df = self._transformer.convertir_a_dataframe(raw_data)
        self._validator.validar_columnas_xxx(df)
        df = self._transformer.procesar_datos_xxx(df)
        validated_data = self._validator.validar_schema_xxx(df)

        return self._transformer.convertir_a_dataframe(validated_data) if as_df else validated_data
```

## 🎯 **Objetivos y Criterios de Éxito MODERNOS**

### **Objetivo Principal**

Implementación moderna de arquitectura hexagonal que maximiza mantenibilidad, testabilidad, performance y elegancia del código.

### **Criterios Éxito por Implementación**

-   ✅ 6 archivos creados siguiendo arquitectura hexagonal pura
-   ✅ Schema Pydantic robusto con validadores personalizados
-   ✅ Cliente funcional para fuentes de datos reales
-   ✅ API pública elegante con type hints completos
-   ✅ Tests comprehensivos que validen funcionalidad real
-   ✅ Logger centralizado con V2Settings funcionando
-   ✅ Imports relativos con manejo robusto de errores
-   ✅ Tiempo total < 75 minutos

### **Red Flags (Implementación fallida)**

-   ❌ Faltan archivos (menos de 6)
-   ❌ Schema sin validadores personalizados
-   ❌ Cliente placeholder vacío sin funcionalidad
-   ❌ API sin type hints o documentación
-   ❌ Tests triviales sin validación real
-   ❌ Errores de import sin resolver
-   ❌ Tiempo > 2 horas

## 🚀 **Comandos de Validación MODERNOS**

```bash
# Test específico del módulo
python test/test_xxx.py

# Test con pytest comprehensivo
pytest test/test_xxx.py -v

# Test de funcionalidad real
python -c "from toolbox.api.xxx_api import get_xxx; print('✅ Import OK'); result = get_xxx(as_df=True); print(f'✅ Funciona: {result.shape}')"

# Resultado esperado siempre:
# ✅ Import exitoso
# ✅ Funcionalidad real operativa
# ✅ Datos procesados correctamente
# ✅ Arquitectura hexagonal validada
# ✅ Performance optimizada
```

## 💫 **Lema de Desarrollo MODERNO**

> **"6 archivos obligatorios. Arquitectura hexagonal pura. APIs elegantes. Funcionalidad real."**

Esta librería implementa arquitectura hexagonal moderna que facilita el mantenimiento de sistemas financieros complejos mediante código elegante, APIs intuitivas y testing robusto.
