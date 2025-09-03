"""
Setup configuration para Adelanta Factoring V2
Librería con arquitectura hexagonal para procesos financieros ETL
"""

from setuptools import setup, find_packages
import os

# Leer README si existe
readme_path = os.path.join(os.path.dirname(__file__), "README.md")
long_description = ""
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = """
    # Adelanta Toolbox
    
    Librería con arquitectura hexagonal para procesos financieros ETL.
    Refactorización modular del sistema financiero con diseño hexagonal.
    """

setup(
    name="adelanta-toolbox",
    version="0.51",
    author="Jimmy",
    author_email="",  # Agrega tu email aquí
    description="Librería con arquitectura hexagonal para procesos financieros ETL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",  # Agrega la URL de tu repositorio GitHub aquí
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=2.3.1",
        "polars>=1.32.0",  # Para APIs que usan Polars
        "pydantic>=2.0.0",
        "requests>=2.25.0",
        "python-dateutil>=2.8.0",
        "openpyxl>=3.0.0",  # Para Excel
        "sqlalchemy>=1.4.0",  # Para bases de datos
        "numpy>=1.20.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            # Si tienes scripts de línea de comandos, agrégalos aquí
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
)
