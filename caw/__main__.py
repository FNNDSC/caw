import os
from importlib.metadata import metadata

import requests.exceptions
import typer
from chris.client import ChrisClient, ChrisIncorrectLoginError, PipelineNotFoundError
from chris.models import Pipeline, PluginInstance, InvalidFilesResourceUrlException
from typing import Optional, List
import logging
from pathlib import Path

from caw.movedata import upload as cube_upload, download as cube_download
from caw.login import LoginManager, NotLoggedInError


if 'CAW_DEBUG' in os.environ:
    logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


DEFAULT_ADDRESS = 'http://localhost:8000/api/v1/'
DEFAULT_USERNAME = 'chris'
DEFAULT_PASSWORD = 'chris1234'

login_manager = LoginManager()


class ClientPrecursor:
    """
    A workaround so that the ChrisClient object's constructor, which attempts to use the login
    credentials, is called by the subcommand instead of the main callback.

    This is necessary to support the ``caw login`` subcommand.
    """
    def __init__(self):
        self.address = None
        self.username = None
        self.password = None
        self.token = None

    def __call__(self) -> ChrisClient:
        """
        Authenticate with ChRIS and construct the client object.

        Login strategy:
        1. First, use given credentials.
        2. If credentials not specified, use saved login.

        :return: client object
        """
        if not self.address:
            raise ValueError('Must specify CUBE address.')

        if self.password == DEFAULT_PASSWORD:  # assume default options are being used
            try:
                self.token = login_manager.get() if self.address == DEFAULT_ADDRESS else login_manager.get(self.address)
            except NotLoggedInError:
                if 'CHRIS_TESTING' not in os.environ:
                    typer.secho('Using defaults (set CHRIS_TESTING=y to suppress this message): '
                                f'{self.address}  {self.username}:{self.password}', dim=True, err=True)

        try:
            if self.token:
                logger.debug('HTTP token: "%s"', self.token)
                return ChrisClient(self.address, token=self.token)
            else:
                return ChrisClient(self.address, username=self.username, password=self.password)
        except ChrisIncorrectLoginError as e:
            typer.secho(e.args[0], err=True)
            raise typer.Abort()
        except Exception:
            typer.secho('Connection error\n'
                        f'address:  {self.address}\n'
                        f'username: {self.username}', fg=typer.colors.RED, err=True)
            raise typer.Abort()


precursor = ClientPrecursor()

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
    program_info = metadata(__package__)
    typer.echo(program_info['version'])
    raise typer.Exit()


@app.callback()
def main(
        address: str = typer.Option(DEFAULT_ADDRESS, '--address', '-a', envvar='CHRIS_URL'),
        username: str = typer.Option(DEFAULT_USERNAME, '--username', '-u', envvar='CHRIS_USERNAME'),
        password: str = typer.Option(DEFAULT_PASSWORD, '--password', '-p', envvar='CHRIS_PASSWORD'),
        version: Optional[bool] = typer.Option(None, '--version', '-V',
                                               callback=show_version, is_eager=True,
                                               help='Print version.')
):
    """
    A command line ChRIS client for pipeline execution and data management.
    """
    global precursor
    precursor.address = address
    precursor.username = username
    precursor.password = password


####################
# LOGIN COMMANDS
####################


@app.command()
def login():
    """
    Login to ChRIS.
    """
    if precursor.username == DEFAULT_USERNAME:
        precursor.username = typer.prompt('username')
    if precursor.password == DEFAULT_PASSWORD:
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


####################
# HELPER FUNCTIONS
####################


def find_pipeline(client: ChrisClient, name: str) -> Pipeline:
    """
    Helper to call ``client.get_pipeline(name)`` within a try/except block.
    :param client:
    :param name:
    :return:
    """
    try:
        return client.get_pipeline(name)
    except PipelineNotFoundError:
        typer.secho(f'Pipeline not found: "{pipeline}"', fg=typer.colors.RED, err=True)
        raise typer.Abort()


def run_pipeline(chris_pipeline: Pipeline, plugin_instance: PluginInstance):
    """
    Helper to execute a pipeline with a progress bar.
    """
    with typer.progressbar(plugin_instance.append_pipeline(chris_pipeline),
                           length=len(chris_pipeline.pipings), label='Scheduling pipeline') as proto_pipeline:
        for _ in proto_pipeline:
            pass


####################
# ACTION COMMANDS
####################


@app.command()
def search(name: str = typer.Argument('', help='name of pipeline to search for')):
    """
    Search for pipelines that are saved in ChRIS.
    """
    client = precursor()
    for pipeline in client.search_pipelines(name):
        typer.echo(f'{pipeline.url:<60}{typer.style(pipeline.name, bold=True)}')


@app.command()
def pipeline(name: str = typer.Argument(..., help='Name of pipeline to run.'),
             target: str = typer.Option(..., help='Plugin instance ID or URL.')):
    """
    Run a pipeline on an existing feed.
    """
    client = precursor()
    plugin_instance = client.get_plugin_instance(target)
    chris_pipeline = find_pipeline(client, name)
    run_pipeline(chris_pipeline=chris_pipeline, plugin_instance=plugin_instance)


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
        chris_pipeline = find_pipeline(client, pipeline_name)

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

    if not chris_pipeline:
        typer.echo(dircopy_instance.url)
        raise typer.Exit()
    run_pipeline(chris_pipeline=chris_pipeline, plugin_instance=dircopy_instance)


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
