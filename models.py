from typing import List, Optional
from uuid import uuid4
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


class Created(BaseModel):
    created: datetime = Field(default_factory=datetime.now)


class Priced(BaseModel):
    price: PositiveFloat


class RequestForQuote(Transaction):
    rfq_id: UUID4 = Field(default_factory=uuid4)


class CreatedRequestForQuote(RequestForQuote, Created, Priced):
    pass


class Trade(Transaction, Created, Priced):
    trade_id: UUID4
    origin: str
    order: UUID4
    executing_unit: str


class Order(Transaction, Created, Priced):
    order_id: UUID4 = Field(default_factory=uuid4)
    client_order_id: UUID4 = Field(default_factory=uuid4)
    executed_price: PositiveFloat
    executing_unit: str
    trades: Optional[List[Trade]]
