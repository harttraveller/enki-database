import typer
from rich import print
from enki.__meta__ import __package__, __module__, __version__
from pycooltext import cooltext

app = typer.Typer()


@app.callback(name="enki", invoke_without_command=True)
def callback():
    cooltext(__module__)
    print(f"[cyan]Version:[/cyan] [lightgreen]{__version__}[/lightgreen]")
    # todo: add printout for where cache and whether dumps/minidb dled
