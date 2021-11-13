from caw.commands.store import app, build_client, login_manager
from caw.constants import DEFAULT_ADDRESS


@app.command()
def logout():
    """
    Remove your login credentials.
    """
    if build_client.address == DEFAULT_ADDRESS:
        login_manager.logout()
    else:
        login_manager.logout(build_client.address)
