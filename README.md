# 📈 Stock Trading News Alert (Telegram Bot)

An automated stock market monitoring script built with Python. The tool tracks daily price fluctuations for a target equity (default: Tesla / `TSLA`) via the Alpha Vantage API. If the closing price shifts significantly (e.g., $\ge 5\%$) relative to the prior trading day, the script queries NewsAPI for relevant articles and dispatches formatted alerts directly to a personal Telegram chat via a custom Telegram Bot.

Part of the **100 Days of Code: Python Pro Bootcamp** (Day 36 Project), featuring architectural improvements including **local JSON caching** and a **Telegram Bot notification pipeline** (replacing SMS/Twilio).

---

## 🚀 Features

- **Automated Price Comparison:** Calculates mathematically accurate percentage change relative to the preceding trading day ($\frac{\text{New} - \text{Old}}{\text{Old}} \times 100$).
- **Visual Trend Indicators:** Automatically attaches directional emoji indicators (`🔺` for gains, `🔻` for drops).
- **API Rate-Limit Safeguard & Caching:** Includes a local JSON caching flag (`USE_MOCK_DATA`) to avoid exhausting strict Alpha Vantage daily rate limits during development and testing.
- **Top 3 News Delivery:** Slices and formats the top three relevant news articles (headline and summary) filtered by date and language.
- **Direct Telegram Alerts:** Utilizes Telegram's Bot API (`sendMessage`) with built-in dispatch pauses to prevent endpoint throttling.

---

## 🛠️ Tech Stack & APIs

- **Language:** Python 3.x
- **Libraries:** `requests`, `python-dotenv`
- **APIs:**
  - [Alpha Vantage API](https://www.alphavantage.co/) (Stock market time series)
  - [NewsAPI](https://newsapi.org/) (Market news headlines)
  - [Telegram Bot API](https://core.telegram.org/bots/api) (Alert delivery)

---

## 📂 Project Structure

```text
├── main.py              # Main execution pipeline (data fetch, math, news query, Telegram dispatch)
├── data.json            # Local cached stock response (generated on first API fetch)
├── .env.example         # Template for environment credentials
├── .gitignore           # Git ignore configuration (protects keys and secrets)
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## ⚙️ Setup & Installation
1. Clone the Repository
```commandline
git clone git@github.com:kama13a/StockTradingNewsAlert.git
cd StockTradingNewsAlert
```
2. Set Up a Virtual Environment
```commandline
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```
3. Install Dependencies
```commandline
pip install -r requirements.txt
```

## 🔑 Environment Variables
Create a .env file in the root directory:
```text
ALPHA_API_KEY=your_alpha_vantage_api_key
NEWS_API_KEY=your_news_api_key
TELEGRAM_TOKEN=your_telegram_bot_token_from_botfather
CHAT_ID=your_numerical_telegram_chat_id
```

## 🚦 How to Run
1. Test with Cached Data:
By default, USE_MOCK_DATA = True reads from data.json without consuming external API credits:
```commandline
python main.py
```

2. Run Live:
Set USE_MOCK_DATA = False inside main.py to fetch fresh market data directly from Alpha Vantage.

## 📬 Sample Telegram Alert
```text
TSLA: 🔺2.05%
Headline: Tesla Stocks Jump 3.2% as China Sales Extend 11-Month Rebound
Brief: Tesla recorded September sales of 95,366 Shanghai-built Model 3 and Model Y vehicles, while shares rose approximately 3.2% to $386.93...
```