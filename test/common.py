from pathlib import Path

temp_path = Path(__file__).parent / "temp"
temp_path.mkdir(exist_ok=True, parents=True)
