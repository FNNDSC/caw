import time
from typing import Callable, TypeVar, Iterable, Optional, Union, FrozenSet, Generator, Type
import requests

from chris.types import CUBEAddress
from chris.errors import WaitTimeoutException


T = TypeVar('T')


def __optional2set(c: Optional[Union[T, Iterable[T]]]) -> FrozenSet[T]:
    if c is None:
        c = []
    elif not isinstance(c, Iterable):
        c = [c]
    return frozenset(c)


def block_until(poller: Callable[[], T],
                not_ready_exception: Optional[Union[Type[Exception], Iterable[Type[Exception]]]] = None,
                interval: float = 2.0,
                timeout: float = 300
                ) -> Generator[Union[Exception, T], None, None]:
    """
    Blocks until a "ready" event by repeatedly polling using a function.

    The given polling function may either raise an allowed exception or produce a return value.

    A client should iterate over ``block_until`` using a loop, and break when ``block_until``
    yields an acceptable return value.

    Example:

    .. code-block:: python

        for poll in block_until(poller=do_request):
            if poll == 'OK':
                break


    :param poller: the function to call which polls the service
    :param not_ready_exception: a set of Exceptions which the poller may raise, indicating the
                                service is not "ready"
    :param interval: number of seconds to wait between poll
    :param timeout: maximum amount of time to wait
    :return: a Generator which yields the exceptions or return values produced when invoking the poller
    """

    if timeout <= 0:
        raise ValueError('timeout must be in the range (0, inf)')
    if interval <= 0:
        raise ValueError('interval must be in the range (0, inf)')

    permissible_exceptions = __optional2set(not_ready_exception)

    elapsed = 0
    while elapsed <= timeout:
        try:
            yield poller()
        except Exception as e:
            if e.__class__ in permissible_exceptions:
                yield e
                continue
            raise e
        finally:
            time.sleep(interval)
            elapsed += interval
    raise WaitTimeoutException(f'Timeout reached after {timeout} seconds')


def __expected_response_from_users(users_url: str) -> dict:
    return {
        'collection': {
            'version': '1.0',
            'href': users_url,
            'items': [],
            'links': [],
            'template': {
                'data': [
                    {'name': 'username', 'value': ''},
                    {'name': 'password', 'value': ''},
                    {'name': 'email', 'value': ''}
                ]
            },
            'total': 0
        }
    }


def wait_until_ready(url: CUBEAddress) -> Generator[None, None, None]:
    """
    Wait for the ChRIS backend service to be ready to accept connections by polling the
    ``/api/v1/users/`` endpoint.

    :param url: address of ChRIS backend
    :return: a Generator which produces the errors or responses from polling
    """
    if url.endswith('api/v1/'):
        url += 'users/'

    session = requests.Session()
    session.headers.update({
        'Accept': 'application/vnd.collection+json'
    })

    expected = __expected_response_from_users(url)

    def poll_user() -> bool:
        return session.get(url=url).json()

    for res in block_until(poller=poll_user, not_ready_exception=requests.exceptions.ConnectionError,
                           interval=2.0, timeout=300.0):
        if isinstance(res, dict) and res == expected:
            break
        yield res
