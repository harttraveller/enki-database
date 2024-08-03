import pytest
import httpx
from pathlib import Path
from typing import Any
from enki.utils import web

temp_path = Path(__file__).parent.parent.parent / "temp"
test_rsrc = (
    "https://uberty.org/wp-content/uploads/2015/07/Norbert_Wiener_Cybernetics.pdf"
)
test_file = "Norbert_Wiener_Cybernetics.pdf"


def test_remote_accepts_byte_range() -> None:
    assert web.remote_accepts_byte_range(test_rsrc) == True


def test_read_resource_chunk() -> None:
    chunk: bytes = web.read_resource_chunk(test_rsrc, 0, 3)
    assert len(chunk) == 4
    assert chunk == b"%PDF"


def test_request_content_length_basic() -> None:
    length: int = web.request_content_length_basic(test_rsrc)
    assert length == 8804356


def test_estimate_content_length_dynamic() -> None:
    length: int = web.estimate_content_length_dynamic(test_rsrc)
    assert length == 8804356


# def test_get_resource_size() -> None:
#     size: int = web.get_resource_size(test_rsrc)
#     assert size == 1000


# def test_download_resource() -> None:
#     file_path: Path = temp_path / test_file
#     web.download_resource(test_rsrc, file_path)
#     assert file_path.exists()
#     assert file_path.stat().st_size == 1000


# def test_read_resource() -> None:
#     content: bytes = web.read_resource(test_rsrc)
#     assert len(content) == 1000
#     assert content == b"0" * 1000


# def test_download_resource_file_exists(tmp_path: Path) -> None:
#     file_path: Path = tmp_path / "existing_file.pdf"
#     file_path.touch()
#     with pytest.raises(FileExistsError):
#         web.download_resource(test_rsrc, file_path)


# def test_request_content_length_basic_missing_header(
#     monkeypatch: pytest.MonkeyPatch,
# ) -> None:
#     def mock_head(*args: Any, **kwargs: Any) -> httpx.Response:
#         return httpx.Response(200)

#     monkeypatch.setattr(httpx, "head", mock_head)
#     with pytest.raises(KeyError):
#         web.request_content_length_basic(test_rsrc)
