from typing import Type, TypeVar
from serde import SerdeError
from serde.json import from_json
from requests import Response
from chris.errors import ResponseError


T = TypeVar("T")


def deserialize(t: Type[T], res: Response) -> T:
    res.raise_for_status()
    try:
        return from_json(t, res.text)
    except SerdeError as e:
        raise ResponseError(msg=str(e), body=res.text)
