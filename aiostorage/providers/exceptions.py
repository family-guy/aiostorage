"""
Exceptions for errors that occur whilst communicating with an object storage
provider.
"""


class ProviderError(Exception):
    """
    Base exception class for provider errors.
    """


class ProviderAuthenticationError(ProviderError):
    """
    Unable to authenticate to the object storage provider.
    """


class ProviderGetUploadUrlError(ProviderError):
    """
    Unable to get URL for uploading a file to the object storage provider.
    """


class ProviderAuthorizationError(ProviderError):
    """
    Unable to perform action due to lack of authorization from the object
    storage provider.
    """


class ProviderFileUploadError(ProviderError):
    """
    Unable to upload file to the object storage provider.
    """
