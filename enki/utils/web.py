import httpx


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
