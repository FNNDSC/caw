import os
import sys
import logging
from pathlib import Path
from typing import Optional, List

import typer
import requests.exceptions

from chris.types import CUBEAddress, CUBEUsername, CUBEPassword
from chris.models import Pipeline, InvalidFilesResourceUrlException

import caw
from caw.movedata import upload as cube_upload, download as cube_download
from caw.login.manager import LoginManager
from caw.globals import DEFAULT_ADDRESS, DEFAULT_USERNAME, DEFAULT_PASSWORD
from caw.builder import ClientBuilder
from caw.helpers import run_pipeline_with_progress


if 'CAW_DEBUG' in os.environ:
    logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


login_manager = LoginManager()
precursor = ClientBuilder(login_manager)

app = typer.Typer(
    epilog='Examples and documentation at '
           'https://github.com/FNNDSC/caw#documentation'
)


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
def main(
        address: str = typer.Option(DEFAULT_ADDRESS, '--address', '-a', envvar='CHRIS_URL'),
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
    global precursor
    precursor.address = CUBEAddress(address)
    precursor.username = CUBEUsername(username)
    precursor.password = CUBEPassword(password)


@app.command()
def login(read_pass: bool = typer.Option(False, '--password-stdin', help='Take the password from stdin')):
    """
    Login to ChRIS.
    """

    if not precursor.username:
        precursor.username = CUBEUsername(typer.prompt('username'))

    if not precursor.password:
        if read_pass:
            precursor.password = CUBEPassword(sys.stdin.read().rstrip('\n'))
        else:
            precursor.password = typer.prompt('password', hide_input=True)

    client = precursor()
    login_manager.login(client.addr, client.token)


@app.command()
def logout():
    """
    Remove your login credentials.
    """
    if precursor.address == DEFAULT_ADDRESS:
        login_manager.logout()
    else:
        login_manager.logout(precursor.address)


@app.command()
def search(name: str = typer.Argument('', help='name of pipeline to search for')):
    """
    Search for pipelines that are saved in ChRIS.
    """
    client = precursor()
    for search_result in client.search_pipelines(name):
        typer.echo(f'{search_result.url:<60}{typer.style(search_result.name, bold=True)}')


@app.command()
def pipeline(name: str = typer.Argument(..., help='Name of pipeline to run.'),
             target: str = typer.Option(..., help='Plugin instance ID or URL.')):
    """
    Run a pipeline on an existing feed.
    """
    client = precursor()
    plugin_instance = client.get_plugin_instance(target)
    chris_pipeline = client.get_pipeline(name)
    run_pipeline_with_progress(chris_pipeline=chris_pipeline, plugin_instance=plugin_instance)


@app.command()
def upload(
        threads: int = typer.Option(4, '--threads', '-t', help='Number of threads to use for file upload.'),
        create_feed: bool = typer.Option(True, help='Run pl-dircopy on the newly uploaded files.'),
        name: str = typer.Option('', '--name', '-n', help='Name of the feed.'),
        description: str = typer.Option('', '--description', '-d', help='Description of the feed.'),
        pipeline_name: str = typer.Option('', '--pipeline', '-p', help='Name of pipeline to run on the data.'),
        files: List[Path] = typer.Argument(..., help='Files to upload. '
                                                     'Folder upload is supported, but directories are destructured.')
):
    """
    Upload local files and run pl-dircopy.
    """
    client = precursor()
    chris_pipeline: Optional[Pipeline] = None
    if pipeline_name:
        chris_pipeline = client.get_pipeline(pipeline_name)

    try:
        swift_path = cube_upload(client=client, files=files, upload_threads=threads)
    except requests.exceptions.RequestException as e:
        logger.debug('RequestException: %s\n%s', str(e), e.response.text)
        typer.secho('Upload unsuccessful', fg=typer.colors.RED, err=True)
        raise typer.Abort()

    if not create_feed:
        raise typer.Exit()

    dircopy_instance = client.run('pl-dircopy', params={'dir': swift_path})
    if name:
        dircopy_instance.get_feed().set_name(name)
    if description:
        dircopy_instance.get_feed().set_description(description)

    if chris_pipeline:
        run_pipeline_with_progress(chris_pipeline=chris_pipeline, plugin_instance=dircopy_instance)
    typer.echo(dircopy_instance.feed)


@app.command()
def download(
        threads: int = typer.Option(4, '--threads', '-t', help='Number of concurrent downloads.'),
        url: str = typer.Argument(..., help='ChRIS files API resource URL'),
        destination: Path = typer.Argument(..., help='Location on host where to save downloaded files.')
):
    """
    Download everything from a ChRIS url.
    """
    client = precursor()
    try:
        cube_download(client=client, url=url, destination=destination, threads=threads)
    except InvalidFilesResourceUrlException as e:
        typer.secho(str(e), fg=typer.colors.RED, err=True)
        raise typer.Abort()


if __name__ == '__main__':
    app()
