""" Handle API interaction with the hosted pigeon services. """
import re
from typing import Tuple, BinaryIO

import requests

from . import errors

API_URL = "https://europe-west2-sharebin-1584549443764.cloudfunctions.net/api"


def _download_file(signed_url: str) -> bytes:
    """ Authenticate the service and get the google file download link. """
    result = requests.get(signed_url)

    if result.status_code == 200:
        return result.content

    raise errors.DownloadException(result.status_code, result.content)


def _extract_id(link: str) -> str:
    """ Perform validation on the inputed URL or ID used for downloading the
    file.

    """
    url_extractor = re.compile(
        r"^(http(s)?://)?pigeon\.ventures/(?P<id>[a-zA-Z0-9]{6})$")
    url_match = url_extractor.match(link)
    if url_match:
        return url_match.group('id')

    id_extractor = re.compile("^[a-zA-Z0-9]{6}$")
    id_match = id_extractor.match(link)
    if id_match:
        return id_match.string

    raise errors.InvalidIDExcpetion(link)


def _get_download_url(file_id: str) -> str:
    """ Authenticate the service and get the google file download link. """
    result = requests.get(f"{API_URL}?id={file_id}")
    jsn = result.json()

    if result.status_code == 200:
        return jsn['signedUrl'][0]

    if result.status_code == 404:
        raise errors.DownloadNotFound(jsn['error'])

    raise errors.DownloadException(result.status_code, result.content)


def _get_upload_url() -> Tuple[str, str]:
    """ Authenticate the service and get the google file upload link. """
    result = requests.post(API_URL)

    if result.status_code == 200:
        jsn = result.json()
        return jsn['id'], jsn['signedUrl'][0]

    raise errors.UploadException(result.status_code, result.content)


def _upload_file(signed_url: str, file: BinaryIO):
    """ Upload the provided file to the signed url returned by the server. """
    results = requests.put(signed_url, data=file)
    if results.status_code != 200:
        raise Exception("Failed to upload file to server!")


def get(link: str) -> str:
    """ Retrieve a file from the service based on the provided URL.

    Args:
        link: The URL or ID used to reference the shared file.

    Returns:
        The name of the newly created file.
    """
    file_id = _extract_id(link)
    signed_url = _get_download_url(file_id)
    downloaded_content = _download_file(signed_url)
    with open(file_id, "wb") as file:
        file.write(downloaded_content)
    return file_id


def share(file: BinaryIO) -> str:
    """ Upload a file to the service and return a reference URL.

    Args:
        file: The file object that will be directly uploaded to service.

    Returns:
        The URL used to retrieve the file at a later time.
    """
    file_id, signed_url = _get_upload_url()
    _upload_file(signed_url, file)
    return f"https://pigeon.ventures/{file_id}"
