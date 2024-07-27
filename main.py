import time
from plyer import notification
import yfinance as yf
import pandas_market_calendars as mcal
from datetime import datetime, timedelta
import pytz
from typing import Optional


# Function to fetch the current stock prices and stock objects
def _get_stock_data(target_prices: dict) -> Optional[dict]:
    """
    Fetches the current stock prices and stock objects for the given symbols.

    Args:
        target_prices (dict): A dictionary of symbols and their target prices.

    Returns:
        Optional[dict]: A dictionary of stock data for each symbol, or None if an error occurs.

    Raises:
        Exception: If there is an error fetching stock data.
    """
    symbols = list(target_prices.keys())
    try:
        stock_data = {}
        for symbol in symbols:
            # Create a new Ticker object for the symbol
            stock = yf.Ticker(symbol)

            # Get the current price of the stock
            current_price = stock.history(period='1d')['Close'].iloc[-1]

            # Get the company name from the stock info
            company_name = stock.info['longName']

            # Add the stock data to the dictionary
            stock_data[symbol] = {
                'stock': stock,
                'current_price': current_price,
                'company_name': company_name
            }
        return stock_data
    except Exception as e:
        # Print the error message and return None
        print("Error fetching stock data:", e)
        return None


# Function to check if the market is open
def _is_market_open() -> bool:
    """
    Check if the NYSE market is currently open.

    Returns:
        bool: True if the market is open, False otherwise.
    """
    # Get the NYSE calendar
    nyse = mcal.get_calendar('NYSE')

    # Get the current time in New York timezone
    current_time = datetime.now(pytz.timezone('America/New_York'))

    # Get the market schedule for the next day
    schedule = nyse.schedule(
        start_date=current_time.strftime('%Y-%m-%d'),
        end_date=(current_time + timedelta(days=1)).strftime('%Y-%m-%d')
    )

    # Check if there is a schedule for the current day
    if not schedule.empty:
        # Get the market open and close times
        market_open = schedule.iloc[0]['market_open'].to_pydatetime()
        market_close = schedule.iloc[0]['market_close'].to_pydatetime()

        # Check if the current time is within the market hours
        return market_open <= current_time <= market_close

    # If there is no schedule, assume the market is closed
    return False


# Main function to continuously monitor the stock prices and trigger reminder
def monitor_stock_price(target_prices: dict) -> Optional[dict]:
    """
    Continuously monitors the stock prices and triggers a notification if the price is within the target range.

    Args:
        target_prices (dict): A dictionary mapping stock symbols to their target prices.

    Returns:
        None
    """
    while True:
        if _is_market_open():
            stock_data = _get_stock_data(target_prices)
            if stock_data is not None:
                for symbol, data in stock_data.items():
                    # Print company name
                    print(f"Stock: {symbol} ({data['company_name']})")

                    # Print current price
                    current_price = data['current_price']
                    print(f"Current Price: {current_price}")

                    # Get target price for the symbol
                    target_price = target_prices.get(symbol)

                    # Print target price
                    print(f"Target Price: {target_price}")

                    if target_price is not None:
                        # Calculate the lower and upper bounds for the target range
                        lower_bound = target_price * 0.9
                        upper_bound = target_price * 1.05

                        # Check if the current price is within the target range
                        if lower_bound <= current_price <= upper_bound:
                            # Construct notification message
                            notification_title = f"STOCK CHECKER"
                            notification_message = (
                                f"{data['company_name']} ({symbol})\n"
                                f"Current Price: ${current_price:.2f}\n"
                                f"Target Range: ${lower_bound:.2f} - ${upper_bound:.2f}\n"
                                f"Keep an eye on this one! O__o"
                            )
                            notification_timeout = 30  # Notification will automatically close after 10 seconds

                            # Trigger notification
                            notification.notify(
                                title=notification_title,
                                message=notification_message,
                                timeout=notification_timeout,
                                app_icon='box_yellow.ico',  # Path to the app icon
                                app_name='Stock Checker',  # Custom app name
                                ticker=f"{symbol}"  # Ticker symbol associated with the app
                            )
                        elif current_price < lower_bound:
                            # Construct notification message
                            notification_title = f"STOCK CHECKER"
                            notification_message = (
                                f"{data['company_name']} ({symbol})\n"
                                f"Current Price: ${current_price:.2f}\n"
                                f"This is below the target range.\n"
                                f"Consider buying now! "
                            )
                            notification_timeout = 30  # Notification will automatically close after 10 seconds

                            # Trigger notification
                            notification.notify(
                                title=notification_title,
                                message=notification_message,
                                timeout=notification_timeout,
                                app_icon='Box_Green.ico',  # Path to the app icon
                                app_name='Stock Checker',  # Custom app name
                                ticker=f"{symbol}"  # Ticker symbol associated with the app
                            )
        time.sleep(3600)


if __name__ == "__main__":
    # Define target prices for stocks
    target_prices = {'AAPL': 183.00, 'O': 52.50, 'MAIN': 48.50,
                     'GAIN': 13.60, 'STAG': 34.00, 'MSFT': 390.00}

    # Start monitoring the stock prices
    monitor_stock_price(target_prices)
