""" Handle API interaction with the hosted pigeon services. """
import re
from typing import Tuple

import requests

API_URL = "https://europe-west2-sharebin-1584549443764.cloudfunctions.net/api"


def _download_file(signed_url: str) -> bytes:
    """ Authenticate the service and get the google file download link. """
    result = requests.get(signed_url)

    if result.status_code == 200:
        return result.content

    raise Exception("Failed to download file!")


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

    raise Exception("Invalid input ID/URL")


def _get_download_url(file_id: str) -> str:
    """ Authenticate the service and get the google file download link. """
    result = requests.get(f"{API_URL}?id={file_id}")
    jsn = result.json()

    if result.status_code == 200:
        signed_url = jsn['signedUrl'][0]

        return signed_url

    raise Exception(f"{jsn['error']}")


def _get_upload_url() -> Tuple[str, str]:
    """ Authenticate the service and get the google file upload link. """
    result = requests.post(API_URL)
    jsn = result.json()

    if result.status_code == 200:
        file_id = jsn['id']
        signed_url = jsn['signedUrl'][0]

        return file_id, signed_url

    raise Exception(f"{jsn['error']}")


def _upload_file(signed_url: str, file: file):
    """ Upload the provided file to the signed url returned by the server. """
    results = requests.put(signed_url, data=file)
    if results.status_code != 200:
        raise Exception("Failed to upload file to server!")


def get(link: str):
    """ Retrieve a file from the service based on the provided URL.

    Args:
        link: The URL or ID used to reference the shared file.
    """
    file_id = _extract_id(link)
    signed_url = _get_download_url(file_id)
    with open(file_id, "wb") as file:
        file.write(_download_file(signed_url))


def share(file: file) -> str:
    """ Upload a file to the service and return a reference URL.

    Args:
        file: The file object that will be directly uploaded to service.

    Returns:
        The URL used to retrieve the file at a later time.
    """
    file_id, signed_url = _get_upload_url()
    _upload_file(signed_url, file)
    return f"https://pigeon.ventures/{file_id}"
