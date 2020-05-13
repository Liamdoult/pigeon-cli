""" Test for the API module. """
from unittest import mock

import pytest

from test.request_mock import mock_requests
from pigeon_cli import api, errors

TEST_EXTRACT_ID_PARAMS = [
    ("https://pigeon.ventures/a83hs1", "a83hs1"),
    ("ajf812", "ajf812"),
]

TEST_EXTRACT_ID_FAILS_PARAMS = [
    "https://some.url/a83hs1",
    "ajf81212sdaklf",
]


@pytest.mark.parametrize("input,expected", TEST_EXTRACT_ID_PARAMS)
def test_extract_id(input, expected):
    assert api._extract_id(input) == expected


@pytest.mark.parametrize("input", TEST_EXTRACT_ID_FAILS_PARAMS)
def test_extract_id_fails(input):
    with pytest.raises(errors.InvalidIDExcpetion):
        api._extract_id(input)


def test_share(mock_requests):
    file_id = "a1asd2"
    signed_url = "https://test.signed.url/lol"
    content = "this is a other test content"

    content = content.encode('utf-8')
    mock_requests.set_responses({
        "post": {
            f"{api.API_URL}": {
                "status_code": 200,
                "json": {
                    "id": file_id,
                    "signedUrl": [signed_url],
                }
            }
        },
        "put": {
            signed_url: {
                "status_code": 200,
            },
        },
    })
    open_mock = mock.mock_open(read_data=content)
    with mock.patch('builtins.open', open_mock, create=False):
        with open(file_id, 'rb') as f:
            assert api.share(f) == f"https://pigeon.ventures/{file_id}"
    open_mock.assert_called_once_with(file_id, 'rb')


def test_share_failed_gcp_cloud_function_query(mock_requests):
    file_id = "a1asd2"
    signed_url = "https://test.signed.url/lol"
    content = "this is a other test content"

    content = content.encode('utf-8')
    mock_requests.set_responses({
        "post": {
            f"{api.API_URL}": {
                "status_code": 404,
                "json": {
                    "_content": "Example content error message"
                }
            }
        },
        "put": {
            signed_url: {
                "status_code": 200,
            },
        },
    })
    open_mock = mock.mock_open(read_data=content)
    with mock.patch('builtins.open', open_mock, create=False):
        with open(file_id, 'rb') as f:
            with pytest.raises(errors.UploadException):
                api.share(f)
    open_mock.assert_called_once_with(file_id, 'rb')


def test_share_failed_upload_to_gcp_storage(mock_requests):
    file_id = "a1asd2"
    signed_url = "https://test.signed.url/lol"
    content = "this is a other test content"

    content = content.encode('utf-8')
    mock_requests.set_responses({
        "post": {
            f"{api.API_URL}": {
                "status_code": 200,
                "json": {
                    "id": file_id,
                    "signedUrl": [signed_url],
                }
            }
        },
        "put": {
            signed_url: {
                "status_code": 404,
                "json": {
                    "_content": "Example content error"
                }
            },
        },
    })
    open_mock = mock.mock_open(read_data=content)
    with mock.patch('builtins.open', open_mock, create=False):
        with open(file_id, 'rb') as f:
            with pytest.raises(errors.UploadException):
                api.share(f)
    open_mock.assert_called_once_with(file_id, 'rb')


# TODO: Add some varaiation in imputs and expectations
def test_get(mock_requests):
    file_id = "a7ds6s"
    signed_url = "https//test.signed.url/lol"
    content = "this is some test content"

    content = content.encode('utf-8')
    mock_requests.set_responses({
        "get": {
            f"{api.API_URL}?id={file_id}": {
                "status_code": 200,
                "json": {
                    "signedUrl": [signed_url]
                }
            },
            signed_url: {
                "status_code": 200,
                "json": {
                    "_content": content
                },
            },
        },
    })
    open_mock = mock.mock_open()
    with mock.patch('builtins.open', open_mock, create=False):
        api.get(file_id)
    open_mock.assert_called_once_with(file_id, 'wb')
    open_mock().write.assert_called_once_with(content)


def test_get_failed_download_gcp_cloud_function_file_id_not_found(
        mock_requests):
    file_id = "a7ds6s"
    signed_url = "https//test.signed.url/lol"
    content = "this is some test content"

    content = content.encode('utf-8')
    mock_requests.set_responses({
        "get": {
            f"{api.API_URL}?id={file_id}": {
                "status_code": 404,
                "json": {
                    "error": "This is an example reasoning"
                }
            },
            signed_url: {
                "status_code": 404,
                "json": {
                    "_content": content
                },
            },
        },
    })
    open_mock = mock.mock_open()
    with mock.patch('builtins.open', open_mock, create=False):
        with pytest.raises(errors.DownloadNotFound):
            api.get(file_id)


def test_get_failed_download_unexpected_gcp_cloud_function_exception(
        mock_requests):
    file_id = "a7ds6s"
    signed_url = "https//test.signed.url/lol"
    content = "this is some test content"

    content = content.encode('utf-8')
    mock_requests.set_responses({
        "get": {
            f"{api.API_URL}?id={file_id}": {
                "status_code": 500,
                "json": {
                    "_content": "This is an example of the error outpupt"
                },
            },
            signed_url: {
                "status_code": 404,
                "json": {
                    "_content": content
                },
            },
        },
    })
    open_mock = mock.mock_open()
    with mock.patch('builtins.open', open_mock, create=False):
        with pytest.raises(errors.DownloadException):
            api.get(file_id)


def test_get_failed_download_from_gcp_storage(mock_requests):
    file_id = "a7ds6s"
    signed_url = "https//test.signed.url/lol"
    content = "this is some test content"

    content = content.encode('utf-8')
    mock_requests.set_responses({
        "get": {
            f"{api.API_URL}?id={file_id}": {
                "status_code": 200,
                "json": {
                    "signedUrl": [signed_url]
                }
            },
            signed_url: {
                "status_code": 404,
                "json": {
                    "_content": content
                },
            },
        },
    })
    open_mock = mock.mock_open()
    with mock.patch('builtins.open', open_mock, create=False):
        with pytest.raises(errors.DownloadException):
            api.get(file_id)
