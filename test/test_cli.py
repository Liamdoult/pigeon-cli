from unittest import mock

import click.testing
import pytest

from pigeon_cli import cli, errors


class MockApi:

    callback = None

    def configure(self, callback):
        """ The result of the callback with be returned in share or the issue
        raised. """
        self.callback = callback

    def share(self, *args, **kwargs):
        if self.callback is None:
            raise Exception("TEST MOCK ERROR: No callback configured.")
        return self.callback(*args, **kwargs)

    def get(self, *args, **kwargs):
        if self.callback is None:
            raise Exception("TEST MOCK ERROR: No callback configured.")
        return self.callback(*args, **kwargs)


@pytest.fixture
def mock_api_share():
    backup = cli.api
    mock_api = MockApi()
    cli.api = mock_api
    yield mock_api
    cli.api = backup


def test_share_success(mock_api_share):
    file_name = "example_file_name.txt"
    content = "Unused useless testing data"

    def callback(*args, **kwargs):
        return "https://pigeon.ventures/1asdf1"

    mock_api_share.configure(callback)

    runner = click.testing.CliRunner()
    with runner.isolated_filesystem():
        with open(file_name, 'w') as f:
            f.write(content)

        result = runner.invoke(cli.run, ['share', file_name])
        assert result.exit_code == 0
        assert "https://pigeon.ventures/1asdf1" in result.output


def test_share_failed_expected_UploadException(mock_api_share):
    file_name = "example_file_name.txt"
    content = "Unused useless testing data"

    def callback(*args, **kwargs):
        raise errors.UploadException(404, "This is test content of an error")

    mock_api_share.configure(callback)

    runner = click.testing.CliRunner()
    with runner.isolated_filesystem():
        with open(file_name, 'w') as f:
            f.write(content)

        result = runner.invoke(cli.run, ['share', file_name])
        assert result.exit_code == 1
        assert ("Something went wrong when attempting to upload the URL. This "
                "could be caused by a bad connection to the server?"
                ) in result.output
        assert "See log for more information: " in result.output
        assert ".log" in result.output


def test_share_failed_unexpected_Exception(mock_api_share):
    file_name = "example_file_name.txt"
    content = "Unused useless testing data"

    def callback(*args, **kwargs):
        raise Exception("This is just a test exception")

    mock_api_share.configure(callback)

    runner = click.testing.CliRunner()
    with runner.isolated_filesystem():
        with open(file_name, 'w') as f:
            f.write(content)

        result = runner.invoke(cli.run, ['share', file_name])
        assert result.exit_code == 1
        assert "Something unexpected happened!"
        assert "See log for more information: " in result.output
        assert ".log" in result.output


def test_get_success(mock_api_share):
    file_id = "as812a"

    def callback(file_id, *args, **kwargs):
        if file_id != "as812a":
            raise Exception(
                "TEST ERROR: received file_id does not match provided")
        return "example_file_name"

    mock_api_share.configure(callback)

    runner = click.testing.CliRunner()
    result = runner.invoke(cli.run, ['get', file_id])
    assert result.exit_code == 0
    assert "example_file_name" in result.output


def test_get_failed_expected_DownloadException(mock_api_share):
    file_id = "as812a"

    def callback(*args, **kwargs):
        raise errors.DownloadException(404,
                                       "This is just example error content")

    mock_api_share.configure(callback)

    runner = click.testing.CliRunner()
    result = runner.invoke(cli.run, ['get', file_id])
    assert result.exit_code == 1
    assert (
        "Error: Something went wrong when attempting to download the file you "
        "requested. This could be caused by a bad connection to the server?\n"
    ) in result.output
    assert "See log for more information: " in result.output
    assert ".log" in result.output


def test_get_failed_expected_DownloadNotFound(mock_api_share):
    file_id = "as812a"

    def callback(*args, **kwargs):
        raise errors.DownloadNotFound("This is just example error content")

    mock_api_share.configure(callback)

    runner = click.testing.CliRunner()
    result = runner.invoke(cli.run, ['get', file_id])
    assert result.exit_code == 1
    assert ("The server failed to find the file you requested. Please "
            "double check you entered the code correctly.\n") in result.output
    assert "See log for more information: " in result.output
    assert ".log" in result.output


def test_get_failed_unexpected_Exception(mock_api_share):
    file_id = "as812a"

    def callback(*args, **kwargs):
        raise errors.Exception("This is just a test exception")

    mock_api_share.configure(callback)

    runner = click.testing.CliRunner()
    result = runner.invoke(cli.run, ['get', file_id])
    assert result.exit_code == 1
    assert "Something unexpected happened!"
    assert "See log for more information: " in result.output
    assert ".log" in result.output
