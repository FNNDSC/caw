from typing import Optional, TypeVar, Iterable

T = TypeVar("T")


def peek(x: Iterable[T]) -> Optional[T]:
    return next(iter(x), None)
