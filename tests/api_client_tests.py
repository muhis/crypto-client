from datetime import date, datetime
from unittest import TestCase
from backend import B2C2ApiClient
from models import CreatedRequestForQuote, RequestForQuote, TransactionSide, Instrument, ExecutedOrder, Order
from models import OrderType
import responses
import requests
import random
from tests.mock_responses import CREATE_RFQ, EXECUTE_ORDER
import json
from tests.factories import ModelsFactory


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

    @responses.activate
    def test_validator(self):
        """Test with response from documentation"""
        mock_rfq_object = self._create_mock_rfq_object()
        responses.add(
            responses.POST, f'{B2C2ApiClient.BASE_URL}/request_for_quote/',
            status=200, body=json.dumps(CREATE_RFQ), content_type='application/json'
        )
        api_client = B2C2ApiClient()
        created_quote = api_client.request_for_quote(mock_rfq_object)
        self.assertEqual(type(created_quote), CreatedRequestForQuote)

    @responses.activate
    def test_execute_order(self):
        order = ModelsFactory.NoneExecutedOrder()
        mock_executed_order = ModelsFactory.ExecutedOrder(order=order)
        responses.add(
            responses.POST, f'{B2C2ApiClient.BASE_URL}/order/',
            status=200, body=mock_executed_order.json(), content_type='application/json'
        )
        api_client = B2C2ApiClient()
        executed_order = api_client.execute_order(order=order)
        self.assertEqual(executed_order, mock_executed_order)

    @responses.activate
    def test_execute_order__documentation_response(self):
        order = ModelsFactory.NoneExecutedOrder()
        mock_executed_order = ExecutedOrder(**EXECUTE_ORDER)
        
        responses.add(
            responses.POST, f'{B2C2ApiClient.BASE_URL}/order/',
            status=200, body=json.dumps(EXECUTE_ORDER), content_type='application/json'
        )
        api_client = B2C2ApiClient()
        executed_order = api_client.execute_order(order=order)
        self.maxDiff = None
        self.assertEqual(executed_order.json(), mock_executed_order.json())

    def _create_mock_rfq_object(self):
        return RequestForQuote(
            side=TransactionSide.BUY,
            quantity=20,
            instrument=Instrument.BTCUSD_SPOT,
            price=1234,
        )
    
    def _create_mock_created_rfq_object(self, rfq_object):
        return CreatedRequestForQuote(
            valid_until=datetime.now(),
            created=datetime.now(),
            price=(random.random() * 10),
            **rfq_object.dict()
        )
    
    def _create_order(self) -> Order:
        return Order(
            executing_unit='Test client',
            order_type=OrderType.FOK,
            price=1122,
            side=TransactionSide.SELL,
            quantity=20,
            instrument=Instrument.BTCUSD_SPOT,
        )
    
