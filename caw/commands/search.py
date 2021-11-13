import typer
from caw.commands.store import app, build_client


@app.command()
def search(name: str = typer.Argument('', help='name of pipeline to search for')):
    """
    Search for pipelines that are saved in ChRIS.
    """
    client = build_client()
    for search_result in client.search_pipelines(name):
        typer.echo(f'{search_result.url:<60}{typer.style(search_result.name, bold=True)}')
