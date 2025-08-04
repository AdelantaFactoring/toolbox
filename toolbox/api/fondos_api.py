"""
🌐 Fondos API V2 - Interfaz unificada para fondos promocional y crecer
"""

from typing import Dict, Any, Union, Optional
import pandas as pd

try:
    from .fondo_promocional_api import (
        FondoPromocionalAPI,
        get_fondo_promocional,
    )
except ImportError as e:
    raise ImportError(
        f"FondoPromocionalAPI V2 requiere dependencias de imports relativos: {e}"
    )

try:
    from .fondo_crecer_api import (
        FondoCrecerAPI,
        get_fondo_crecer,
    )
except ImportError as e:
    raise ImportError(
        f"FondoCrecerAPI V2 requiere dependencias de imports relativos: {e}"
    )


# Funciones públicas unificadas (aliases para compatibilidad)
def get_promocional(
    as_df: bool = False, **kwargs
) -> Union[pd.DataFrame, Dict[str, Any]]:
    """
    Alias para get_fondo_promocional

    Args:
        as_df: Si retornar como DataFrame
        **kwargs: Parámetros adicionales

    Returns:
        DataFrame o diccionario con los datos del fondo promocional
    """
    return get_fondo_promocional(as_df=as_df, **kwargs)


async def get_promocional_async(
    as_df: bool = False, **kwargs
) -> Union[pd.DataFrame, Dict[str, Any]]:
    """
    Versión asíncrona de get_promocional (placeholder)

    Args:
        as_df: Si retornar como DataFrame
        **kwargs: Parámetros adicionales

    Returns:
        DataFrame o diccionario con los datos del fondo promocional
    """
    # Por ahora, usar la versión sincrónica
    # TODO: Implementar versión async real
    return get_promocional(as_df=as_df, **kwargs)


def get_crecer(as_df: bool = False, **kwargs) -> Union[pd.DataFrame, Dict[str, Any]]:
    """
    Alias para get_fondo_crecer

    Args:
        as_df: Si retornar como DataFrame
        **kwargs: Parámetros adicionales

    Returns:
        DataFrame o diccionario con los datos del fondo crecer
    """
    return get_fondo_crecer(as_df=as_df, **kwargs)


async def get_crecer_async(
    as_df: bool = False, **kwargs
) -> Union[pd.DataFrame, Dict[str, Any]]:
    """
    Versión asíncrona de get_crecer (placeholder)

    Args:
        as_df: Si retornar como DataFrame
        **kwargs: Parámetros adicionales

    Returns:
        DataFrame o diccionario con los datos del fondo crecer
    """
    # Por ahora, usar la versión sincrónica
    # TODO: Implementar versión async real
    return get_crecer(as_df=as_df, **kwargs)


# Aliases para compatibilidad
__all__ = [
    "FondoPromocionalAPI",
    "FondoCrecerAPI",
    "get_promocional",
    "get_promocional_async",
    "get_crecer",
    "get_crecer_async",
    "get_fondo_promocional",
    "get_fondo_crecer",
]
