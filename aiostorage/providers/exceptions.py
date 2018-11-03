"""
Exceptions for errors whilst communicating with an object storage provider.
"""


class ProviderError(Exception):
    """
    Base exception class for object storage provider errors.
    """


class ProviderAuthenticationError(ProviderError):
    """
    Unable to authenticate.
    """


class ProviderGetUploadUrlError(ProviderError):
    """
    Unable to get file upload URL.
    """


class ProviderAuthorizationError(ProviderError):
    """
    Unable to perform action due to lack of authorization.
    """


class ProviderFileUploadError(ProviderError):
    """
    Unable to upload file.
    """
