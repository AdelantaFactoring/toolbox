# 🚀 Guía de instalación desde GitHub

## Pasos para subir a GitHub y permitir `pip install git+...`

### 1. Preparar el repositorio local

```bash
cd c:\Jimmy\main-backend\library-adelanta\toolbox\v2
git init
git add .
git commit -m "Initial commit: Adelanta Toolbox V2 con arquitectura hexagonal"
```

### 2. Crear repositorio en GitHub

1. Ve a [GitHub](https://github.com)
2. Crea un nuevo repositorio llamado `adelanta-toolbox`
3. **NO** inicialices con README, .gitignore o LICENSE (ya los tienes)

### 3. Conectar y subir

```bash
git remote add origin https://github.com/TU_USUARIO/adelanta-toolbox.git
git branch -M main
git push -u origin main
```

### 4. Instalar desde cualquier lugar

Una vez subido a GitHub, cualquiera puede instalarlo con:

```bash
# Instalación básica
pip install git+https://github.com/TU_USUARIO/adelanta-toolbox.git

# Para desarrollo (con dependencias de testing)
pip install "git+https://github.com/TU_USUARIO/adelanta-toolbox.git[dev]"

# Versión específica (si creas tags)
pip install git+https://github.com/TU_USUARIO/adelanta-toolbox.git@v2.0.0
```

### 5. Usar la librería

```python
# Importaciones directas de APIs específicos
from adelanta_toolbox.toolbox.api.fondo_promocional_api import get_fondo_promocional
from adelanta_toolbox.toolbox.api.fondo_crecer_api import get_fondo_crecer
from adelanta_toolbox.toolbox.api.comisiones_api import ComisionesCalcular

# Usar las funciones
promocional = get_fondo_promocional()
crecer = get_fondo_crecer()
comisiones = ComisionesCalcular(kpi_df)
```

### 6. Verificar instalación

```python
# Test básico de instalación
try:
    from adelanta_toolbox.toolbox.api.comisiones_api import ComisionesCalcular
    print("✅ Adelanta Toolbox instalado correctamente")
except ImportError as e:
    print(f"❌ Error en instalación: {e}")
```

## Estructura final del proyecto

```
adelanta-toolbox/
├── README.md                    # Documentación principal
├── LICENSE                      # Licencia MIT
├── pyproject.toml              # Configuración moderna Python
├── setup.py                    # Configuración clásica Python
├── requirements.txt            # Dependencias
├── MANIFEST.in                 # Archivos a incluir en distribución
├── .gitignore                  # Archivos a ignorar
├── ARCHITECTURE_GUIDE.md       # Guía de arquitectura hexagonal
├── __init__.py                 # Punto de entrada principal
├── toolbox/                    # Paquete principal
│   ├── __init__.py            # Exports de toolbox
│   ├── api/                   # APIs públicas
│   ├── engines/               # Lógica de negocio
│   ├── io/                    # Comunicación externa
│   ├── processing/            # Pipelines ETL
│   ├── schemas/               # Esquemas Pydantic
│   ├── config/                # Configuración
│   └── core/                  # Componentes base
└── test/                      # Tests
    ├── __init__.py
    ├── conftest.py
    ├── pytest.ini
    └── test_*.py
```

## Comandos útiles

```bash
# Desarrollo local
pip install -e .

# Testing
pytest test/ -v

# Build para distribución
python -m build

# Linting
black toolbox/
flake8 toolbox/
```

---

## ✅ TODO listo para GitHub

Tu proyecto ya está configurado correctamente para:

-   ✅ Instalación con `pip install git+...`
-   ✅ Arquitectura hexagonal limpia
-   ✅ Sin fallbacks de importación
-   ✅ Testing básico funcional
-   ✅ Documentación completa
