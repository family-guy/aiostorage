import pytest

from aiostorage.providers import Backblaze


@pytest.fixture
def provider_storage():
    credentials = {
        'account_id': '23424',
        'app_key': 'sdfsdfs',
    }
    return Backblaze(credentials)


@pytest.mark.parametrize(
    ('action', 'authorized_base_url', 'expected'),
    (
        ('authorize_account', None,
         'https://api.backblazeb2.com/b2api/v1/b2_authorize_account/'),
        ('get_upload_url', 'https://abc.com',
         'https://abc.com/b2api/v1/b2_get_upload_url/'),
        ('list_buckets', 'https://xyz.com',
         'https://xyz.com/b2api/v1/b2_list_buckets/'),
    )
)
def test__get_api_url(provider_storage, action, authorized_base_url, expected):
    provider_storage.authorized_base_url = authorized_base_url
    assert provider_storage._get_api_url(action) == expected
