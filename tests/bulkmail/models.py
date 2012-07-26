from decimal import Decimal

from django.test import TestCase
"""
from arbitrage.models import Stock
from .factories import StockIntradeFactory


class StockTestCase(TestCase):
    def test_intrade_fields_limited(self):
        fields = ['symbol', 'last_trade_price', 'bid']
        returned = Stock.intrade_fields(743474, fields)
        # returned dict has same number of items
        self.assertItemsEqual(returned.keys(), fields)
        self.assertIsInstance(returned['bid'], Decimal)

    def test_intrade_fields_values(self):
        fields = ['symbol', 'last_trade_price', 'bid', 'ask']
        returned = Stock.intrade_fields(743474, fields)
        value_fields = ['last_trade_price', 'bid', 'ask']
        for decimal_value in [returned[field] for field in value_fields]:
            self.assertIsInstance(decimal_value, Decimal)
            self.assertLessEqual(decimal_value, 1)
            self.assertGreaterEqual(decimal_value, 0)

    def test_intrade_save(self):
        stock = StockIntradeFactory()
"""
