"""
Pagination helpers.
"""

from dataclasses import dataclass
from typing import Generator, Any, TypedDict, TypeVar, List, Dict, Callable

from requests import Session


@dataclass(frozen=True)
class UnrecognizedResponseException(Exception):
    """
    Raised when CUBE response could not be deserialized.
    """

    url: str
    data: Any

    def __str__(self) -> str:
        return f"Invalid response from {repr(self.url)}: {repr(self.data)}"


T = TypeVar("T")


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
    for d in _fetch_paginated_raw(session, url):
        yield constructor(d, session)


def _fetch_paginated_raw(
    session: Session, url: str
) -> Generator[Dict[str, Any], None, None]:
    res = session.get(url)
    res.raise_for_status()
    data = res.json()

    yield from __get_results_from(url, data)
    if data["next"]:
        yield from _fetch_paginated_raw(session, data["next"])


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
