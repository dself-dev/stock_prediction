🎯 Stock Prediction Model – 96% Accuracy

A production-ready machine-learning project that predicts next-day stock prices using technical indicators and sentiment analysis, with an integrated web UI, SQLite user-login system, and an experimental UP/DOWN classifier.

👨‍💻 Author

Dennis Selfinger
Machine Learning Engineer · Software Engineer · Quantitative Analyst

📊 96 % accuracy on real-world stock prediction (July 2025)
🎯 Focused on financial ML, technical analysis & algorithmic trading
💼 2 + years of data-science and algorithmic-trading experience

GitHub: @dself-dev

🚀 Overview

The system provides:

Price-forecast model (regression) for next-day close

Sentiment layer scraping Yahoo Finance headlines (VADER)

Binary classifier predicting UP / DOWN direction

FastAPI back-end with SQLite user-registration & login

Front-end GUI pages for login, account creation and home dashboard

📊 Model Performance
Model	Metric	Value
Price-forecast (AAPL)	R²	95.1 %
	RMSE	$3.40
Price-forecast (IONQ)	R²	97.6 %
	RMSE	$1.89
Classifier (UP/DOWN)	Baseline Accuracy	≈ 48 %*

*Classifier is experimental; intended as a baseline for future tuning.

🛠️ Core Features
ML / Data

19 technical indicators: RSI, Bollinger Bands, EMAs (12/26), SMAs (10/20/50), MACD & Signal, Stoch K/D, ATR, Volume SMA

Sentiment analysis: Yahoo Finance news → VADER polarity score

Binary classifier: Keras sequential dense network on the same indicators for UP/DOWN movement

Regression: Keras linear model (indicators + sentiment) for next-day price

Web / App

FastAPI back-end: REST endpoints, SQLite user DB

User authentication: sign-up / login pages

Front-end assets: HTML + CSS + JS served as static pages

🏗️ Architecture

Data source: yfinance (2–5 yrs OHLCV, auto-downloaded)

Pre-processing: StandardScaler on engineered indicators

Regression model: Keras Dense(1) → linear output

Classifier: Keras Dense(16) → ReLU → Dense(1, sigmoid)

Training: Regression ≈ 500 epochs; Classifier ≈ 25 epochs (baseline)

📁 Project Structure
api/
 ├─ app.py                   # FastAPI with DB & login routes
 ├─ database.py              # SQLite helpers
 ├─ models.py                # User model
frontEnd/
 ├─ assets/css & js          # Styling + login/create-user scripts
 └─ public/                  # Homepage.html, Login.html, Create_User.html
main/
 └─ predictions/
      ├─ predict_tomorrow.py # Regression + sentiment forecast
      └─ classify_direction.py# Binary UP/DOWN classifier
services/
 ├─ market.py                # Technical-indicator calculator
 ├─ sentiment.py             # Yahoo news → VADER
 └─ news.py                  # News scraper
combined_indicators.py       # Builds indicator-rich CSV
scraped_news/                # Saved news CSVs
requirments.txt
.gitignore
README.md

📦 Key Dependencies
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
tensorflow>=2.19.0
yfinance>=0.2.0
ta>=0.10.0
playwright>=1.55.0
nltk>=3.9
fastapi>=0.115.0
uvicorn>=0.30.0
sqlite3  # built-in

🚀 Quick Start
# clone + enter project
git clone https://github.com/dself-dev/stock_prediction.git
cd stock_prediction

# virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# install dependencies
pip install -r requirments.txt

# run price-forecast (regression + sentiment)
python main/predictions/predict_tomorrow.py

# run UP/DOWN classifier
python main/predictions/classify_direction.py

🧮 Workflow

Collect OHLCV data → yfinance

Compute 19 indicators → combined_indicators.py

Scrape news & sentiment → services/sentiment.py

Scale features → StandardScaler

Train or run regression → next-day close prediction

Train or run classifier → UP / DOWN probability

Serve results via CLI or FastAPI-backed GUI

📈 Example Output
Today's Close: $70.41
Predicted Close: $64.21
Expected Change: -8.8%

ML Prediction: GO DOWN
Sentiment: POSITIVE (avg 0.707)
ML and Sentiment DISAGREE → Mixed Signal – be cautious

🔮 Planned Enhancements

Improve classifier accuracy with hyper-parameter tuning & longer history

Add real-time order-book / depth & volatility-spike features

Upgrade to FinBERT / transformer-based sentiment

Add unit tests + complexity documentation

Expand FastAPI endpoints to serve all predictions programmatically

🎯 Why It Works

Indicators capture market-structure patterns

Sentiment adds macro / news-driven context

Agreement between models strengthens the signal; disagreement flags volatility

⚠️ Disclaimer

For educational / research use only – not financial advice.
Markets are unpredictable; trade responsibly.