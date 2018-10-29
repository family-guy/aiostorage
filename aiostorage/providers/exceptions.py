class ProviderError(Exception):
    """
    Exceptions that occur whilst contacting an external storage provider's
    API.
    """


class BackblazeError(ProviderError):
    """
    Exceptions that occur whilst contacting the Backblaze B2 Cloud Storage API.
    """


class ProviderAuthenticationError(ProviderError):
    """
    Unable to authenticate.
    """


class ProviderGetUploadUrlError(ProviderError):
    """
    Unable to get URL for uploading a file to.
    """


class ProviderAuthorizationError(ProviderError):
    """
    Not authorised to perform the action.
    """


class ProviderFileUploadError(ProviderError):
    """
    Unable to upload file.
    """
