import typer

from caw.commands.store import app, build_client


@app.command()
def export(name: str = typer.Argument(..., help='Name of pipeline.')):
    """
    Deserialize a pipeline to JSON.
    """
    client = build_client()
    pipeline = client.get_pipeline(name)
    typer.echo(pipeline.deserialize())
