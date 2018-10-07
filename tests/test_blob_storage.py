import asynctest
import pytest

from aiostorage.blob_storage import BlobStorage
from aiostorage.exceptions import BlobStorageUnrecognizedProviderError
from aiostorage.providers.backblaze import Backblaze
from aiostorage.providers.exceptions import (BackblazeAuthenticationError,
                                             BackblazeFileUploadError)


@pytest.fixture
def storage():
    provider = 'backblaze'
    credentials = {
        'account_id': '23424',
        'app_key': 'sdfsdfs',
    }
    return BlobStorage(provider, credentials)


def test_instance(storage):
    assert storage.provider


def test_instance_unrecognized_provider():
    provider = 'Fake'
    credentials = {
        'account_id': '23423',
        'app_key': 'sdfsdf',
    }
    with pytest.raises(BlobStorageUnrecognizedProviderError):
        BlobStorage(provider, credentials)


def test_instance_bad_credentials():
    provider = 'backblaze'
    credentials = {
        'accountId': '23423',
        'appKey': 'sdfsdf',
    }
    with pytest.raises(KeyError):
        BlobStorage(provider, credentials)


def fake_provider_authenticate_side_effect():
    return {'token': '23490xnzz3dfsejisdfa'}


def fake_provider_upload_file_side_effect(bucket_id, file_to_upload,
                                          content_type):
    return {'fileUploaded': file_to_upload, 'fileId': 234234,
            'fileBucketId': bucket_id, 'fileContentType': content_type}


@pytest.fixture
def mock_provider_authenticate(monkeypatch):
    fake_provider_authenticate = asynctest.CoroutineMock(
        Backblaze.authenticate,
        side_effect=fake_provider_authenticate_side_effect
    )
    monkeypatch.setattr(Backblaze, 'authenticate', fake_provider_authenticate)
    return fake_provider_authenticate


@pytest.fixture
def mock_provider_upload_file(monkeypatch):
    fake_provider_upload_file = asynctest.CoroutineMock(
        Backblaze.upload_file,
        side_effect=fake_provider_upload_file_side_effect)
    monkeypatch.setattr(Backblaze, 'upload_file', fake_provider_upload_file)
    return fake_provider_upload_file


@pytest.mark.asyncio
async def test__upload_file(storage, mock_provider_authenticate,
                            mock_provider_upload_file):
    bucket_id = '3432'
    file_to_upload = {'content_type': 'video/mp4', 'path': 'hello.mp4'}
    fake_result = {
        'fileUploaded': file_to_upload['path'],
        'fileId': 234234,
        'fileBucketId': bucket_id,
        'fileContentType': file_to_upload['content_type']
    }
    assert fake_result == await storage._upload_file(bucket_id, file_to_upload)


def fake_provider_authenticate_error_side_effect():
    return {}


@pytest.fixture
def mock_provider_authenticate_error(monkeypatch):
    fake_provider_authenticate_error = asynctest.CoroutineMock(
        Backblaze.authenticate,
        side_effect=fake_provider_authenticate_error_side_effect
    )
    monkeypatch.setattr(
        Backblaze, 'authenticate', fake_provider_authenticate_error)
    return fake_provider_authenticate_error


@pytest.mark.asyncio
async def test__upload_file_authentication_error(
    storage,
    mock_provider_authenticate_error
):
    bucket_id = '3432'
    file_to_upload = {'content_type': 'video/mp4', 'path': 'hello.mp4'}
    with pytest.raises(BackblazeAuthenticationError):
        await storage._upload_file(bucket_id, file_to_upload)


def fake_provider_upload_file_error_side_effect(bucket_id, file_to_upload,
                                                content_type):
    return {}


@pytest.fixture
def mock_provider_upload_file_error(monkeypatch):
    fake_provider_upload_file_error = asynctest.CoroutineMock(
        Backblaze.upload_file,
        side_effect=fake_provider_upload_file_error_side_effect
    )
    monkeypatch.setattr(
        Backblaze, 'upload_file', fake_provider_upload_file_error)
    return fake_provider_upload_file_error


@pytest.mark.asyncio
async def test__upload_file_upload_file_error(
    storage,
    mock_provider_upload_file_error,
    mock_provider_authenticate
):
    bucket_id = '3432'
    file_to_upload = {'content_type': 'video/mp4', 'path': 'hello.mp4'}
    with pytest.raises(BackblazeFileUploadError):
        await storage._upload_file(bucket_id, file_to_upload)
