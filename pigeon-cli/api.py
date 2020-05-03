import re

import requests

API_URL = "https://europe-west2-sharebin-1584549443764.cloudfunctions.net/api"

def _get_upload_url():
    """ Authenticate the service and get the google file upload link. """
    result = requests.post(API_URL)
    jsn = result.json()

    if result.status_code == 200:
        id = jsn['id']
        signed_url = jsn['signedUrl'][0]

        return id, signed_url
    else:
        raise Exception(f"{jsn['error']}")
        

def _upload_file(signed_url, file):
    """ Upload the provided file to the signed url returned by the server. """
    results = requests.put(signed_url, data=file)
    if results.status_code != 200:
        raise Exception("Failed to upload file to server!")


def share(file):
    """ Upload a file to the service and return a reference URL.
    
    Args:
        file: The file object that will be directly uploaded to service.

    Returns:
        The URL used to retrieve the file at a later time.
    """
    id, signed_url = _get_upload_url() 
    _upload_file(signed_url, file)
    return f"https://pigeon.ventures/{id}"


def _get_download_url(id):
    """ Authenticate the service and get the google file download link. """
    result = requests.get(f"{API_URL}?id={id}")
    jsn = result.json()

    if result.status_code == 200:
        signed_url = jsn['signedUrl'][0]

        return signed_url
    else:
        raise Exception(f"{jsn['error']}")

def _download_file(signed_url):
    """ Authenticate the service and get the google file download link. """
    result = requests.get(signed_url)

    if result.status_code == 200:
        return result.content
    else:
        raise Exception(f"Failed to download file!")
    

def _extract_id(input):
    """ Perform validation on the inputed URL or ID used for downloading the
    file.
    
    """
    url_extractor = re.compile("^(http(s)?:\/\/)?pigeon\.ventures\/(?P<id>[a-zA-Z0-9]{6})$")
    url_match = url_extractor.match(input)
    if url_match:
        return url_match.group('id')

    id_extractor = re.compile("^[a-zA-Z0-9]{6}$")
    id_match = id_extractor.match(input)
    if id_match:
        return id_match.string

    raise Exception("Invalid input ID/URL")


def get(input):
    """ Retrieve a file from the service based on the provided URL. """
    id = _extract_id(input)
    signed_url = _get_download_url(id)
    with open(id, "wb") as file:
        file.write(_download_file(signed_url))
