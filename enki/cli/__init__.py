import typer
import webbrowser
from rich import print
from enki.__meta__ import __package__, __module__, __version__, __docs__
from pycooltext import cooltext

app = typer.Typer()


@app.callback(name="enki", invoke_without_command=True)
def callback():
    cooltext(__module__)
    print(
        f"[deep_sky_blue1]Version:[/deep_sky_blue1] [turquoise2]{__version__}[/turquoise2]"
    )
    # todo: add printout for where cache and whether dumps/minidb dled


@app.command()
def docs():
    webbrowser.open(__docs__)
