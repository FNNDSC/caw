"""
Pagination helpers.
"""

from dataclasses import dataclass
from typing import (
    Generator,
    Any,
    TypedDict,
    TypeVar,
    List,
    Dict,
    Callable,
    Iterable,
    Generic,
    Sized,
    Type,
)
from chris.helpers.connected_resource import ConnectedResource
from requests import Session

T = TypeVar("T", bound=ConnectedResource)


@dataclass(frozen=True)
class Paginated(Generic[T], Iterable[T], Sized):
    """
    An iterable object which yields items from a paginated collection,
    making lazy requests as needed.

    Getting the `len` of a `Paginated` makes a request with `limit=0`
    and returns the `count` of the paginated collection.
    This makes it convenient to wrap `Paginated` with
    [tqdm](https://github.com/tqdm/tqdm).
    """

    item: Type[T]
    """Type of items in the collection"""
    url: str
    """URL of paginated collection, optionally with the query string `limit=N&offset=N`"""
    session: Session

    def __len__(self) -> int:
        res = self.session.get(self.url, params={"limit": 0})
        data: _JSONPaginatedResponse = res.json()
        return data["count"]

    def __iter__(self) -> Generator[T, None, None]:
        return fetch_paginated_objects(
            session=self.session, url=self.url, constructor=self.item.deserialize
        )


def fetch_paginated_objects(
    session: Session, url: str, constructor: Callable[[Dict[str, Any], Session], T]
) -> Generator[T, None, None]:
    """
    Produce all values from a paginated endpoint, making lazy requests as needed.

    Parameters:
    -----------
    session : requests.Session
    url : str
        paginated URL, optionally with the query string `limit=N&offset=N`
    constructor: [Dict[str, Any], Session] -> T
        deserializer for yield type
    """
    for d in fetch_paginated_raw(session, url):
        yield constructor(d, session)


def fetch_paginated_raw(
    session: Session, url: str
) -> Generator[Dict[str, Any], None, None]:
    """
    Helper function which yields the items from a paginated collection.
    """
    res = session.get(url)
    res.raise_for_status()
    data = res.json()

    yield from __get_results_from(url, data)
    if data["next"]:
        yield from fetch_paginated_raw(session, data["next"])


class _JSONPaginatedResponse(TypedDict):
    count: int
    next: str
    previous: str
    results: List[Dict[str, Any]]


__PaginatedResponseKeys = frozenset(_JSONPaginatedResponse.__annotations__)


def __get_results_from(url: str, data: Any) -> List[Dict[str, Any]]:
    """
    Check that the response from a paginated endpoint is well-formed,
    and return the results.
    """
    if not isinstance(data, dict) or __PaginatedResponseKeys > frozenset(data.keys()):
        raise UnrecognizedResponseException(url, data)
    return data["results"]


@dataclass(frozen=True)
class UnrecognizedResponseException(Exception):
    """
    Raised when CUBE response could not be deserialized.
    """

    url: str
    data: Any

    def __str__(self) -> str:
        return f"Invalid response from {repr(self.url)}: {repr(self.data)}"
