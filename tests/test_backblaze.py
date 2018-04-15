import logging
import os

import aiohttp
import pytest

from aiostorage.backblaze import Backblaze
from aiostorage.settings import BACKBLAZE_ACCOUNT_ID
from aiostorage.settings import BACKBLAZE_APP_KEY
from aiostorage.settings import BACKBLAZE_TEST_BUCKET_ID


logger = logging.getLogger(__name__)

VIDEOS_PATH = 'tests/data/videos'


@pytest.fixture
def storage():
    return Backblaze(account_id=BACKBLAZE_ACCOUNT_ID,
                     app_key=BACKBLAZE_APP_KEY)


@pytest.mark.asyncio
async def test_authenticate(storage):
    try:
        result = await storage.authenticate()
        assert {'apiUrl', 'authorizationToken'}.issubset(result)
    except aiohttp.ClientResponseError:
        logger.exception('Unable to authenticate, please check credentials. '
                         'Status: %s, message: %s, headers: %s, history: %s',
                         aiohttp.ClientResponseError.status,
                         aiohttp.ClientResponseError.message,
                         aiohttp.ClientResponseError.headers,
                         aiohttp.ClientResponseError.history)


@pytest.mark.asyncio
async def test__get_upload_url(storage):
    try:
        await storage.authenticate()
    except aiohttp.ClientResponseError:
        logger.exception('Unable to authenticate, please check credentials. '
                         'Status: %s, message: %s, headers: %s, history: %s',
                         aiohttp.ClientResponseError.status,
                         aiohttp.ClientResponseError.message,
                         aiohttp.ClientResponseError.headers,
                         aiohttp.ClientResponseError.history)
    else:
        try:
            result = await storage._get_upload_url(BACKBLAZE_TEST_BUCKET_ID)
            assert {'uploadUrl', 'authorizationToken'}.issubset(result)
        except aiohttp.ClientResponseError:
            logger.exception('Unable to get upload URL. Status: %s, message: '
                             '%s, headers: %s, history: %s',
                             aiohttp.ClientResponseError.status,
                             aiohttp.ClientResponseError.message,
                             aiohttp.ClientResponseError.headers,
                             aiohttp.ClientResponseError.history)


@pytest.mark.parametrize(
    ('bucket_id', 'file_to_upload', 'content_type', 'expected'),
    (
        (BACKBLAZE_TEST_BUCKET_ID,
         'Helene Fischer - Atemlos durch die Nacht.mp4', 'video/mp4', 1607175),
        (BACKBLAZE_TEST_BUCKET_ID,
         'Luis Fonsi - Despacito ft Daddy Yankee.mp4', 'video/mp4', 3452397),
        (BACKBLAZE_TEST_BUCKET_ID,
         'Rino Gaetano - Ma il cielo è sempre più blu.webm', 'video/webm',
         262276),
        (BACKBLAZE_TEST_BUCKET_ID,
         'Stromae - Alors On Danse.webm', 'video/webm', 664295),
    )
)
@pytest.mark.asyncio
async def test_upload_file(storage, bucket_id, file_to_upload, content_type,
                           expected):
    try:
        await storage.authenticate()
    except aiohttp.ClientResponseError:
        logger.exception('Unable to authenticate, please check credentials. '
                         'Status: %s, message: %s, headers: %s, history: %s',
                         aiohttp.ClientResponseError.status,
                         aiohttp.ClientResponseError.message,
                         aiohttp.ClientResponseError.headers,
                         aiohttp.ClientResponseError.history)
    else:
        try:
            result = await storage.upload_file(bucket_id, os.path.join(
                VIDEOS_PATH, file_to_upload), content_type)
            assert result.get('contentLength') == expected
        except aiohttp.ClientResponseError:
            logger.exception('Unable to upload file (error uploading file) %s'
                             ' with content type %s to bucket %s. Status: %s,'
                             'message: %s, headers: %s, history: %s',
                             file_to_upload, content_type, bucket_id,
                             aiohttp.ClientResponseError.status,
                             aiohttp.ClientResponseError.message,
                             aiohttp.ClientResponseError.headers,
                             aiohttp.ClientResponseError.history)
