import json
from typing import Generator, Any, TypedDict, Type, TypeVar
from chris.cube.resource import CUBEResource
from chris.errors import UnrecognizedResponseError, TooMuchPaginationError
from chris.types import CUBEUrl

import logging

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=CUBEResource)


class JSONPaginatedResponse(TypedDict):
    count: int
    next: CUBEUrl
    previous: CUBEUrl
    results: list[dict[str, Any]]
    collection_links: dict[str, CUBEUrl]


class PaginatedResource(CUBEResource):

    __PaginatedResponseKeys = frozenset(JSONPaginatedResponse.__annotations__)

    def fetch_paginated_objects(self, url: CUBEUrl, constructor=Type[T], max_requests=100
                                ) -> Generator[T, None, None]:
        yield from (constructor(s=self.s, **d) for d in self.fetch_paginated_raw(url, max_requests))

    def fetch_paginated_raw(self, url: CUBEUrl, max_requests: int
                            ) -> Generator[dict[str, any], None, None]:
        """
        Produce all values from a paginated endpoint.

        :param url: the paginated URI, optionally ending
                    with the query-string ``?limit=N&offset=N&``
        :param max_requests: a quota on the number of requests
                             a call to this method may make in total
        """
        if max_requests <= 0:
            raise TooMuchPaginationError()

        res = self.s.get(url)
        res.raise_for_status()
        data = res.json()

        yield from self.__get_results_from(url, data)
        if data['next']:
            print(data['next'])
            yield from self.fetch_paginated_raw(data['next'], max_requests - 1)

    # TODO in Python 3.10, we should use TypeGuard
    # https://docs.python.org/3.10/library/typing.html#typing.TypeGuard
    @classmethod
    def __get_results_from(cls, url: CUBEUrl, data: Any) -> list[dict[str, Any]]:
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
            raise UnrecognizedResponseError(f'Response from {url} is invalid.')

        if not frozenset(data.keys()) == cls.__PaginatedResponseKeys:
            logging.debug('Invalid response from %s\n'
                          'dict keys did not match: %s\n'
                          '%s',
                          url,
                          str(cls.__PaginatedResponseKeys),
                          json.dumps(data, indent=4))
            raise UnrecognizedResponseError(f'Response from {url} is invalid.')

        return data['results']
