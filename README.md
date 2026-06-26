# stock-sentiment-dashboard



\# 📈 Stock Sentiment Dashboard



An AI-powered financial news sentiment analyzer built with FinBERT and Streamlit.



\## 🔗 Live Demo

\[View Live App](https://stock-sentiment-dashboard-3puvj3cajmunuwhppubgcl.streamlit.app/)



\## 📸 Screenshots

!\[Dashboard](screenshots/dashboard.png)

!\[Charts](screenshots/charts.png)

!\[Headlines](screenshots/headlines.png)

!\[sentiments](sentiments/charts.png)




\## ✨ Features

\- Real-time stock data via yfinance

\- Live news headlines from NewsAPI

\- AI sentiment analysis using FinBERT (financial transformer model)

\- Interactive charts: pie chart, candlestick, bar chart, gauge

\- Supports US and Indian stocks (e.g. AAPL, RELIANCE.NS)



\## 🛠 Tech Stack

| Component | Technology |

|-----------|------------|

| Frontend | Streamlit |

| AI Model | FinBERT (HuggingFace) |

| Stock Data | yfinance |

| News Data | NewsAPI |

| Charts | Plotly |

| Hosting | Streamlit Community Cloud |



\## ⚙️ Local Setup

```bash

git clone https://github.com/AtulPandeyCode/stock-sentiment-dashboard

cd stock-sentiment-dashboard

python -m venv venv

source venv/bin/activate  # Windows: venv\\Scripts\\activate

pip install -r requirements.txt

\# Create .env file and add: NEWS\_API\_KEY=your\_key\_here

streamlit run app.py

```



\## 🏗 Architecture

User → Streamlit UI → yfinance + NewsAPI → FinBERT → Plotly Charts → Dashboard



\## 📄 License

MIT

