from pathlib import Path
from typing import Optional, List
import logging

import typer
import requests

from chris.cube.pipeline import Pipeline
from caw.commands.store import app, build_client
from caw.movedata import upload as cube_upload
from caw.run_pipeline import run_pipeline_with_progress

logger = logging.getLogger(__name__)


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
    client = build_client()
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
