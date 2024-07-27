import unittest
from unittest.mock import patch, MagicMock
from main import _get_stock_data, _is_market_open, \
    monitor_stock_price
from datetime import datetime, timedelta
import pytz

class TestStockMonitor(unittest.TestCase):

    @patch('main.yf.Ticker')  # Mock `yf.Ticker`
    def test_get_stock_data(self, MockTicker):
        # Set up the mock
        mock_ticker = MockTicker.return_value
        mock_ticker.history.return_value = MagicMock(
            **{'Close': [150.00]}
        )
        mock_ticker.info = {'longName': 'Test Company'}

        target_prices = {'AAPL': 180.00}
        expected = {
            'AAPL': {
                'stock': mock_ticker,
                'current_price': 150.00,
                'company_name': 'Test Company'
            }
        }

        result = _get_stock_data(target_prices)
        self.assertEqual(result, expected)

    @patch('main.mcal.get_calendar')
    @patch('main.pytz.timezone')
    def test_is_market_open(self, MockTimezone, MockGetCalendar):
        # Set up the mock
        mock_timezone = MockTimezone.return_value
        mock_get_calendar = MockGetCalendar.return_value
        mock_schedule = MagicMock()
        mock_schedule.empty = False
        mock_schedule.iloc[0] = {'market_open': datetime(2024, 7, 27, 9, 30),
                                 'market_close': datetime(2024, 7, 27, 16, 0)}
        mock_get_calendar.schedule.return_value = mock_schedule

        # Test case when market is open
        MockTimezone.return_value = pytz.timezone('America/New_York')
        result = _is_market_open()
        self.assertTrue(result)

        # Test case when market is closed
        mock_schedule.empty = True
        result = _is_market_open()
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
