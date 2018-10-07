from .providers import PROVIDERS


class BlobStorageError(Exception):
    """
    Base exception class for `BlobStorage`.
    """


class BlobStorageUnrecognizedProviderError(BlobStorageError):
    """
    Unrecognised object storage provider.
    """
    def __str__(self):
        return (f'Unrecognised object storage provider. Please select one of'
                f' {", ".join(PROVIDERS)}')
