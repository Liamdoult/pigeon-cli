""" Error reporting and handling module. """
import logging


class ExceptionLogging(Exception):
    """ Provide Logging to Exception. """
    def __init__(self, message, *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        logging.exception("error: %s", message)


class DownloadException(ExceptionLogging):
    """ Base Exception class for handling download exceptions. """
    def __init__(self, status_code, content):
        super().__init__(f"Unknow download error - {status_code} : {content}")


class DownloadNotFound(ExceptionLogging):
    """ This exception is raised of the server has not found the correct
    download based on the client provided ID. """
    def __init__(self, error):
        super().__init__(f"ID not found by the server. \n{error}")


class InvalidIDExcpetion(ExceptionLogging):
    """ Base Exception class for handling invalid ID's """
    def __init__(self, provided_id):
        super().__init__(f"Invalid URL or ID: {provided_id}")


class UploadException(ExceptionLogging):
    """ Base Exception class for handling download exceptions. """
    def __init__(self, status_code, content):
        super().__init__(f"Unknow download error - {status_code} : {content}")
