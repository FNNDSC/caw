"""
A global variable namespace.
"""

import typer
from caw.login.manager import LoginManager
from caw.builder import ClientBuilder


login_manager = LoginManager()
build_client = ClientBuilder(login_manager)

app = typer.Typer(
    epilog='Examples and documentation at '
           'https://github.com/FNNDSC/caw#documentation'
)
