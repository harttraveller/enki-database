import typer
from typing import Annotated
from enki import loc
from enki.utils.console import print_tree

app = typer.Typer()


@app.callback(name="cache", invoke_without_command=True)
def callback(ctx: typer.Context):
    """
    Show the path and tree of contents.
    """
    if ctx.invoked_subcommand is None:
        print()
        print_tree(loc.cache)


@app.command(name="vs")
def vs():
    """
    Open cache in VSCode. Requires user to run VSCode command: "Install 'code' command in PATH".
    """
    import subprocess

    subprocess.run(["code", str(loc.cache)])


@app.command(name="rm")
def rm(yes: Annotated[bool, typer.Option("--yes/-y")]):
    """
    Delete all locally cached data. This is a destructive action.
    """
    raise NotImplementedError()
