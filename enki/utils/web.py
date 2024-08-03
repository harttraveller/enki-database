import httpx
from io import BytesIO
from pathlib import Path


def remote_accepts_byte_range(
    url: str,
    follow_redirects: bool = True,
) -> bool:
    """
    Check if a remote server accepts byte range requests.

    This function sends a HEAD request to the specified URL with a 'Range' header
    to determine if the server supports partial content requests.

    Args:
        url (str): The URL to check for byte range support.
        follow_redirects (bool, optional): Whether to follow redirects. Defaults to True.

    Returns:
        bool: True if the server accepts byte range requests, False otherwise.
    """
    headers = {"Range": "bytes=0-8"}
    response = httpx.head(url=url, headers=headers, follow_redirects=follow_redirects)
    response.raise_for_status()
    return response.status_code == 206


def read_resource_chunk(
    url: str,
    start: int,
    end: int,
    follow_redirects: bool = True,
) -> bytes:
    """
    Read a specific byte range from a remote resource.

    This function sends a GET request to the specified URL with a 'Range'
    header to retrieve a specific chunk of the resource.

    Args:
        url (str): The URL of the remote resource.
        start (int): The starting byte position of the chunk.
        end (int): The ending byte position of the chunk.
        follow_redirects (bool, optional): Whether to follow redirects. Defaults to True.

    Returns:
        bytes: The requested chunk of the resource as bytes.

    Raises:
        Exception: If the remote server does not accept byte range requests.
    """
    headers = {"Range": f"bytes={start}-{end}"}
    buffer = BytesIO()
    response = httpx.get(url, headers=headers, follow_redirects=follow_redirects)
    response.raise_for_status()
    if response.status_code != 206:
        raise Exception("The remote server does not accept byte range requests.")
    buffer.write(response.content)
    buffer.seek(0)
    return buffer.read()


def request_content_length_basic(
    url: str,
    follow_redirects: bool = True,
) -> int:
    """
    Get the content length of a remote resource.

    This function sends a HEAD request to the specified URL and retrieves
    the 'Content-Length' header value.

    Args:
        url (str): The URL of the remote resource.
        follow_redirects (bool, optional): Whether to follow redirects. Defaults to True.

    Returns:
        int: The content length of the resource in bytes.

    Raises:
        KeyError: If the 'Content-Length' header is not found in the response.
    """
    response = httpx.head(url, follow_redirects=follow_redirects)
    response.raise_for_status()
    headers = {k.lower(): v for k, v in dict(response.headers).items()}
    if "content-length" not in headers.keys():
        raise KeyError("'content-length' header not found")
    else:
        return int(headers["content-length"])


def estimate_content_length_dynamic(
    url: str,
    initial_guess: int = 1 << 20,
    max_requests: int = 10,
) -> int:
    """
    Estimates the content length of a resource by making strategic byte range requests.

    Args:
        url (str): The URL of the resource.
        initial_guess (int): Initial guess for the file size in bytes. Default is 1MB.
        max_requests (int): Maximum number of requests to make before giving up.

    Returns:
        int: Estimated content length in bytes
    """
    with httpx.Client() as httpx_client:
        lower_bound = 0
        upper_bound = initial_guess
        requests_made = 0
        while requests_made < max_requests:
            requests_made += 1
            mid = (lower_bound + upper_bound) // 2
            headers = {"Range": f"bytes={mid}-{mid}"}
            response = httpx_client.get(url, headers=headers, follow_redirects=True)
            if response.status_code == 206:
                lower_bound = mid
                if upper_bound == lower_bound + 1:
                    return upper_bound
                if "Content-Range" in response.headers:
                    content_range = response.headers["Content-Range"]
                    total_size = int(content_range.split("/")[-1])
                    return total_size
            elif response.status_code == 416:
                upper_bound = mid
            else:
                raise Exception(
                    f"Unexpected status code: {response.status_code}",
                )
            if upper_bound - lower_bound <= 1:
                return upper_bound
            if upper_bound == initial_guess:
                upper_bound *= 2
        raise Exception("Cannot estimate remote resource size")


def get_resource_size(url: str) -> int:
    """
    Get the size of a remote resource.

    This function attempts to determine the size of a remote resource using different methods.
    It first tries to get the content length using a basic request. If that fails, it checks
    if the server accepts byte range requests. If so, it estimates the content length dynamically.

    Args:
        url (str): The URL of the remote resource.

    Returns:
        int: The size of the remote resource in bytes.

    Raises:
        Exception: If the size of the remote resource cannot be determined.
    """
    try:
        size = request_content_length_basic(url)
        return size
    except:
        range_accepted = remote_accepts_byte_range(url)
        if range_accepted:
            size = estimate_content_length_dynamic(url)
            return size
        else:
            raise Exception("cannot estimate remote resource size")


def download_resource(
    url: str,
    path: str | Path | None = None,
    allow_overwrite: bool = False,
    chunk_size: int = 1 << 10,
    show_progress: bool = False,
) -> None: ...
