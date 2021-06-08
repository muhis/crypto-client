from uuid import uuid4
import models
from models import ExecutedOrder, Order, TransactionSide, Instrument, OrderType
from typing import List, Optional

class OrderFactory():
    executing_unit='Test client'
    order_type=OrderType.FOK
    price=1122.1
    side=TransactionSide.SELL
    quantity=20
    instrument=Instrument.BTCUSD_SPOT


class ExecutedOrderFactory():
    executing_unit='Test client'
    order_type=OrderType.FOK
    price="1122.2"
    side=TransactionSide.SELL
    quantity=20
    instrument=Instrument.BTCUSD_SPOT


class ExecutedOrderFactory():
    order_id = uuid4()


class ModelsFactory():
    @staticmethod
    def NoneExecutedOrder() -> models.NonExecutedOrder:
        return models.NonExecutedOrder(
            executing_unit='Test client',
            order_type=OrderType.FOK,
            price=1122.1,
            side=TransactionSide.SELL,
            quantity=20,
            instrument=Instrument.BTCUSD_SPOT,
        )
    
    @classmethod
    def ExecutedOrder(cls, order: Optional[models.Order]=None, trades: List[Optional[models.Trade]]=[]):
        if not order:
            payload = {
                'executing_unit':'Test client',
                'order_type':OrderType.FOK,
                'price':1122.1,
                'side':TransactionSide.SELL,
                'quantity':20,
                'instrument':Instrument.BTCUSD_SPOT,
            }
        else:
            payload = order.dict()

        trades = trades if trades else [cls.Trade()]
        return models.ExecutedOrder(
            order_id=uuid4(),
            trades=trades,
            **payload
        )

    def Trade() -> models.Trade:
        return models.Trade(
            **{
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
        )