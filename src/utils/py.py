from typing import Any, Type, TypeVar, cast

T = TypeVar("T")


def inmutable(cls: Type[T]) -> Type[T]:
    """
    Decorador que permite inicializar la clase pero bloquea
    cualquier cambio o borrado posterior.
    """
    original_init = cls.__init__

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # 1. Dejamos que el objeto se llene
        original_init(self, *args, **kwargs)
        # 2. Le ponemos el candado (usando la base para no disparar el error)
        object.__setattr__(self, "_bloqueado", True)

    def __setattr__(self, name: str, value: Any) -> None:
        if getattr(self, "_bloqueado", False):
            raise AttributeError(f"[@inmutable] {cls.__name__} es de solo lectura.")
        object.__setattr__(self, name, value)

    def __delattr__(self, name: str) -> None:
        raise AttributeError(
            f"[@inmutable] No se pueden borrar atributos en {cls.__name__}."
        )

    # Inyecciones seguras para Mypy
    setattr(cls, "__init__", __init__)
    setattr(cls, "__setattr__", __setattr__)
    setattr(cls, "__delattr__", __delattr__)

    return cast(Type[T], cls)
