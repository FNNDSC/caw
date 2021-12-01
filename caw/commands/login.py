import sys
import typer
from chris.types import CUBEUsername, CUBEPassword
from caw.commands.store import app, build_client, login_manager


@app.command()
def login(read_pass: bool = typer.Option(False, '--password-stdin', help='Take the password from stdin')):
    """
    Login to ChRIS.
    """

    if not build_client.username:
        build_client.username = CUBEUsername(typer.prompt('username'))

    if not build_client.password:
        if read_pass:
            build_client.password = CUBEPassword(sys.stdin.read().rstrip('\n'))
        else:
            build_client.password = typer.prompt('password', hide_input=True)

    client = build_client()
    login_manager.login(client.address, client.token)
