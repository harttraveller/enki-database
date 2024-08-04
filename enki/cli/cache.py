import typer


app = typer.Typer()


@app.command(name="vscode")
def vscode():
    """
    Open cache dir in VSCode.
    """
    raise NotImplementedError()


@app.command(name="delete")
def delete():
    """
    Delete all locally cached data.
    """
    raise NotImplementedError()
