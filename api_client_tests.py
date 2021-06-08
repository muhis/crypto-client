from datetime import datetime
from unittest import TestCase
from backend import B2C2ApiClient
from models import CreatedRequestForQuote, RequestForQuote, TransactionSide, Instrument
import responses
import requests
import random

class B2C2ApiClientTest(TestCase):
    @responses.activate
    def test_request_for_quote__handle_request_error(self):
        responses.add(
            responses.POST, f'{B2C2ApiClient.BASE_URL}/request_for_quote/',
            status=400
        )
        mock_rfq = self._create_mock_rfq_object()
        with self.assertRaises(requests.exceptions.HTTPError):
            api_client = B2C2ApiClient()
            api_client.request_for_quote(mock_rfq)

    @responses.activate
    def test_request_for_quote__success(self):
        mock_rfq_object = self._create_mock_rfq_object()
        created_rfq_object = self._create_mock_created_rfq_object(rfq_object=mock_rfq_object)
        responses.add(
            responses.POST, f'{B2C2ApiClient.BASE_URL}/request_for_quote/',
            status=200, body=created_rfq_object.json(), content_type='application/json'
        )
        api_client = B2C2ApiClient()
        created_quote = api_client.request_for_quote(mock_rfq_object)
        self.assertEqual(type(created_quote), CreatedRequestForQuote)
        self.assertEqual(created_quote, created_rfq_object)

    def _create_mock_rfq_object(self):
        return RequestForQuote(
            side=TransactionSide.buy,
            quantity=20,
            instrument=Instrument.BTCUSD_SPOT,
            price=1234,
        )
    
    def _create_mock_created_rfq_object(self, rfq_object):
        return CreatedRequestForQuote(
            created=datetime.now(),
            price=(random.random() * 10),
            **rfq_object.dict()
        )