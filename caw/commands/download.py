from pathlib import Path
import typer
from caw.commands.store import app, build_client
from caw.movedata import download as cube_download

from chris.cube.pagination import UnrecognizedResponseException


@app.command()
def download(
        threads: int = typer.Option(4, '--threads', '-t', help='Number of concurrent downloads.'),
        url: str = typer.Argument(..., help='ChRIS files API resource URL'),
        destination: Path = typer.Argument(..., help='Location on host where to save downloaded files.')
):
    """
    Download everything from a ChRIS url.
    """
    client = build_client()
    try:
        cube_download(client=client, url=url, destination=destination, threads=threads)
    except UnrecognizedResponseException as e:  # TODO different error please
        typer.secho(str(e), fg=typer.colors.RED, err=True)
        raise typer.Abort()
