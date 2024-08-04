import typer
from typing import Annotated

app = typer.Typer()


@app.callback(name="cache", invoke_without_command=True)
def callback(ctx: typer.Context):
    """Show the path"""
    ...


@app.command(name="vscode")
def vscode():
    """
    Open cache dir in VSCode.
    """
    raise NotImplementedError()


@app.command(name="clear")
def clear(yes: Annotated[bool, typer.Option("--yes/-y")]):
    """
    Delete all locally cached data.
    """
    raise NotImplementedError()
