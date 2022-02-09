from typing import Optional
import typer

from chris.types import CUBEAddress, CUBEUsername, CUBEPassword
import caw
from caw.commands.store import app, build_client
from caw.constants import DEFAULT_ADDRESS, DEFAULT_USERNAME, DEFAULT_PASSWORD


def show_version(value: bool):
    """
    Print version.
    """
    if not value:
        return
    typer.echo(f'{caw.pkg.metadata["name"]} {caw.__version__}')
    raise typer.Exit()


# noinspection PyUnusedLocal
@app.callback()
def entry(
        address: str = typer.Option(None, '--address', '-a', envvar='CHRIS_URL'),
        username: Optional[str] = typer.Option(
            None, '--username', '-u', envvar='CHRIS_USERNAME',
            help='Username of your ChRIS user account.'),
        password: Optional[str] = typer.Option(
            None, '--password', '-p', envvar='CHRIS_PASSWORD',
            help='Password of your ChRIS user account. '
            'If neither username nor password are specified, then the default '
            f'account "{DEFAULT_USERNAME}:{DEFAULT_PASSWORD}" is used.'),
        version: Optional[bool] = typer.Option(
            None, '--version', '-V', callback=show_version, is_eager=True, help='Print version.')
):
    """
    A command line ChRIS client for pipeline execution and data management.
    """
    build_client.address = CUBEAddress(address)
    build_client.username = CUBEUsername(username)
    build_client.password = CUBEPassword(password)
