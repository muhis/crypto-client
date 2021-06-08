from typing import Dict
import requests
from models import RequestForQuote, CreatedRequestForQuote


BASE_URL = 'http://127.0.0.1:8000/api.uat.b2c2.net'


class B2C2ApiClient(object):
    BASE_URL: str = BASE_URL

    def request_for_quote(self, rfq_object: RequestForQuote) -> CreatedRequestForQuote:
        url = self._construct_url('request_for_quote')
        response = requests.post(
            url=url, data=rfq_object.json(), headers=self._headers,
        )
        response.raise_for_status()
        return CreatedRequestForQuote(**response.json())

    def _construct_url(self, endpoint: str) -> str:
        return f'{self.BASE_URL}/{endpoint}/'

    @property
    def _headers(self) -> Dict[str, str]:
        api_token = '9b44b09199c61bcf9416ad846dd0e4'
        return {'Authorization': 'Token %s' % api_token}
