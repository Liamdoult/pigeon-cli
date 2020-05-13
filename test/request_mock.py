import json

import pytest

from pigeon_cli import api


class MockResult:
    def __init__(self, status_code, json={}):
        self.status_code = status_code
        self._json = json

    def json(self):
        return self._json

    @property
    def content(self):
        if '_content' in self._json:
            return self._json['_content']
        else:
            return json.dumps(json)


class MockRequest:
    responses = {}

    def set_responses(self, responses):
        self.responses = responses

    def get(self, url, **kwargs):
        if 'get' in self.responses:
            if url in self.responses['get']:
                return MockResult(**self.responses['get'][url])

        raise Exception(
            "Invalid mock request. Please make sure the mocked request matches what has been requested"
        )

    def post(self, url, **kwargs):
        if 'post' in self.responses:
            if url in self.responses['post']:
                return MockResult(**self.responses['post'][url])

        raise Exception(
            "Invalid mock request. Please make sure the mocked request matches what has been requested"
        )

    def put(self, url, **kwargs):
        if 'put' in self.responses:
            if url in self.responses['put']:
                return MockResult(**self.responses['put'][url])

        raise Exception(
            "Invalid mock request. Please make sure the mocked request matches what has been requested"
        )


@pytest.fixture
def mock_requests():
    backup = api.requests
    api.requests = MockRequest()
    yield api.requests
    api.requests = backup
