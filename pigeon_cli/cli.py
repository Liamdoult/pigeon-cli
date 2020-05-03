""" Provide Command Line Interface handling using Click. """
import click

from pigeon_cli import api


@click.group()
def run():
    """ Main appication entry point """


@run.command()
@click.argument("file", type=click.File())
def share(file: file):
    """ Upload a file and recieve a link to share the file. """
    link = api.share(file)
    print(f"You can share the link: {link}")


@run.command()
@click.argument("link")
def get(link: str):
    """ Use a URL or ID to download a shared file. """
    api.get(link)
    print("Download complete")
