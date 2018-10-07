import asyncio

from .exceptions import BlobStorageUnrecognizedProviderError
from .providers import (Backblaze, BackblazeAuthenticationError,
                        BackblazeFileUploadError, PROVIDERS, )


class BlobStorage:
    PROVIDER_ADAPTER = {
        'backblaze': Backblaze,
    }

    def __init__(self, provider, credentials):
        if provider not in PROVIDERS:
            raise BlobStorageUnrecognizedProviderError
        self.provider = self.PROVIDER_ADAPTER[provider](credentials)
        self.loop = asyncio.get_event_loop()

    async def _upload_file(self, bucket, file_to_upload):
        auth_response = await self.provider.authenticate()
        if not auth_response:
            raise BackblazeAuthenticationError
        upload_file_response = await self.provider.upload_file(
            bucket, file_to_upload['path'], file_to_upload['content_type'])
        if not upload_file_response:
            raise BackblazeFileUploadError

    def upload_files(self, bucket, files_to_upload):
        async def _upload_files():
            futures = []
            for file_to_upload in files_to_upload:
                future = asyncio.ensure_future(
                    self._upload_file(bucket, file_to_upload))
                futures.append(future)
            await asyncio.wait(futures)
        self.loop.run_until_complete(_upload_files())
