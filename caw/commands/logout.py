import typer

from caw.commands.store import app, build_client, login_manager
from caw.constants import DEFAULT_ADDRESS


@app.command()
def logout():
    """
    Remove your login credentials.
    """
    addr = None if build_client.address == DEFAULT_ADDRESS else build_client.address
    if login_manager.get(addr) is None:
        typer.echo('Not logged in.', err=True)
    else:
        login_manager.logout(addr)
