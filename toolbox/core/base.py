"""
🎯 Base V2 - Clases base con funcionalidad común para arquitectura hexagonal

Contiene Base y BaseObtenerV2 para herencia múltiple y compatibilidad V1.
"""

import functools
import time

# from typing import Optional

try:
    from ..config.settings import V2Settings
except ImportError:
    raise ImportError("V2 base requires V2Settings from relative config")


class Base:
    """
    🏗️ Clase base V2 con funcionalidad común.

    Contiene únicamente el decorador timeit para minimizar duplicación de código
    en la arquitectura hexagonal.
    """

    @staticmethod
    def timeit(func):
        """Decorador para medir tiempo de ejecución con logging V2"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            t0 = time.time()
            result = func(*args, **kwargs)
            t1 = time.time()
            V2Settings.logger(
                f"Function {func.__name__} executed in {t1 - t0:.4f} seconds"
            )
            return result

        return wrapper
