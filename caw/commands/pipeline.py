import typer

from caw.commands.store import app, build_client
from caw.run_pipeline import run_pipeline_with_progress


@app.command()
def pipeline(name: str = typer.Argument(..., help='Name of pipeline to run.'),
             target: str = typer.Option(..., help='Plugin instance ID or URL.')):
    """
    Run a pipeline on an existing feed. The URLs of the created plugin instances are printed out.
    """
    client = build_client()
    plugin_instance = client.get_plugin_instance(target)
    chris_pipeline = client.get_pipeline(name)

    for p in run_pipeline_with_progress(chris_pipeline=chris_pipeline, parent=plugin_instance):
        typer.echo(p.url)
