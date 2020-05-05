""" Basic setup for Pigeon CLI """
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

test_dependencies = ['pytest']

setup(
    name='pigeon-cli',
    version='0.0.2',
    aution='Liam Doult',
    packages=find_packages(),
    python_requires='>=3.7, < 4',
    install_requires=[
        'click',
        'requests',
    ],
    tests_require=test_dependencies,
    setup_requires=['pytest-runner'],
    extras_require={
        'test': test_dependencies,
    },
    test_suite='test',
)
