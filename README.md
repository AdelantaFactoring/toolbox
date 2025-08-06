# Adelanta Toolbox

Librería con **arquitectura hexagonal** para procesos financieros ETL. Refactorización modular del sistema financiero con diseño hexagonal estricto.

## Instalación

### Desde GitHub

```bash
pip install git+https://github.com/tu-usuario/adelanta-toolbox.git
```

### Para desarrollo

```bash
git clone https://github.com/tu-usuario/adelanta-toolbox.git
cd adelanta-toolbox
pip install -e .[dev]
```

## Características

-   **Arquitectura Hexagonal** - Separación clara de responsabilidades
-   **APIs Simples** - Interfaces compatibles con V1
-   **Validación Pydantic** - Esquemas robustos de datos
-   **Procesamiento ETL** - Pipelines especializados
-   **Módulos Especializados** - Fondos, comisiones, KPIs, etc.

## Arquitectura

```
toolbox/
├── api/         # Interfaz pública simple
├── engines/     # Motores especializados (cálculo, validación, datos)
├── io/          # Comunicación externa (webservices, archivos)
├── processing/  # Pipelines (transformers, validators)
├── schemas/     # Contratos Pydantic
├── config/      # Configuración centralizada
└── core/        # Componentes base
```

## Uso Rápido

### KPI API

```python
from toolbox.api.kpi_api import get_kpi
from datetime import datetime
import pandas as pd

# Preparar datos de tipo de cambio
tipo_cambio_df = pd.DataFrame(...)

# Calcular KPIs
resultado = await get_kpi(
    tipo_cambio_df=tipo_cambio_df,
    start_date=datetime(2024, 1, 1),
    end_date=datetime(2024, 12, 31),
    fecha_corte=datetime(2024, 12, 31),
    as_df=True
)
```

### Fondos API

```python
# Fondo promocional
from toolbox.api.fondo_promocional_api import get_fondo_promocional
promocional = get_fondo_promocional()

# Fondo crecer
from toolbox.api.fondo_crecer_api import get_fondo_crecer
crecer = get_fondo_crecer()
```

### Comisiones

```python
from toolbox.api.comisiones_api import ComisionesCalcular

# Calcular comisiones
comisiones = ComisionesCalcular(kpi_df)
resultado = comisiones.calculate()
```

## Módulos Disponibles

| Módulo               | Descripción                 | API                                         |
| -------------------- | --------------------------- | ------------------------------------------- |
| **KPIs**             | Cálculo de KPIs financieros | `get_kpi`                                   |
| **Fondos**           | Fondo promocional y crecer  | `get_fondo_promocional`, `get_fondo_crecer` |
| **Comisiones**       | Cálculo de comisiones       | `ComisionesCalcular`                        |
| **Diferidos**        | Procesamiento diferidos     | APIs especializadas                         |
| **Sector Pagadores** | Análisis sector pagadores   | APIs especializadas                         |
| **Ventas**           | Autodetracciones            | APIs especializadas                         |

## Testing

```bash
# Ejecutar todos los tests
pytest

# Tests específicos
pytest test/test_kpi.py
pytest test/test_fondos.py
pytest test/test_comisiones.py

# Con coverage
pytest --cov=toolbox
```

## Documentación

-   [`ARCHITECTURE_GUIDE.md`](ARCHITECTURE_GUIDE.md) - Guía completa de arquitectura hexagonal
-   [`DEVELOPMENT_PROMPT.md`](DEVELOPMENT_PROMPT.md) - Guía de desarrollo
-   Módulos individuales tienen documentación en sus respectivos archivos

## Desarrollo

### Prerequisitos

-   Python >= 3.8
-   pip >= 21.0

### Setup desarrollo

```bash
git clone https://github.com/tu-usuario/adelanta-toolbox.git
cd adelanta-toolbox
pip install -e .[dev]
```

### Ejecutar tests

```bash
pytest test/ -v -s
```

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Licencia

MIT License - ver [LICENSE](LICENSE) para detalles.

## Compatibilidad

Mantiene **compatibilidad total** con interfaces V1 mientras mejora la arquitectura interna.

## Versión

Versión actual: **0.5.0**

```python
import toolbox
print(toolbox.__version__)  # 0.5.0
```
