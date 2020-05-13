""" Provide Command Line Interface handling using Click. """
import tempfile
import traceback
from typing import BinaryIO

import click

from pigeon_cli import api, errors


def _click_handle_error(error, message):
    with tempfile.NamedTemporaryFile("w", suffix=".log",
                                     delete=False) as tmp_file:
        tmp_file.write(traceback.format_exc())
        raise click.ClickException(
            f"{message}\nSee log for more information: {tmp_file.name}"
        ) from error


@click.group()
def run():
    """ Main appication entry point """


@run.command()
@click.argument("file", type=click.File())
def share(file: BinaryIO):
    """ Upload a file and receive a link to share the file. """
    try:
        link = api.share(file)
        print(f"You can share the link: {link}")
    except errors.UploadException as error:
        _click_handle_error(
            error,
            "Something went wrong when attempting to upload the URL. This "
            "could be caused by a bad connection to the server?")
    except Exception as error:  # pylint: disable=W0703
        _click_handle_error(error, "Something unexpected happened!")


@run.command()
@click.argument("link")
def get(link: str):
    """ Use a URL or ID to download a shared file. """
    try:
        output_name = api.get(link)
        print(
            f"Your requested file has been downloaded and named: {output_name}"
        )
    except errors.DownloadNotFound as error:
        _click_handle_error(
            error,
            "The server failed to find the file you requested. Please double "
            "check you entered the code correctly.")
    except errors.DownloadException as error:
        _click_handle_error(
            error,
            "Something went wrong when attempting to download the file you "
            "requested. This could be caused by a bad connection to the "
            "server?")
    except Exception as error:  # pylint: disable=W0703
        _click_handle_error(error, "Something unexpected happened!")
