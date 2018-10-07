class ProviderError(Exception):
    """
    Exceptions that occur whilst contacting an external storage provider's
    API.
    """


class BackblazeError(ProviderError):
    """
    Exceptions that occur whilst contacting the Backblaze B2 Cloud Storage API.
    """


class BackblazeAuthenticationError(BackblazeError):
    """
    Unable to authenticate.
    """


class BackblazeGetUploadUrlError(BackblazeError):
    """
    Unable to get URL for uploading a file to.
    """


class BackblazeAuthorisationError(BackblazeError):
    """
    Not authorised to perform the action requested.
    """


class BackblazeFileUploadError(BackblazeError):
    """
    Unable to upload file.
    """