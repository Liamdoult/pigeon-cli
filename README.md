# pigeon-cli

CLI component to my file sharing service.


# Usage

## Installation

The current version only supports Python usage:

    python setup.py install

## Upload a file

    python pigeon-cli share /path/to/file

## Download file

To download the shared file:

    python pigeon-cli get <shared ID or URL>

This will create a file with the same name as the `ID` provided.

