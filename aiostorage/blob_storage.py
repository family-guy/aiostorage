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
        required = ('account_id', 'app_key')
        if not all(r in credentials.keys() for r in required):
            raise KeyError
        self.provider = self.PROVIDER_ADAPTER[provider](credentials)
        self.loop = asyncio.get_event_loop()

    async def _upload_file(self, bucket_id, file_to_upload):
        auth_response = await self.provider.authenticate()
        if not auth_response:
            raise BackblazeAuthenticationError
        upload_file_response = await self.provider.upload_file(
            bucket_id, file_to_upload['path'], file_to_upload['content_type'])
        if not upload_file_response:
            raise BackblazeFileUploadError
        return upload_file_response

    def upload_files(self, bucket_id, files_to_upload):
        async def _upload_files():
            futures = []
            for file_to_upload in files_to_upload:
                future = asyncio.ensure_future(
                    self._upload_file(bucket_id, file_to_upload))
                futures.append(future)
            return await asyncio.gather(*futures)
        return self.loop.run_until_complete(_upload_files())
