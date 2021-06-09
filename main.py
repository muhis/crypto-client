import enum
from prompt_toolkit.shortcuts import dialogs
from prompt_toolkit.validation import ValidationError
from traitlets.traitlets import default
from serializers import enum_to_choices
from models import Instrument, NonExecutedOrder, OrderType, TransactionSide, RequestForQuote
from tabulate import tabulate
from backend import B2C2ApiClient
from logging import getLogger

log = getLogger(__name__)


def balance():
    print(B2C2ApiClient().get_balances())


def create_rfq() -> RequestForQuote:
    trade_side_direction = enum_to_choices(TransactionSide)
    trade_side = dialogs.radiolist_dialog(
        title="Trade",
        text="What would you like to do ?",
        values=trade_side_direction,
    ).run()
    quantity = dialogs.input_dialog(
        title="Trade",
        text="How much you want to trade ?",
    ).run()
    instruments_choices = enum_to_choices(Instrument)
    instrument = dialogs.radiolist_dialog(
        title="Trade",
        text="Pick an instrument for trade",
        values=instruments_choices
    ).run()

    rfq = RequestForQuote(
        side=trade_side,
        quantity=quantity,
        instrument=instrument
    )
    log.info(rfq)
    return rfq


def execute_order(created_rfq):
    confirmation_question = f"""
        Do you want to execute the trade {created_rfq.side} with quantity {created_rfq.quantity}
        created at {created_rfq.created}?
    """
    is_execute_granted = dialogs.radiolist_dialog(
        title="Trade",
        text=confirmation_question,
        values=[('yes', 'Yes'), ('no', 'No')]
    ).run()
    if not is_execute_granted:
        return
    if created_rfq.is_stale():
        raise ValidationError('The request for quote has expired')
    order_type_choices = enum_to_choices(OrderType)
    order_type = dialogs.radiolist_dialog(
        title="Trade",
        text="Select order type",
        values=order_type_choices
    ).run()
    acceptable_slippage_in_basis_points = dialogs.input_dialog(
        title="Trade",
        text="Do you want to set slippage base point?",
    ).run()
    acceptable_slippage_in_basis_points =acceptable_slippage_in_basis_points or None
    executing_unit = dialogs.input_dialog(
        title="Trade",
        text="What is the executing unit",
    ).run()
    non_executed_order = NonExecutedOrder(
        order_type=order_type,
        acceptable_slippage_in_basis_points=acceptable_slippage_in_basis_points,
        executing_unit=executing_unit,
        **created_rfq.dict(),
    )
    executed_order = B2C2ApiClient().execute_order(non_executed_order)
    print(executed_order)
    balance()

def trade():
    rfq = create_rfq()
    created_rfq = B2C2ApiClient().request_for_quote(rfq)
    executed_order = execute_order(created_rfq)
    print(executed_order)


def route_user():
    operations = [
        ('trade', 'Trade'),
        ('balances', 'Balances'),
    ]
    user_choice = dialogs.radiolist_dialog(
        title="Chose an operation",
        text="What would you like to do ?",
        values=operations
    ).run()
    if user_choice == 'balances':
        balance()
    elif user_choice == 'trade':
        trade()


if __name__ == "__main__":
    route_user()