from typing import Type, TypeVar, Iterable

T = TypeVar('T')


def peek(x: Iterable[T], mt: Type[Exception] = ValueError) -> T:
    for e in x:
        return e
    raise mt('x is empty')
