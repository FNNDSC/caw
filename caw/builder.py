"""
This file eases usage of the Python chris.client and Typer.
"""
import os
from typing import Optional, Tuple

import typer

from chris.cube.pipeline import Pipeline
from chris.client import ChrisClient
from chris.errors import ChrisIncorrectLoginError, PipelineNotFoundError

from chris.types import CUBEAddress, CUBEToken, CUBEUsername, CUBEPassword
from caw.constants import DEFAULT_ADDRESS, DEFAULT_USERNAME, DEFAULT_PASSWORD

from caw.login.manager import LoginManager

import logging
logger = logging.getLogger(__name__)


class FriendlyClient(ChrisClient):
    """
    A ``ChrisClient`` which shows (less helpful) error messages instead of exceptions.
    """
    def get_pipeline(self, name: str) -> Pipeline:
        try:
            return super().get_pipeline(name)
        except PipelineNotFoundError:
            typer.secho(f'Pipeline not found: "{name}"', fg=typer.colors.RED, err=True)
            raise typer.Abort()


class ClientBuilder:
    """
    A workaround so that the ChrisClient object's constructor, which attempts to use the login
    credentials, is called by the subcommand instead of the main callback.

    This is necessary to support the ``caw login`` subcommand.
    """
    def __init__(self, login_manager: LoginManager):
        self.login_manager = login_manager
        self.address: Optional[CUBEAddress] = None
        self.username: Optional[CUBEUsername] = None
        self.password: Optional[CUBEPassword] = None

    def _determine_address(self, given_address: Optional[CUBEAddress]) -> CUBEAddress:
        if given_address:
            return given_address
        saved_address = self.login_manager.get_default_address()
        if saved_address:
            return saved_address
        return DEFAULT_ADDRESS

    def _determine_login_method(self, address: CUBEAddress) \
            -> Tuple[Optional[CUBEToken], Optional[CUBEUsername], Optional[CUBEPassword]]:
        """
        Determines whether to use token auth, or username+password auth.

        1. If user explicitly specifies a username and password, then use them.
        2. If neither username nor password given, then check if they're logged in and get the token.
        3. If user is not logged in and does not give username nor password, then use default username and password.

        :param address: address of ChRIS to log into
        :return: token, username, password
        """
        if self.username and not self.password:
            typer.echo('Given a username but no password. You must supply both.', err=True)
            raise typer.Abort()
        if self.password and not self.username:
            typer.echo('Given a password but no username. You must supply both.', err=True)
            raise typer.Abort()

        if self.username and self.password:
            return None, self.username, self.password

        token = self.login_manager.get(address)
        if token:
            return token, None, None

        return None, DEFAULT_USERNAME, DEFAULT_PASSWORD

    @staticmethod
    def _create_client_with(address: CUBEAddress, token: Optional[CUBEToken],
                            username: Optional[CUBEUsername], password: Optional[CUBEPassword]) -> FriendlyClient:
        """
        Use token authentication if given a token. Otherwise, use username and password.
        """
        if token:
            return FriendlyClient(address=address, token=token)
        return FriendlyClient.from_login(address=address, username=username, password=password)

    def __call__(self) -> FriendlyClient:
        """
        Authenticate with ChRIS and construct the client object.

        In general, it works like this:

        1. First try to use user-specified values.
        2. For any value not specified, check to see if they're logged in and use their existing session.
        3. As a last resort, use defaults (e.g. chris:chris1234 on http://localhost:8000/api/v1/)

        :return: client object
        """
        address = self._determine_address(self.address)
        token, username, password = self._determine_login_method(address)
        self._print_debug(address, token, username, password)

        try:
            return self._create_client_with(address, token, username, password)
        except ChrisIncorrectLoginError as e:
            self._handle_incorrect_login(e, address, token)
        # except Exception as e:
        #     typer.secho('Unknown connection error', fg=typer.colors.RED, err=True)
        #     typer.echo(str(e), err=True)
        #     raise typer.Abort()

    def _handle_incorrect_login(self, e: ChrisIncorrectLoginError, address: CUBEAddress,
                                token: Optional[CUBEToken] = None):
        typer.secho(f'Authentication failed for {address}.', err=True)
        typer.secho(str(e), err=True)

        if token:
            typer.secho(f'warning: removing saved login for {address}.\n'
                        f'To login again, run\n'
                        f"\n\tcaw --address '{address}' login", err=True)
            self.login_manager.logout(address)
        raise typer.Abort()

    @staticmethod
    def _print_debug(address: CUBEAddress, token: Optional[CUBEToken],
                     username: Optional[CUBEUsername], password: Optional[CUBEPassword]):
        if token:
            logger.debug('HTTP token: "%s"', token)
            return
        if password == DEFAULT_PASSWORD and 'CHRIS_TESTING' not in os.environ:
            typer.secho('Using defaults (set CHRIS_TESTING=y to suppress this message): '
                        f'{address}  {username}:{password}', dim=True, err=True)
            return
        logger.debug('Using HTTP basic auth with given username and password.')
        logger.debug('address=%s username=%s', address, username)
