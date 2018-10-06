import asyncio

from .providers import Backblaze


class BlobStorage:

    PROVIDER_ADAPTER = {
        'backblaze': Backblaze,
    }

    def __init__(self, provider, credentials):
        if provider not in self.PROVIDER_ADAPTER.keys():
            raise Exception('unrecognised provider')
        self.provider = self.PROVIDER_ADAPTER[provider](credentials)
        self.loop = asyncio.get_event_loop()

    async def _upload_file(self, bucket, file):
        await self.provider.authenticate()
        await self.provider.upload_file(bucket, file['path'],
                                        file['content_type'])

    def upload_files(self, bucket, files):
        async def _upload_files():
            futures = []
            for file in files:
                future = asyncio.ensure_future(self._upload_file(bucket, file))
                futures.append(future)
            await asyncio.wait(futures)
        self.loop.run_until_complete(_upload_files())
