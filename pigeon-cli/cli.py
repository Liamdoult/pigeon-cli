import click

import api


@click.group()
def run():
    """ Main appication entry point """


@run.command()
@click.argument("file", type=click.File())
def share(file):
    """ Upload a file and recieve a link to share the file. """
    link = api.share(file)
    print(f"You can share the link: {link}")
