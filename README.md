# pigeon-cli

![Python tests](https://github.com/Liamdoult/python-template/workflows/Python%20tests/badge.svg)

## Usage

### Installation

The current version only supports Python usage:

    python setup.py install

### Upload a file

    python pigeon_cli share /path/to/file

### Download file

To download the shared file:

    python pigeon_cli get <shared ID or URL>

This will create a file with the same name as the `ID` provided.

### Testing

All tests are written in with pytest. You can simply run the test suite with tox:

    $ tox
