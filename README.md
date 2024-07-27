# Stock Price Monitor

This Python script monitors the stock prices of specified companies and sends desktop notifications when the current prices are within a defined target range. It uses the `yfinance` library to fetch stock data, `pandas_market_calendars` to check market hours, and `plyer` to display notifications.

## Requirements

- Python 3.7+
- yfinance
- plyer
- pandas_market_calendars
- pytz

## Installation

To install the necessary packages, run:

```bash
pip install yfinance plyer pandas_market_calendars pytz
```

## Usage

The script defines a function to monitor stock prices, fetching data at regular intervals and notifying the user if certain conditions are met.

### Monitor Stock Prices

To start monitoring stock prices, define a dictionary of target prices for the desired stock symbols and call the `monitor_stock_price` function with this dictionary as the argument.

### Example

```python
from stock_monitor import monitor_stock_price

if __name__ == "__main__":
    target_prices = {
        'AAPL': 183.00,
        'O': 52.50,
        'MAIN': 48.50,
        'GAIN': 13.60,
        'STAG': 34.00,
        'MSFT': 390.00
    }

    monitor_stock_price(target_prices)
```

## How It Works

1. **Fetching Stock Data**: The script uses `yfinance` to get the current stock prices and company names.
2. **Checking Market Hours**: It checks if the market is open using `pandas_market_calendars`.
3. **Notification Trigger**: The script sends notifications using `plyer` if the stock price is within a specified target range or below a certain threshold.

### Notification Details

- The notification includes the company name, current stock price, and target range.
- Different messages and icons can be set for various stock price conditions.

## Functions

- `_get_stock_data(target_prices: dict) -> Optional[dict]`  
  Fetches the current stock prices and stock objects for the given symbols.

  **Args**:  
  - `target_prices (dict)`: A dictionary of symbols and their target prices.

  **Returns**:  
  - `Optional[dict]`: A dictionary of stock data for each symbol, or `None` if an error occurs.

- `_is_market_open() -> bool`  
  Checks if the NYSE market is currently open.

  **Returns**:  
  - `bool`: True if the market is open, False otherwise.

- `monitor_stock_price(target_prices: dict)`  
  Continuously monitors the stock prices and triggers a notification if the price is within the target range.

  **Args**:  
  - `target_prices (dict)`: A dictionary mapping stock symbols to their target prices.

  **Returns**:  
  - None

## Notes

- Ensure the script runs continuously to monitor the stock prices effectively.
- Customize the target prices and notification settings as needed.

This script provides a convenient way to keep track of stock prices and receive timely alerts, helping investors make informed decisions.
