"""
Class for interacting with the Backblaze cloud storage REST API.
"""
import hashlib
import logging
import os
import urllib.parse

import aiohttp

from .exceptions import BackblazeAuthorisationError, BackblazeGetUploadUrlError


logger = logging.getLogger(__name__)


class Backblaze:

    API_NAME = 'b2api/'
    API_VERSION = 'v1/'
    API_DOMAIN = 'https://api.backblazeb2.com'
    API_ENDPOINTS = {
        'list_buckets': 'b2_list_buckets/',
        'get_upload_url': 'b2_get_upload_url/',
        'authorize_account': 'b2_authorize_account/',
    }

    def __init__(self, credentials):
        self._account_id = credentials['account_id']
        self._app_key = credentials['app_key']
        self._authorized_base_url = None
        self._authorization_token = None
        self._authorized_session = None

    def _get_api_url(self, action):
        """
        Generate API endpoint URL.

        :param str action: API action to get URL for.
        :return: API endpoint URL.
        :rtype: str
        """
        path = '{}{}{}'.format(self.API_NAME, self.API_VERSION,
                               self.API_ENDPOINTS[action])
        if self._authorized_base_url is None:
            return urllib.parse.urljoin(self.API_DOMAIN, path)
        else:
            return urllib.parse.urljoin(self._authorized_base_url, path)

    async def authenticate(self):
        """
        Authenticate to the API and update authorization attributes.

        :raise ClientResponseError: If HTTP status error code.
        :return: JSON API response containing authorization details.
        :rtype: dict
        """
        url = self._get_api_url('authorize_account')
        auth = aiohttp.BasicAuth(self._account_id, self._app_key)
        required = ('apiUrl', 'authorizationToken')
        async with aiohttp.ClientSession(auth=auth) as session:
            async with session.get(url, timeout=30) as response:
                response.raise_for_status()
                response_js = await response.json()
                if all(r in response_js for r in required):
                    self._authorized_base_url = response_js['apiUrl']
                    self._authorization_token = response_js['authorizationToken']  # noqa
                    self._authorized_session = aiohttp.ClientSession(
                        headers={'Authorization': self._authorization_token})
                    return response_js

    async def _get_upload_url(self, bucket_id):
        """
        Retrieve URL used for uploading a file.

        :param bucket_id: bucket to upload file to.
        :raise ClientResponseError: If HTTP status error code.
        :return: JSON API response containing upload URL.
        :rtype: dict
        """
        if self._authorized_session is None:
            raise BackblazeAuthorisationError
        url = self._get_api_url('get_upload_url')
        required = ('uploadUrl', 'authorizationToken')
        async with self._authorized_session as session:
            async with session.post(
                    url, json={'bucketId': bucket_id}) as response:
                response.raise_for_status()
                response_js = await response.json()
                if all(r in response_js for r in required):
                    return response_js

    async def upload_file(self, bucket_id, file_to_upload, content_type):
        """
        Upload file.

        :param bucket_id: bucket to upload file to.
        :param file_to_upload: path of file to upload.
        :param content_type: content (MIME) type of file to upload.
        :return: JSON API response containing confirmation of file upload.
        :rtype: dict
        """
        upload_info = await self._get_upload_url(bucket_id)
        if not upload_info:
            raise BackblazeGetUploadUrlError
        upload_url = upload_info['uploadUrl']
        upload_token = upload_info['authorizationToken']
        with open(file_to_upload, 'rb') as f:
            file_data = f.read()
        upload_headers = {
            'Authorization': upload_token,
            'X-Bz-File-Name': urllib.parse.quote(
                os.path.basename(file_to_upload)),
            'Content-Type': content_type,
            'X-Bz-Content-Sha1': hashlib.sha1(file_data).hexdigest()
        }
        async with aiohttp.ClientSession(
                headers=upload_headers) as session:
            async with session.post(
                    upload_url, data=file_data) as response:
                response.raise_for_status()
                response_js = await response.json()
                return response_js
