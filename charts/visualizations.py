import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Color palette
COLORS = {
    "positive": "#2ecc71",
    "neutral":  "#95a5a6",
    "negative": "#e74c3c",
    "background": "rgba(0,0,0,0)",
    "text": "#2c3e50"
}

def sentiment_pie_chart(results):
    """Pie chart showing distribution of positive/neutral/negative."""
    if not results:
        return go.Figure()

    labels = [r["label"] for r in results]
    counts = pd.Series(labels).value_counts().reset_index()
    counts.columns = ["label", "count"]

    color_seq = [COLORS.get(l, "#888") for l in counts["label"]]

    fig = go.Figure(data=[go.Pie(
        labels=counts["label"].str.capitalize(),
        values=counts["count"],
        hole=0.4,
        marker_colors=color_seq,
        textfont_size=14
    )])

    fig.update_layout(
        title=dict(text="Sentiment Distribution", font=dict(size=16)),
        paper_bgcolor=COLORS["background"],
        showlegend=True,
        margin=dict(t=60, b=20, l=20, r=20)
    )
    return fig


def sentiment_bar_chart(results):
    """Horizontal bar chart: each headline colored by sentiment."""
    if not results:
        return go.Figure()

    df = pd.DataFrame(results)
    df["color"] = df["label"].map(COLORS)
    df["short_text"] = df["text"].apply(
        lambda t: t[:60] + "..." if len(t) > 60 else t
    )
    # Signed score for display
    sign_map = {"positive": 1, "neutral": 0, "negative": -1}
    df["signed_score"] = df.apply(
        lambda row: round(sign_map.get(row["label"], 0) * row["score"], 3), axis=1
    )
    df = df.sort_values("signed_score", ascending=True)

    fig = go.Figure(go.Bar(
        x=df["signed_score"],
        y=df["short_text"],
        orientation="h",
        marker_color=df["color"],
        text=df["label"].str.capitalize(),
        textposition="outside"
    ))

    fig.update_layout(
        title=dict(text="Headline Sentiment Scores", font=dict(size=16)),
        xaxis=dict(title="Sentiment Score (-1 to +1)", range=[-1.1, 1.1]),
        yaxis=dict(title=""),
        height=max(400, len(results) * 35),
        paper_bgcolor=COLORS["background"],
        margin=dict(t=60, b=40, l=20, r=40)
    )
    return fig


def stock_price_chart(hist):
    """Candlestick chart of stock price history."""
    if hist is None or hist.empty:
        return go.Figure()

    fig = go.Figure(data=[go.Candlestick(
        x=hist.index,
        open=hist["Open"],
        high=hist["High"],
        low=hist["Low"],
        close=hist["Close"],
        increasing_line_color=COLORS["positive"],
        decreasing_line_color=COLORS["negative"]
    )])

    fig.update_layout(
        title=dict(text="Stock Price — Last 30 Days", font=dict(size=16)),
        xaxis_rangeslider_visible=False,
        paper_bgcolor=COLORS["background"],
        margin=dict(t=60, b=40, l=40, r=40)
    )
    return fig


def sentiment_gauge(overall_score):
    """Gauge chart showing overall sentiment score."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=overall_score,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "Overall Sentiment", "font": {"size": 16}},
        delta={"reference": 0},
        number={"font": {"size": 28}},
        gauge={
            "axis": {"range": [-1, 1], "tickwidth": 1},
            "bar": {"color": "#3498db"},
            "steps": [
                {"range": [-1, -0.15], "color": "#fadbd8"},
                {"range": [-0.15, 0.15], "color": "#f8f9fa"},
                {"range": [0.15, 1], "color": "#d5f5e3"},
            ],
            "threshold": {
                "line": {"color": "black", "width": 4},
                "thickness": 0.75,
                "value": overall_score
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor=COLORS["background"],
        height=250,
        margin=dict(t=60, b=20, l=30, r=30)
    )
    return fig