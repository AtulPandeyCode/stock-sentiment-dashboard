import streamlit as st
import os
from dotenv import load_dotenv

from data.fetch_news import fetch_news
from data.fetch_stock import fetch_stock_info
from sentiment.analyzer import (
    load_finbert,
    analyze_sentiment,
    compute_overall_score,
    get_sentiment_label
)
from charts.visualizations import (
    sentiment_pie_chart,
    sentiment_bar_chart,
    stock_price_chart,
    sentiment_gauge
)

# ── Load environment variables ──────────────────────────────────────
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# ── Page configuration ───────────────────────────────────────────────
st.set_page_config(
    page_title="Stock Sentiment Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Cache the AI model — loads ONCE, reuses across interactions ──────
@st.cache_resource(show_spinner="Loading FinBERT AI model...")
def get_finbert():
    return load_finbert()

# ── Header ────────────────────────────────────────────────────────────
st.title("📈 Stock Sentiment Dashboard")
st.markdown(
    "*Powered by **FinBERT AI** · Real-time financial news sentiment analysis*"
)
st.divider()

# ── Sidebar Controls ──────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    st.markdown("Enter a US stock ticker symbol to analyze its news sentiment.")

    ticker = st.text_input(
        "Stock Ticker",
        value="AAPL",
        max_chars=10,
        help="Examples: AAPL, MSFT, TSLA, GOOGL, AMZN"
    ).upper().strip()

    days = st.slider(
        "News Lookback Period (days)",
        min_value=1,
        max_value=30,
        value=7,
        help="How many days of news to analyze"
    )

    analyze_button = st.button(
        "🔍 Analyze Sentiment",
        use_container_width=True,
        type="primary"
    )

    st.divider()
    st.markdown("**About this app**")
    st.markdown(
        "This dashboard uses [FinBERT](https://huggingface.co/ProsusAI/finbert), "
        "a financial AI model, to analyze the sentiment of recent news headlines "
        "about any publicly traded stock."
    )

# ── Main Logic ────────────────────────────────────────────────────────
if analyze_button and ticker:

    # -- Fetch all data with a progress indicator
    progress_bar = st.progress(0, text="Starting analysis...")

    with st.spinner(f"Fetching stock data for **{ticker}**..."):
        info, hist = fetch_stock_info(ticker)
        progress_bar.progress(25, text="Stock data loaded...")

    with st.spinner("Fetching latest news headlines..."):
        articles = fetch_news(ticker, NEWS_API_KEY, days)
        progress_bar.progress(50, text=f"Found {len(articles)} articles...")

    with st.spinner("Running FinBERT sentiment analysis..."):
        finbert = get_finbert()
        headlines = [a["title"] for a in articles if a.get("title")]
        results = analyze_sentiment(headlines, finbert)
        overall_score = compute_overall_score(results)
        sentiment_label = get_sentiment_label(overall_score)
        progress_bar.progress(90, text="Building dashboard...")

    progress_bar.progress(100, text="Complete!")
    progress_bar.empty()

    # -- Validate ticker
    if not info or not info.get("shortName"):
        st.error(f"❌ Could not find stock data for **{ticker}**. Check the ticker symbol.")
        st.stop()

    # -- Metric Row
    st.subheader(f"📊 {info.get('shortName', ticker)} ({ticker})")
    col1, col2, col3, col4, col5 = st.columns(5)

    price = info.get("currentPrice") or info.get("regularMarketPrice", "N/A")
    change = info.get("regularMarketChangePercent", 0)
    market_cap = info.get("marketCap", 0)

    with col1:
        st.metric("Current Price", f"${price}")
    with col2:
        delta_color = "normal"
        st.metric("Day Change", f"{change:.2f}%" if change else "N/A")
    with col3:
        mc_str = f"${market_cap/1e12:.2f}T" if market_cap > 1e12 else f"${market_cap/1e9:.1f}B"
        st.metric("Market Cap", mc_str if market_cap else "N/A")
    with col4:
        st.metric("Articles Analyzed", len(results))
    with col5:
        st.metric("Overall Sentiment", sentiment_label, f"Score: {overall_score:+.3f}")

    st.divider()

    # -- Charts Row 1
    col_left, col_right = st.columns([1, 2])
    with col_left:
        if results:
            st.plotly_chart(sentiment_pie_chart(results), use_container_width=True)
            st.plotly_chart(sentiment_gauge(overall_score), use_container_width=True)
        else:
            st.warning("No headlines to display sentiment for.")

    with col_right:
        if hist is not None and not hist.empty:
            st.plotly_chart(stock_price_chart(hist), use_container_width=True)
        else:
            st.warning("Could not load stock price history.")

    # -- Bar chart of headlines
    if results:
        st.plotly_chart(sentiment_bar_chart(results), use_container_width=True)

    # -- News Table
    st.subheader("📰 Headlines & Sentiment Breakdown")
    if results:
        for article, result in zip(articles[:len(results)], results):
            emoji = {"positive": "🟢", "neutral": "⚪", "negative": "🔴"}.get(result["label"], "❓")
            label_color = {"positive": "green", "neutral": "gray", "negative": "red"}.get(result["label"])

            with st.expander(f"{emoji} {article['title'][:100]}{'...' if len(article['title']) > 100 else ''}"):
                col_a, col_b = st.columns([1, 3])
                with col_a:
                    st.markdown(f"**Sentiment:** :{label_color}[{result['label'].capitalize()}]")
                    st.markdown(f"**Confidence:** {result['score']:.1%}")
                    st.markdown(f"**Published:** {article['publishedAt'][:10]}")
                with col_b:
                    if article.get("description"):
                        st.markdown(f"*{article['description'][:200]}*")
                    st.markdown(f"[📖 Read full article]({article['url']})")
    else:
        st.info(f"No news headlines found for **{ticker}** in the last {days} days. Try a longer period or a different ticker.")

elif not analyze_button:
    # Welcome screen
    st.markdown("""
    ## Welcome! 👋

    This dashboard analyzes the **sentiment of recent financial news** for any publicly traded US stock using AI.

    **How to use:**
    1. Enter a stock ticker in the sidebar (e.g., `AAPL` for Apple)
    2. Choose how many days of news to analyze
    3. Click **Analyze Sentiment**

    **What you'll see:**
    - 📊 Company overview (price, market cap)
    - 📈 30-day stock price candlestick chart
    - 🥧 Sentiment distribution pie chart
    - 💯 Overall sentiment gauge
    - 📰 Individual headline sentiment breakdown

    ---
    *Built with FinBERT AI · yfinance · NewsAPI · Streamlit*
    """)