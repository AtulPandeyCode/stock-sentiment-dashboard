import yfinance as yf
import time


def fetch_stock_info(ticker):
    """
    Fetch stock information and price history.
    Returns: (info_dict, history_dataframe)
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Retry history up to 3 times
        hist = None
        for attempt in range(3):
            try:
                hist = stock.history(period="1mo")
                if not hist.empty:
                    break
            except Exception:
                print(f"History attempt {attempt + 1} failed, retrying...")
                time.sleep(2)

        return info, hist
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return {}, None


def validate_ticker(ticker):
    """
    Returns True if ticker is valid, False otherwise.
    """
    try:
        info = yf.Ticker(ticker).info
        return bool(info.get("shortName"))
    except:
        return False