from typing import List, Optional, Union
from uuid import uuid4
from pydantic import BaseModel, Field, PositiveFloat
import pydantic
from datetime import datetime
from pydantic.types import UUID4
from enum import Enum, IntEnum

from pydantic.typing import NoneType
from traitlets.traitlets import Float


class TransactionSide(str, Enum):
    BUY: str = "buy"
    SELL: str = "sell"


class Instrument(str, Enum):
    BTCUSD_SPOT: str = "BTCUSD.SPOT"


class OrderType(str, Enum):
    FOK: str = "FOK"  # Fill or Kill
    MKT: str = "MKT"  # Market Order


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
    valid_until: datetime

    def is_stale(self):
        return self.valid_until < datetime.now()


class Trade(Transaction, Created, Priced):
    trade_id: UUID4
    origin: str
    order: UUID4
    executing_unit: str


class Order(Transaction, Priced):
    client_order_id: UUID4 = Field(default_factory=uuid4)
    executing_unit: str

class NonExecutedOrder(Order):
    order_type: OrderType
    acceptable_slippage_in_basis_points: Optional[PositiveFloat]


class ExecutedOrder(Order, Created):
    order_id: UUID4
    executed_price: Optional[PositiveFloat]
    trades: List[Trade]


class Balances(BaseModel):
    USD: float
    BTC: float
    JPY: float
    GBP: float
    ETH: float
    EUR: float
    CAD: float
    LTC: float
    XRP: float
    BCH: float