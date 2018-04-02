import asyncio
import time

import aiostorage.backblaze
import aiostorage.settings


videos = (
    {
        'path': 'tests/data/videos/Helene Fischer - Atemlos durch die Nacht.mp4',
        'content_type': 'video/mp4',
    },
    {
        'path': 'tests/data/videos/Luis Fonsi - Despacito ft Daddy Yankee.mp4',
        'content_type': 'video/mp4',
    },
    {
        'path': 'tests/data/videos/Rino Gaetano - Ma il cielo è sempre più blu.webm',
        'content_type': 'video/webm',
    },
    {
        'path': 'tests/data/videos/Stromae - Alors On Danse.webm',
        'content_type': 'video/webm',
    },
)

i = 20

async def upload_video(storage, video):
    start = time.time()
    print('{} Starting upload_video for {}...'.format('#' * i, video['path']))
    await storage.authenticate()
    bucket_id = aiostorage.settings.BACKBLAZE_TEST_BUCKET_ID
    await storage.upload_file(bucket_id, video['path'], video['content_type'])
    print('{} Uploaded {} in {}s'.format('#' * i, video['path'], time.time() - start))


async def run():
    start = time.time()
    print('{} Starting main loop...'.format('#' * i))
    storage = aiostorage.backblaze.Backblaze(
        account_id=aiostorage.settings.BACKBLAZE_ACCOUNT_ID,
        app_key=aiostorage.settings.BACKBLAZE_APP_KEY
    )
    futures = []
    for video in videos:
        future = asyncio.ensure_future(upload_video(storage, video))
        futures.append(future)
    await asyncio.wait(futures)
    print('{} Main loop done in {}s'.format('#' * i, time.time() - start))

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
