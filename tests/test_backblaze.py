import pytest

from aiostorage.backblaze import Backblaze
from aiostorage.settings import BACKBLAZE_APP_KEY
from aiostorage.settings import BACKBLAZE_ACCOUNT_ID
from aiostorage.settings import BACKBLAZE_TEST_BUCKET_ID


@pytest.mark.asyncio
async def test_authenticate():
    storage = Backblaze(account_id=BACKBLAZE_ACCOUNT_ID,
                        app_key=BACKBLAZE_APP_KEY)
    result = await storage.authenticate()
    assert {'apiUrl', 'authorizationToken'}.issubset(result)

@pytest.mark.asyncio
async def test__get_upload_url():
    storage = Backblaze(account_id=BACKBLAZE_ACCOUNT_ID,
                        app_key=BACKBLAZE_APP_KEY)
    await storage.authenticate()
    result = await storage._get_upload_url(BACKBLAZE_TEST_BUCKET_ID)
    assert {'uploadUrl', 'authorizationToken'}.issubset(result)


@pytest.mark.parametrize(
    ('bucket_id', 'file_to_upload', 'content_type', 'expected'),
    (
        (BACKBLAZE_TEST_BUCKET_ID,
         'tests/data/videos/Helene Fischer - Atemlos durch die Nacht.mp4',
         'video/mp4', 1607175),
        (BACKBLAZE_TEST_BUCKET_ID,
         'tests/data/videos/Luis Fonsi - Despacito ft Daddy Yankee.mp4',
         'video/mp4', 3452397),
        (BACKBLAZE_TEST_BUCKET_ID,
         'tests/data/videos/Rino Gaetano - Ma il cielo è sempre più blu.webm',
         'video/webm', 262276),
        (BACKBLAZE_TEST_BUCKET_ID,
         'tests/data/videos/Stromae - Alors On Danse.webm',
         'video/webm', 664295),
    )
)
@pytest.mark.asyncio
async def test_upload_file(bucket_id, file_to_upload, content_type, expected):
    storage = Backblaze(account_id=BACKBLAZE_ACCOUNT_ID,
                        app_key=BACKBLAZE_APP_KEY)
    await storage.authenticate()
    result = await storage.upload_file(bucket_id, file_to_upload, content_type)
    assert result.get('contentLength') == expected
