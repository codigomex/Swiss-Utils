__all__ = ['immutable']

from typing import Any, Type, TypeVar, cast

T = TypeVar('T')


def immutable(cls: Type[T]) -> Type[T]:
    """
    Decorator that makes class instances read-only after __init__.

    Intended for classes that will NOT be subclassed. Subclassing breaks the
    immutability guarantee because child classes might not trigger the lock or
    could override __setattr__/__delattr__. Use only on final (non‑inherited)
    classes.
    """
    original_init = cls.__init__

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # 1. Allow the object to populate
        original_init(self, *args, **kwargs)
        # 2. Apply the lock (using base object to avoid triggering the error)
        object.__setattr__(self, '_locked', True)

    def __setattr__(self, name: str, value: Any) -> None:
        if getattr(self, '_locked', False):
            raise AttributeError(f'[@immutable] {cls.__name__} is read-only.')
        object.__setattr__(self, name, value)

    def __delattr__(self, name: str) -> None:
        raise AttributeError(
            f'[@immutable] Attributes cannot be deleted in {cls.__name__}.'
        )

    # Safe injections for Mypy
    setattr(cls, '__init__', __init__)
    setattr(cls, '__setattr__', __setattr__)
    setattr(cls, '__delattr__', __delattr__)

    return cast(Type[T], cls)
