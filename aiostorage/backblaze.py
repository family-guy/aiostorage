import urllib.parse

import aiohttp


class Backblaze:

    API_NAME = 'b2api/'
    API_VERSION = 'v1/'
    API_DOMAIN = 'https://api.backblazeb2.com'
    API_ENDPOINTS = {
        'list_buckets': 'b2_list_buckets/',
        'get_upload_url': 'b2_get_upload_url/',
        'authorize_account': 'b2_authorize_account/',
    }

    def __init__(self, account_id=None, app_key=None):
        self._account_id = account_id
        self._app_key = app_key
        self._authorized_base_url = None
        self._authorization_token = None
        self._authorized_session = None

    def _create_url(self, api_endpoint):
        path = '{}{}{}'.format(self.API_NAME, self.API_VERSION,
                               self.API_ENDPOINTS[api_endpoint])
        if self._authorized_base_url is None:
            return urllib.parse.urljoin(self.API_DOMAIN, path)
        else:
            return urllib.parse.urljoin(self._authorized_base_url, path)

    async def authenticate(self):
        url = self._create_url('authorize_account')
        auth = aiohttp.BasicAuth(self._account_id, self._app_key)
        async with aiohttp.ClientSession(auth=auth) as session:
            async with session.get(url, timeout=30) as response:
                print('status code', response.status)
                response_js = await response.json()
                print('response', response_js)
                self._authorized_base_url = response_js['apiUrl']
                self._authorization_token = response_js['authorizationToken']
                self._authorized_session = aiohttp.ClientSession(
                    headers={'Authorization': self._authorization_token})
            print('type of session', type(self._authorized_session))
            print('session', self._authorized_session)

    async def f(self):
        url = self._create_url('list_buckets')
        async with self._authorized_session as session:
            async with session.post(url, json={'accountId': self._account_id}) as response:
                print('status code', response.status)
                response_js = await response.json()
                print('response', response_js)




