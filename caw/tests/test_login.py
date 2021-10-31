import unittest
from unittest.mock import Mock

import json
from pathlib import Path

from chris.types import CUBEAddress, CUBEToken
from caw.login.store import AbstractSecretStore, KeyringSecretStore, PlaintextSecretStore, use_keyring
from caw.login.manager import LoginManager

from tempfile import NamedTemporaryFile


class TestSecretStore(unittest.TestCase):
    def can_save_clear(self, store: AbstractSecretStore):
        store.set('http://localhost:8910/api/v1/', 'abcdefg')
        stored = store.get('http://localhost:8910/api/v1/')
        self.assertEqual(stored, 'abcdefg',
                         msg='Stored secret does not match what was originally set.')
        store.clear('http://localhost:8910/api/v1/')
        self.assertIsNone(store.get('http://localhost:8910/api/v1/'),
                          msg='store.clear did not work.')

    @unittest.skipUnless(use_keyring, 'keyring not supported')
    def test_keyring(self):
        self.can_save_clear(KeyringSecretStore({}))

    def test_plaintext(self):
        self.can_save_clear(PlaintextSecretStore({}))


class TestLoginManager(unittest.TestCase):

    def setUp(self) -> None:
        with NamedTemporaryFile(suffix='.json', delete=True) as self.savefile:
            pass
        self.savefile = Path(self.savefile.name)
        self.store: Mock = Mock(spec=AbstractSecretStore)
        wrapper = Mock(return_value=self.store, spec=AbstractSecretStore.__init__)
        self.lm = LoginManager(wrapper, self.savefile)  # type: ignore

    def getJson(self) -> dict:
        """
        Load the file written to by the ``LoginManager``.
        """
        with self.savefile.open('r') as f:
            return json.load(f)

    def test_default_address(self):
        self.lm.login(CUBEAddress('https://example.com/api/v1/'), CUBEToken('berry'))
        self.store.set.assert_called_once_with(CUBEAddress('https://example.com/api/v1/'), CUBEToken('berry'))

        content = self.getJson()
        self.assertIn('defaultAddress', content,
                      msg='Login manager did not set the CUBE address as default.')
        self.assertEqual(content['defaultAddress'], 'https://example.com/api/v1/',
                         msg='Default address is incorrect.')

        self.store.get = Mock(return_value='berry')
        self.assertEqual(self.lm.get(), CUBEToken('berry'),
                         msg='Retrieved password for default CUBE address is incorrect.')

        self.lm.logout()
        self.store.clear.assert_called_once_with('https://example.com/api/v1/')
        self.assertNotIn('defaultAddress', self.getJson(),
                         msg='Default address not removed after logout.')
