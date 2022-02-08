import json
from typing import Generator, Any, TypedDict, Callable, TypeVar, List, Dict

import requests

from chris.cube.resource import CUBEResource
from chris.types import CUBEUrl

import logging

logger = logging.getLogger(__name__)


class UnrecognizedResponseException(Exception):
    pass


class TooMuchPaginationException(Exception):
    pass


T = TypeVar('T', bound=CUBEResource)


class JSONPaginatedResponse(TypedDict):
    count: int
    next: CUBEUrl
    previous: CUBEUrl
    results: List[Dict[str, Any]]


def fetch_paginated_objects(s: requests.Session,
                            url: CUBEUrl,
                            constructor=Callable[..., T],
                            max_requests=100
                            ) -> Generator[T, None, None]:
    for d in fetch_paginated_raw(s, url, max_requests):
        yield constructor(s=s, **d)


def fetch_paginated_raw(s: requests.Session,
                        url: CUBEUrl, max_requests: int
                        ) -> Generator[Dict[str, any], None, None]:
    """
    Produce all values from a paginated endpoint.

    :param s: session
    :param url: the paginated URI, optionally ending
                with the query-string ``?limit=N&offset=N&``
    :param max_requests: a quota on the number of requests
                         a call to this method may make in total
    """
    if max_requests <= 0:
        raise TooMuchPaginationException()

    logger.debug('%s', url)
    res = s.get(url)  # TODO pass qs params separately?
    res.raise_for_status()
    data = res.json()

    yield from __get_results_from(url, data)
    if data['next']:
        yield from fetch_paginated_raw(s, data['next'], max_requests - 1)


__PaginatedResponseKeys = frozenset(JSONPaginatedResponse.__annotations__)


# TODO in Python 3.10, we should use TypeGuard
# https://docs.python.org/3.10/library/typing.html#typing.TypeGuard
def __get_results_from(url: CUBEUrl, data: Any) -> List[Dict[str, Any]]:
    """
    Check that the response from a paginated endpoint is well-formed,
    and return the results.
    """
    if not isinstance(data, dict):
        logging.debug('Invalid response from %s\n'
                      'Was not parsed correctly into a dict.\n'
                      '%s',
                      url,
                      json.dumps(data, indent=4))
        raise UnrecognizedResponseException(f'Response from {url} is invalid.')

    if __PaginatedResponseKeys > frozenset(data.keys()):
        logging.debug('Invalid response from %s\n'
                      'dict keys did not match: %s\n'
                      '%s',
                      url,
                      str(__PaginatedResponseKeys),
                      json.dumps(data, indent=4))
        raise UnrecognizedResponseException(f'Response from {url} is invalid.')

    return data['results']
