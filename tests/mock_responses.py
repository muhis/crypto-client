CREATE_RFQ = {
  "valid_until": "2017-01-01T19:45:22.025464Z",
  "rfq_id": "d4e41399-e7a1-4576-9b46-349420040e1a",
  "client_rfq_id": "149dc3e7-4e30-4e1a-bb9c-9c30bd8f5ec7",
  "quantity": "1.0000000000",
  "side": "buy",
  "instrument": "BTCUSD.SPOT",
  "price": "700.00000000",
  "created": "2018-02-06T16:07:50.122206Z"
}

EXECUTE_ORDER = {
  "order_id": "d4e41399-e7a1-4576-9b46-349420040e1a",
  "client_order_id": "d4e41399-e7a1-4576-9b46-349420040e1a",
  "quantity": "3.0000000000",
  "side": "buy",
  "instrument": "BTCUSD.SPOT",
  "price": "11000.00000000",
  "executed_price": "10457.651100000",
  "executing_unit": "risk-adding-strategy",
  "trades": [
      {
        "instrument": "BTCUSD.SPOT",
        "trade_id": "b2c50b72-92d4-499f-b0a3-dee6b37378be",
        "origin": "rest",
        "rfq_id": None,
        "created": "2018-02-26T14:27:53.675962Z",
        "price": "10457.65110000",
        "quantity": "3.0000000000",
        "order": "d4e41399-e7a1-4576-9b46-349420040e1a",
        "side": "buy",
        "executing_unit": "risk-adding-strategy",
      }
  ],
  "created": "2018-02-06T16:07:50.122206Z"
}

GET_BALANCES = {
  "USD": "0",
  "BTC": "0",
  "JPY": "0",
  "GBP": "0",
  "ETH": "0",
  "EUR": "0",
  "CAD": "0",
  "LTC": "0",
  "XRP": "0",
  "BCH": "0"
}