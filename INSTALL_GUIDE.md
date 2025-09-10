# 📋 Adelanta Toolbox - Guía de Instalación Simple

## 🚀 Instalación (Una sola línea)

```bash
uv pip install adelanta-toolbox
```

## ⚠️ **CONFIGURACIÓN OBLIGATORIA**

Antes de usar la librería, **DEBES** configurarla con tus settings:

### Paso 1: Crear configuración

```python
# config.py
TOOLBOX_CONFIG = {
    'WEBSERVICE_BASE_URL': "https://tu-webservice.com",
    'KPI_CREDENTIALS': {
        "username": "TU_USERNAME",
        "password": "TU_PASSWORD",
    },
    'INTERESES_PEN': 0.14,
    'INTERESES_USD': 0.12,
    'GOOGLE_SHEETS_URLS': {
        "fondo_promocional": "TU_URL_1",
        "fondo_crecer": "TU_URL_2",
        # ... todas las URLs necesarias
    }
}
```

### Paso 2: Inicializar ANTES de usar

```python
import toolbox
from config import TOOLBOX_CONFIG

# ⚡ OBLIGATORIO: Configurar primero
toolbox.configure(TOOLBOX_CONFIG)

# ✅ Ahora sí usar las APIs
from toolbox.api.kpi_api import get_kpi
resultado = await get_kpi(...)
```

## 📄 Template de Configuración

Copia `config_template.py` y completa con tus valores reales.

## 🛠️ Para Desarrolladores

### Publicar nueva versión

```bash
# 1. Actualizar versión en pyproject.toml
# 2. Build
uv build

# 3. Publicar a PyPI (solo una vez configurar token)
uv publish
```

### Instalar desde fuente local

```bash
pip install -e .
```

## ✅ Verificar Instalación

```python
import toolbox
print("✅ Adelanta Toolbox funcionando correctamente")
```
