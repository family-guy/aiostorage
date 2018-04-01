import pytest

from aiostorage.backblaze import Backblaze
from aiostorage.settings import BACKBLAZE_APP_KEY
from aiostorage.settings import BACKBLAZE_ACCOUNT_ID


@pytest.mark.asyncio
async def test_authenticate():
    storage = Backblaze(account_id=BACKBLAZE_ACCOUNT_ID,
                        app_key=BACKBLAZE_APP_KEY)
    result = await storage.authenticate()
    assert {'apiUrl', 'authorizationToken'}.issubset(result)
