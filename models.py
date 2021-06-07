from typing import List, Optional
from uuid import uuid4
import ipdb
from pydantic import BaseModel, Field, PositiveFloat
import pydantic
from datetime import datetime
from pydantic.types import UUID4
from enum import Enum, IntEnum


class TransactionSide(str, Enum):
    buy: str = "buy"
    sell: str = "sell"


class Instrument(str, Enum):
    BTCUSD_SPOT: str = "BTCUSD.SPOT"


class Transaction(BaseModel):
    side: TransactionSide
    quantity: PositiveFloat
    instrument: Instrument
    price: PositiveFloat
    created: datetime = Field(default_factory=datetime.now)


class RequestForQuote(Transaction):
    rfq_id: UUID4 = Field(default_factory=uuid4)


class Trade(Transaction):
    trade_id: UUID4
    origin: str
    order: UUID4
    executing_unit: str


class Order(Transaction):
    order_id: UUID4 = Field(default_factory=uuid4)
    client_order_id: UUID4 = Field(default_factory=uuid4)
    executed_price: PositiveFloat
    executing_unit: str
    trades: Optional[List[Trade]]


def create_dummy_rfq() -> RequestForQuote:
    return RequestForQuote(
        side=TransactionSide.buy,
        quantity=20,
        instrument=Instrument.BTCUSD_SPOT,
        price=1234,
    )

{
    "valid_until": "2017-01-01T19:45:22.025464Z",
    "rfq_id": "d4e41399-e7a1-4576-9b46-349420040e1a",
    "client_rfq_id": "149dc3e7-4e30-4e1a-bb9c-9c30bd8f5ec7",
    "quantity": "1.0000000000",
    "side": "buy",
    "instrument": "BTCUSD.SPOT",
    "price": "700.00000000",
    "created": "2018-02-06T16:07:50.122206Z"
}
