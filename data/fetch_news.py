import requests
from datetime import datetime, timedelta

def fetch_news(ticker, api_key, days=7):
    """
    Fetch recent news articles for a stock ticker.
    Returns: list of dicts with title, url, publishedAt
    """
    if not api_key:
        print("Warning: No API key provided")
        return []

    end_date = datetime.today()
    start_date = end_date - timedelta(days=days)

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": ticker,
        "from": start_date.strftime("%Y-%m-%d"),
        "to": end_date.strftime("%Y-%m-%d"),
        "language": "en",
        "sortBy": "relevancy",
        "apiKey": api_key,
        "pageSize": 20
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            return [
                {
                    "title": a["title"],
                    "description": a.get("description", ""),
                    "url": a["url"],
                    "publishedAt": a["publishedAt"]
                }
                for a in articles
                if a.get("title") and a["title"] != "[Removed]"
            ]
        else:
            print(f"NewsAPI error: {response.status_code} — {response.text}")
            return []
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []