from datetime import date, datetime
from unittest import TestCase

from pydactory.pydactory import Factory
from backend import B2C2ApiClient
from models import Balances, CreatedRequestForQuote, RequestForQuote, TransactionSide, Instrument, ExecutedOrder, Order
from models import OrderType
import responses
import requests
import random
from tests.mock_responses import CREATE_RFQ, EXECUTE_ORDER, GET_BALANCES
import json
from tests.factories import ModelsFactory


class B2C2ApiClientTest(TestCase):
    @responses.activate
    def test_request_for_quote__handle_request_error(self):
        responses.add(
            responses.POST, f'{B2C2ApiClient.BASE_URL}/request_for_quote/',
            status=400
        )
        mock_rfq = ModelsFactory.RequestForQuote()
        with self.assertRaises(requests.exceptions.HTTPError):
            api_client = B2C2ApiClient()
            api_client.request_for_quote(mock_rfq)

    @responses.activate
    def test_request_for_quote__success(self):
        mock_rfq_object = ModelsFactory.RequestForQuote()
        created_rfq_object = ModelsFactory.CreatedRequestForQuote(rfq=mock_rfq_object)
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
        mock_rfq_object = ModelsFactory.RequestForQuote()
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
        self.assertEqual(executed_order.json(), mock_executed_order.json())
    
    @responses.activate
    def test_get_balances(self):
        mock_balances = ModelsFactory.Balances()
        responses.add(
            responses.GET, f'{B2C2ApiClient.BASE_URL}/balance/',
            status=200, body=mock_balances.json(), content_type='application/json'
        )
        api_client = B2C2ApiClient()
        balances = api_client.get_balances()
        self.assertEqual(balances, mock_balances)
    
    @responses.activate
    def test_get_balanaces__documentation_repsonse(self):
        responses.add(
            responses.GET, f'{B2C2ApiClient.BASE_URL}/balance/',
            status=200, body=json.dumps(GET_BALANCES), content_type='application/json'
        )
        expected_balances = ModelsFactory.Balances(balance=0)
        api_client = B2C2ApiClient()
        balances = api_client.get_balances()
        self.assertEqual(balances, expected_balances)
