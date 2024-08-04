import typer
import webbrowser
from rich import print
from enki.__meta__ import __module__, __version__, __docs__
from pycooltext import cooltext
from . import cache

app = typer.Typer()
app.add_typer(cache.app)


@app.callback(name=__module__, invoke_without_command=True)
def callback(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        cooltext(__module__)
        print(
            f"[deep_sky_blue1]Version:[/deep_sky_blue1] [turquoise2]{__version__}[/turquoise2]"
        )
        # todo: add printout for where cache and whether dumps/minidb dled


@app.command()
def docs():
    """Open the docs site in your default web browser."""
    webbrowser.open(__docs__)
