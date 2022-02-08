from pathlib import Path
import typer
from caw.commands.store import app, build_client
from caw.movedata import download as cube_download

from chris.types import CUBEUrl
from chris.cube.pagination import UnrecognizedResponseException

from caw.constants import DEFAULT_ADDRESS
from caw.commands.helpers import api_address


@app.command()
def download(
        threads: int = typer.Option(4, '--threads', '-t', help='Number of concurrent downloads.'),
        url: str = typer.Argument(..., help='ChRIS files API resource URL'),
        destination: Path = typer.Argument(..., help='Location on host where to save downloaded files.')
):
    """
    Download everything from a ChRIS url.
    """
    base_address = api_address(CUBEUrl(url))
    if base_address != build_client.address:
        if build_client.address != DEFAULT_ADDRESS:
            given_address = typer.style(f'--address={build_client.address}',
                                        fg=typer.colors.GREEN, bold=True)
            download_url = typer.style(url, fg=typer.colors.YELLOW, bold=True)
            typer.echo(f'Given {given_address} is different '
                       f'from download URL: {download_url}', err=True)
            raise typer.Abort()
        build_client.address = base_address

    client = build_client()

    try:
        cube_download(client=client, url=url, destination=destination, threads=threads)
    except UnrecognizedResponseException as e:  # TODO different error please
        typer.secho(str(e), fg=typer.colors.RED, err=True)
        raise typer.Abort()
