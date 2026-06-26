import yfinance as yf
import time

def fetch_stock_info(ticker):
    for attempt in range(3):  # try 3 times
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            if info.get("shortName"):  # valid response
                hist = stock.history(period="1mo")
                return info, hist
            time.sleep(2)  # wait 2 sec before retry
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(2)
    return {}, None

def validate_ticker(ticker):
    info, _ = fetch_stock_info(ticker)
    return bool(info.get("shortName"))