# stock-sentiment-dashboard



# 📈 Stock Sentiment Dashboard



An AI-powered financial news sentiment analyzer built with FinBERT and Streamlit.



## 🔗 Live Demo

[View Live App](https://stock-sentiment-dashboard-3puvj3cajmunuwhppubgcl.streamlit.app/)



## 📸 Screenshots

Dashboard
<img width="1845" height="977" alt="dashboard" src="https://github.com/user-attachments/assets/f9153fe2-fb0f-4a1f-9807-0e946b645b95" />
Charts
<img width="1436" height="755" alt="charts" src="https://github.com/user-attachments/assets/a1305c27-d723-46a4-99ec-58bc4aaefad6" />
Market Sentiments
<img width="1417" height="798" alt="sentiment" src="https://github.com/user-attachments/assets/c83cffe3-bcce-40cd-a382-0c3dff339f08" />
Actual Articles
<img width="1443" height="856" alt="headlines" src="https://github.com/user-attachments/assets/832a99ff-6a2c-4a89-b4d1-72a0d5892901" />


## ✨ Features

\- Real-time stock data via yfinance

\- Live news headlines from NewsAPI

\- AI sentiment analysis using FinBERT (financial transformer model)

\- Interactive charts: pie chart, candlestick, bar chart, gauge

\- Supports US and Indian stocks (e.g. AAPL, RELIANCE.NS)



## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| AI Model | FinBERT (HuggingFace) |
| Stock Data | yfinance |
| News Data | NewsAPI |
| Charts | Plotly |
| Hosting | Streamlit Community Cloud |


## ⚙️ Local Setup

```bash

git clone https://github.com/AtulPandeyCode/stock-sentiment-dashboard

cd stock-sentiment-dashboard

python -m venv venv

source venv/bin/activate  # Windows: venv\\Scripts\\activate

pip install -r requirements.txt

\# Create .env file and add: NEWS\_API\_KEY=your\_key\_here

streamlit run app.py

```



## 🏗 Architecture

User → Streamlit UI → yfinance + NewsAPI → FinBERT → Plotly Charts → Dashboard



\## 📄 License

MIT

