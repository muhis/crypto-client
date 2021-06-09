from serializers import enum_to_choices
from unittest import TestCase
from models import TransactionSide


class SerializersTest(TestCase):
    def test_enum_serializer(self):
        choices = enum_to_choices(TransactionSide)
        self.assertEqual(choices, [('Buy', 'buy'), ('Sell', 'sell')])

