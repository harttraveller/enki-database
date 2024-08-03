from pathlib import Path
from enki.utils import web

temp_path = Path(__file__).parent / "temp"
temp_path.mkdir(exist_ok=True, parents=True)


url1 = "https://uberty.org/wp-content/uploads/2015/07/Norbert_Wiener_Cybernetics.pdf"
url1_size = 8804356
url2 = "https://the-eye.eu/public/AI/Alignment/moirage_alignment-research-dataset/README.txt"


def test_remote_accepts_byte_range() -> None:
    assert web.remote_accepts_byte_range(url1) == True


def test_read_resource_chunk() -> None:
    chunk: bytes = web.read_resource_chunk(url1, 0, 3)
    assert len(chunk) == 4
    assert chunk == b"%PDF"


def test_request_content_length_basic() -> None:
    length: int = web.request_content_length_basic(url1)
    assert length == url1_size


def test_estimate_content_length_dynamic() -> None:
    length: int = web.estimate_content_length_dynamic(url1)
    assert length == url1_size


def test_get_resource_size() -> None:
    size: int = web.get_resource_size(url1)
    assert size == url1_size


def test_download_resource() -> None:
    file_path: Path = temp_path / url1.split("/")[-1]
    if not file_path.exists():
        web.download_resource(url1, file_path)
        assert file_path.exists()
        assert file_path.stat().st_size == url1_size


def test_read_resource() -> None:
    file_path: Path = temp_path / url2.split("/")[-1]
    if not file_path.exists():
        web.download_resource(url2, file_path, skip_sizecheck=True)
    web_bytes: bytes = web.read_resource(url2, skip_sizecheck=True)
    with open(file_path, "rb") as f:
        loc_bytes = f.read()
    assert web_bytes == loc_bytes
