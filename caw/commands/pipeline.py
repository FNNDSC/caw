import typer

from caw.commands.store import app, build_client
from caw.run_pipeline import run_pipeline_with_progress


@app.command()
def pipeline(name: str = typer.Argument(..., help='Name of pipeline to run.'),
             target: str = typer.Option(..., help='Plugin instance ID or URL.')):
    """
    Run a pipeline on an existing feed.
    """
    client = build_client()
    plugin_instance = client.get_plugin_instance(target)
    chris_pipeline = client.get_pipeline(name)
    run_pipeline_with_progress(chris_pipeline=chris_pipeline, plugin_instance=plugin_instance)
