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


def get(url):
    """ Retrieve a file from the service based on the provided URL. """
    raise NotImplementedError()
