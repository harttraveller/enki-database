from pathlib import Path

package = Path(__file__).parent
include = package / ".include"

home = Path.home()
cache = home / ".enki"
database = cache / "wiki.db"
dumps = cache / "dumps"
