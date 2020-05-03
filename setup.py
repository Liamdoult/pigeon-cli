""" Basic setup for Pigeon CLI """
from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pigeon-cli',
    version='0.0.1',
    aution='Liam Doult',
    install_requires=[
        'click',
        'requests',
    ],
)
