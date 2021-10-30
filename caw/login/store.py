import abc
from typing import Optional

import logging

logger = logging.getLogger(__name__)


use_keyring = True
"""
``use_keyring`` is a :class:`bool` which denotes whether it is possible to use
:class:`KeyringSecretStore`.
"""

try:
    import keyring
    logger.info('Using keyring')
except ModuleNotFoundError:
    use_keyring = False
    logger.info('Using plaintext')


class AbstractSecretStore(abc.ABC):
    """
    A key-value data structure which hopefully stores its values securely.

    Implementations of ``AbstractSecretStore`` are given a :class:`dict` which
    the ``AbstractSecretStore`` may optionally use as a persistent key-value
    store for arbitrary metadata. However, it is the ``AbstractSecretStore``'s
    client's responsibility to read and write that :class:`dict` to disk, thus
    it is considered insecure.
    """

    def __init__(self, context: dict):
        """
        :param context: application settings which are expected to be saved
                        after the invocation of this object's methods
        """
        self.context = context

    @abc.abstractmethod
    def get(self, address: str) -> Optional[str]:
        ...

    @abc.abstractmethod
    def set(self, address: str, token: str):
        ...

    @abc.abstractmethod
    def clear(self, address: str):
        ...


class PlaintextSecretStore(AbstractSecretStore):
    """
    Insecure token storage in plaintext.
    This implementation should only be used when the keyring is not available.
    """
    def __init__(self, context: dict):
        super().__init__(context)
        if 'secrets' not in context:
            context['secrets'] = {}

    def get(self, address: str) -> Optional[str]:
        if address not in self.context['secrets']:
            return None
        return self.context['secrets'][address]

    def set(self, address: str, token: str):
        self.context['secrets'][address] = token

    def clear(self, address: str):
        del self.context['secrets'][address]


class KeyringSecretStore(AbstractSecretStore):
    """
    Secure token storage using the host desktop environment's login keyring.
    """

    __SPACE = 'org.chrisproject.caw'

    def get(self, address: str) -> Optional[str]:
        return keyring.get_password(self.__SPACE, address)

    def set(self, address: str, token: str):
        keyring.set_password(self.__SPACE, address, token)

    def clear(self, address: str):
        keyring.delete_password(self.__SPACE, address)
