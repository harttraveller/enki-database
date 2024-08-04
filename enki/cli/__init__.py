import typer
import webbrowser
from rich import print
from pycooltext import cooltext
from enki.__meta__ import __module__, __version__, __docs__
from enki import loc
from enki.cli import cache

app = typer.Typer()
app.add_typer(cache.app)


@app.callback(name=__module__, invoke_without_command=True)
def callback(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        cooltext(__module__)
        metadata = f"[deep_sky_blue1]Version:[/deep_sky_blue1] [turquoise2]{__version__}[/turquoise2] | "
        if loc.database.exists():
            metadata += "[green]Local DB Available[/green]"
        else:
            metadata += "[red]Local DB Not Found[/red]"
        print(metadata)


@app.command()
def docs():
    """Open the docs site in your default web browser."""
    webbrowser.open(__docs__)
