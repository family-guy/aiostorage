import asyncio
import logging

from .exceptions import BlobStorageUnrecognisedProviderError
from .providers import (Backblaze, BackblazeAuthenticationError, PROVIDERS,
                        BackblazeFileUploadError)


logger = logging.getLogger(__name__)

class BlobStorage:

    PROVIDER_ADAPTER = {
        'backblaze': Backblaze,
    }

    def __init__(self, provider, credentials):
        if provider not in PROVIDERS:
            raise BlobStorageUnrecognisedProviderError
        self.provider = self.PROVIDER_ADAPTER[provider](credentials)
        self.loop = asyncio.get_event_loop()

    async def _upload_file(self, bucket, file):
        auth_response = await self.provider.authenticate()
        if not auth_response:
            raise BackblazeAuthenticationError
        upload_file_response = await self.provider.upload_file(
            bucket, file['path'], file['content_type'])
        if not upload_file_response:
            raise BackblazeFileUploadError

    def upload_files(self, bucket, files):
        async def _upload_files():
            futures = []
            for file in files:
                future = asyncio.ensure_future(self._upload_file(bucket, file))
                futures.append(future)
            await asyncio.wait(futures)
        self.loop.run_until_complete(_upload_files())
