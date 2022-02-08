"""
Session token storage mechanisms.

If available, the desktop keyring is used. Else a session token
(not the account password) will be stored in plaintext.
"""
import json
from typing import Optional, Type
import typer
from pathlib import Path
from packaging import version

import caw
from chris.types import CUBEAddress, CUBEToken
from caw.login.store import AbstractSecretStore, KeyringSecretStore, PlaintextSecretStore, use_keyring

PreferredSecretStore: Type[AbstractSecretStore] = KeyringSecretStore if use_keyring else PlaintextSecretStore
"""
``PreferredSecretStore`` is the :class:`KeyringSecretStore` if the :mod:`keyring` module is
available. Otherwise, :class:`PlaintextSecretStore` is used instead.
"""

default_config_file: Path = Path(typer.get_app_dir('caw')) / 'login.json'


class LoginManager:
    """
    A wrapper around an :class:`AbstractSecretStore` which handles saving of configurations.

    The configuration file is saved in ``~/.config/caw`` after each method call.
    """

    VERSION = caw.__version__

    def __init__(self, SecretStoreBackend: Type[AbstractSecretStore] = PreferredSecretStore,
                 config_file: Optional[Path] = default_config_file):
        self.__savefile = config_file
        self._initialize_config()

        with self.__savefile.open('r') as f:
            self._config = json.load(f)

        if 'secretStore' not in self._config:
            self._config['secretStore'] = dict()
        self._store = SecretStoreBackend(self._config['secretStore'])

    def _initialize_config(self):
        """
        Creates an empty configuration file on first run.

        If the configuration file already exists but its spec was written by
        a backwards-incompatible version, the configuration is deleted and
        recreated.
        """
        if self.__savefile.exists():
            if not self._config_file_is_sane():
                typer.secho(f'WARNING: config file {self.__savefile} was created by '
                            f'an incompatible version of {caw.pkg.metadata["name"]}.\n'
                            'It will be overwritten with an empty configuration.',
                            dim=True, err=True)
                self._write_empty_config()
        else:
            self.__savefile.parent.mkdir(parents=True, exist_ok=True)
            self._write_empty_config()

    def _config_file_is_sane(self) -> bool:
        """
        :return: True if the configuration file is valid JSON and its major version
                 spec is compatible with the current version of caw
        """
        with self.__savefile.open('r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                msg = f'CRITICAL: the file {self.__savefile} is not valid JSON.'
                typer.secho(msg, fg=typer.colors.RED, err=True)
                raise typer.Abort()

        if 'version' not in data:
            return False

        try:
            spec = version.Version(data['version'])
        except version.InvalidVersion:
            typer.secho(f'WARNING: invalid config version specified in {self.__savefile}.',
                        fg=typer.colors.RED, err=True)
            return False

        return spec.major == self.VERSION.major

    def _write_empty_config(self):
        """
        Overwrites the configuration file with an empty configuration.
        """
        self.__savefile.write_text(f'{{"version": "{self.VERSION}"}}')

    def get_default_address(self, address: Optional[CUBEAddress] = None) -> Optional[CUBEAddress]:
        if address is not None:
            return address
        if 'defaultAddress' not in self._config:
            return None
        return CUBEAddress(self._config['defaultAddress'])

    def _write_config(self):
        """
        Save login configuration to disk.
        """
        with self.__savefile.open('w') as f:
            json.dump(self._config, f)

    def get(self, address: Optional[CUBEAddress] = None) -> Optional[CUBEToken]:
        address = self.get_default_address(address)
        if not address:
            return None
        return CUBEToken(self._store.get(address))

    def logout(self, address: Optional[CUBEAddress] = None):
        """
        Remove secret from storage. If the address is the default address, then remove the default address as well.
        """
        address = self.get_default_address(address)
        if address == self.get_default_address() and 'defaultAddress' in self._config:
            del self._config['defaultAddress']

        self._store.clear(address)
        self._write_config()

    def login(self, address: CUBEAddress, token: CUBEToken):
        self._store.set(address, token)
        self._config['defaultAddress'] = address
        self._write_config()

        if not use_keyring and isinstance(self._store, PlaintextSecretStore):
            typer.secho(f'Login token was saved as plaintext in the file {self.__savefile}',
                        dim=True, err=True)
            typer.secho('For safer credentials storage, please run: '
                        '\n\n\tcaw logout'
                        '\n\tpip install keyring'
                        f'\n\tcaw --address {address} login\n', dim=True, err=True)
