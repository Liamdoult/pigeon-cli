""" Provide Command Line Interface handling using Click. """
from typing import BinaryIO

import click

from pigeon_cli import api, errors


@click.group()
def run():
    """ Main appication entry point """


@run.command()
@click.argument("file", type=click.File())
def share(file: BinaryIO):
    """ Upload a file and recieve a link to share the file. """
    try:
        link = api.share(file)
        print(f"You can share the link: {link}")
    except errors.UploadException:
        print("Something went wrong when attempting to upload the URL. This "
              "could be caused by a bad connection to the server?")


@run.command()
@click.argument("link")
def get(link: str):
    """ Use a URL or ID to download a shared file. """
    try:
        output_name = api.get(link)
        print(
            f"Your requested file has been downloaded and named: {output_name}"
        )
    except errors.DownloadNotFound:
        print(
            "The server failed to find the file you requested. Please double "
            "check you entered the code correctly.")
    except errors.DownloadException:
        print(
            "Something went wrong when attempting to download the file you "
            "requested. This could be caused by a bad connection to the server?"
        )
