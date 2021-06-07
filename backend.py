from typing import Dict
import requests
import uuid
from models import RequestForQuote, create_dummy_rfq
from dataclasses import dataclass
BASE_URL = 'http://127.0.0.1:8000/api.uat.b2c2.net'

class B2C2ApiClient(object):
    BASE_URL: str = BASE_URL

    def request_for_quote(self, rfq_object):
        url = self._construct_url('request_for_quote')
        try:
            response = requests.post(url=url, data=rfq_object.json(), headers=create_headers())
            import ipdb; ipdb.set_trace()
            response.raise_for_status()
        except requests.RequestException as error:
            print(error)
        else:
            return RequestForQuote(**response.json())

    def _construct_url(self, endpoint: str) ->str:
        return f'{self.BASE_URL}/{endpoint}/'



def create_headers() ->Dict[str, str]:
    api_token = '9b44b09199c61bcf9416ad846dd0e4'
    return {'Authorization': 'Token %s' % api_token}

uuid = str(uuid.uuid4())
quantity = '1'
side = 'buy'
instrument = 'BTCUSD.SPOT'

post_data = {
    'instrument': instrument,
    'side': side,
    'quantity': quantity,
    'client_rfq_id': uuid
}

def _create_request(payload: dict[str, str]) -> requests.Request:
    headers = create_headers()
    return requests.post('http://127.0.0.1:8000/api.uat.b2c2.net/request_for_quote/', json=post_data, headers=create_headers())

def test():
    rfq = create_dummy_rfq()
    api_client = B2C2ApiClient()
    return api_client.request_for_quote(rfq)

test()