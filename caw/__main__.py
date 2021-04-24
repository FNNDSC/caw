import os
from importlib.metadata import metadata

import requests.exceptions
import typer
from chrisclient2.chrisclient import ChrisClient, ChrisIncorrectLoginError, \
    PipelineNotFoundError, run_pipeline_generator
from chrisclient2.models import Pipeline, PluginInstance
from typing import Optional, List
import logging
from pathlib import Path

from caw.movedata import upload as cube_upload, download as cube_download

# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

client: Optional[ChrisClient] = None

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
        address: str = typer.Option('http://localhost:8000/api/v1/', '--address', '-a', envvar='CHRIS_URL'),
        username: str = typer.Option('chris', '--username', '-u', envvar='CHRIS_USERNAME'),
        password: str = typer.Option('chris1234', '--password', '-p', envvar='CHRIS_PASSWORD'),
        version: Optional[bool] = typer.Option(None, '--version', '-V',
                                               callback=show_version, is_eager=True,
                                               help='Print version.')
):
    """
    A command line ChRIS client for pipeline execution and data management.
    """
    if 'CHRIS_TESTING' not in os.environ and password == 'chris1234':
        typer.secho('Using defaults (set CHRIS_TESTING=y to supress this message): '
                    f'{address}  {username}:{password}', dim=True, err=True)
    global client
    try:
        client = ChrisClient(address, username, password)
    except ChrisIncorrectLoginError as e:
        typer.secho(e.args[0])
        raise typer.Abort()
    except Exception:
        typer.secho('Connection error\n'
                    f'address:  {address}\n'
                    f'username: {username}', fg=typer.colors.RED, err=True)
        raise typer.Abort()


@app.command()
def search(name: str = typer.Argument('', help='name of pipeline to search for')):
    """
    Search for pipelines that are saved in ChRIS.
    """
    for pipeline in client.search_pipelines(name):
        typer.echo(f'{pipeline.url:<60}{typer.style(pipeline.name, bold=True)}')


def get_pipeline(name: str) -> Pipeline:
    try:
        return client.get_pipeline(name)
    except PipelineNotFoundError:
        typer.secho(f'Pipeline not found: "{pipeline}"', fg=typer.colors.RED, err=True)
        raise typer.Abort()


def run_pipeline(chris_pipeline: Pipeline, plugin_instance: PluginInstance):
    with typer.progressbar(run_pipeline_generator(pipeline=chris_pipeline, plugin_instance=plugin_instance),
                           length=len(chris_pipeline.pipings), label='Scheduling pipeline') as proto_pipeline:
        for _ in proto_pipeline:
            pass


@app.command()
def pipeline(name: str = typer.Argument(..., help='Name of pipeline to run.'),
             target: str = typer.Option(..., help='Plugin instance ID or URL.')):
    """
    Run a pipeline on an existing feed.
    """
    plugin_instance = client.get_plugin_instance(target)
    chris_pipeline = get_pipeline(name)
    run_pipeline(chris_pipeline=chris_pipeline, plugin_instance=plugin_instance)


@app.command()
def upload(
        threads: int = typer.Option(4, '--threads', '-t', help='Number of threads to use for file upload.'),
        create_feed: bool = typer.Option(True, help='Run pl-dircopy on the newly uploaded files.'),
        name: str = typer.Option('', '--name', '-n', help='Name of the feed.'),
        description: str = typer.Option('', '--description', '-d', help='Description of the feed.'),
        pipeline: str = typer.Option('', '--pipeline', '-p', help='Name of pipeline to run on the data.'),
        files: List[Path] = typer.Argument(..., help='Files to upload. '
                                                     'Folder upload is supported, but directories are destructured.')
):
    """
    Upload local files from host into ChRIS storage and then run pl-dircopy.
    """
    chris_pipeline: Optional[Pipeline] = None
    if pipeline:
        chris_pipeline = get_pipeline(pipeline)

    try:
        swift_path = cube_upload(client=client, files=files, upload_threads=threads)
    except requests.exceptions.RequestException:
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
    cube_download(client=client, url=url, destination=destination, threads=threads)


if __name__ == '__main__':
    app()
