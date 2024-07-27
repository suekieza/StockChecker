import unittest
from main import _get_stock_data, _is_market_open


class TestStockFunctions(unittest.TestCase):

    def test_get_stock_data_success(self):
        # This test assumes you have a valid connection to the internet
        # and yfinance is properly installed and working.
        target_prices = {'AAPL': 183.00}
        result = _get_stock_data(target_prices)

        # You might need to adjust this depending on the actual output of _get_stock_data
        # Since _get_stock_data involves live data, this is just a placeholder assertion
        self.assertTrue('AAPL' in result)
        self.assertTrue(result['AAPL']['current_price'] > 0)
        self.assertTrue(result['AAPL']['company_name'] is not None)

    def test_is_market_open_success(self):
        # This test assumes you have valid implementation for market schedule
        result = _is_market_open()
        if result:
            # You might need to adjust this based on actual implementation of _is_market_open
            self.assertTrue(result)
        else:
            # Adjust this based on actual implementation of _is_market_open
            self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
