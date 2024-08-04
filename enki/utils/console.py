from pathlib import Path

from rich import print
from rich.filesize import decimal
from rich.markup import escape
from rich.text import Text
from rich.tree import Tree


def walk_directory(
    directory: Path, tree: Tree, file_color: str, size_color: str
) -> None:
    paths = sorted(
        Path(directory).iterdir(),
        key=lambda path: (path.is_file(), path.name.lower()),
    )
    for path in paths:
        if path.is_dir():
            branch = tree.add(escape(path.name))
            walk_directory(path, branch, file_color, size_color)
        else:
            text_filename = Text(path.name, file_color)
            text_filename.highlight_regex(r"\..*$", file_color)
            file_size = path.stat().st_size
            text_filename.append(f" ({decimal(file_size)})", size_color)
            tree.add(text_filename)


def print_tree(
    root: Path,
    dir_color: str = "aquamarine1",
    file_color: str = "sea_green2",
    size_color: str = "light_coral",
) -> None:
    tree = Tree(
        str(root),
        style=dir_color,
        guide_style=dir_color,
    )
    walk_directory(root, tree, file_color, size_color)
    print(tree)
