from typing import Dict
import requests
from models import Balances, ExecutedOrder, NonExecutedOrder, RequestForQuote, CreatedRequestForQuote, Order, ExecutedOrder


BASE_URL = 'https://api.uat.b2c2.net/'


class B2C2ApiClient(object):
    BASE_URL: str = BASE_URL

    def request_for_quote(self, rfq_object: RequestForQuote) -> CreatedRequestForQuote:
        url = self._construct_url('request_for_quote')
        response = requests.post(
            url=url, data=rfq_object.json(), headers=self._headers,
        )
        response.raise_for_status()
        return CreatedRequestForQuote(**response.json())

    def execute_order(self, order: NonExecutedOrder) -> ExecutedOrder:
        url = self._construct_url('order')
        response = requests.post(
            url=url, data=order.json(), headers=self._headers,
        )
        response.raise_for_status()
        return ExecutedOrder(**response.json())

    def get_balances(self):
        url = self._construct_url('balance')
        response = requests.get(
            url=url, headers=self._headers,
        )
        return Balances(**response.json())

    def _construct_url(self, endpoint: str) -> str:
        return f'{self.BASE_URL}/{endpoint}/'

    @property
    def _headers(self) -> Dict[str, str]:
        api_token = 'e13e627c49705f83cbe7b60389ac411b6f86fee7'
        return {'Authorization': f'Token {api_token}'}
