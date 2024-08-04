from pathlib import Path

package = Path(__file__).parent
include = package / ".include"

home = Path.home()
cache = home / ".enki"
dumps = cache / "dumps"
for __path in [cache, dumps]:
    __path.mkdir(exist_ok=True, parents=True)

database = cache / "enwiki.db"
