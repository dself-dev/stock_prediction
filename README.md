📈 Stock Prediction & Market Intelligence Platform

FastAPI · Machine Learning · Technical Indicators · Modular Architecture

A full-stack market analysis platform that combines technical indicators, machine-learning price prediction, and a web-based user interface with authentication.
Designed with clean separation of concerns, extensibility, and production deployment in mind.

⚠️ Educational & research use only. Not financial advice.

👨‍💻 Author

Dennis Selfinger
Machine Learning Engineer · Software Engineer · Quantitative Systems

GitHub: @dself-dev

Primary interests:

Financial machine learning

Time-series modeling

Backend API design

Scalable data pipelines

🚀 Project Overview

This project provides an end-to-end pipeline for predicting next-day stock prices using historical market data and engineered technical features.

Current capabilities:

📊 Next-day price regression

🧮 Modular technical indicator engine

🧠 Neural-network regression model

🌐 FastAPI backend

🖥️ Browser-based frontend

🔐 User registration & login

🧱 Clean, testable architecture

Planned extensions (in progress):

🔮 Direction classification (UP / DOWN)

📰 Market sentiment analysis

🐳 Dockerized deployment

📈 Advanced deep-learning models

🧠 System Architecture (Runtime Flow)
User (Browser)
  ↓
HTML / JavaScript Frontend
  ↓
FastAPI (/predict)
  ↓
MarketDataService
  ├─ DataFetcher (yfinance)
  ├─ DataCleaner
  ├─ FeatureBuilder
  ↓
TomorrowPredictor
  ├─ Train
  ├─ Predict
  ↓
JSON Response
  ↓
Frontend DOM Update


FastAPI serves both the API and the frontend, while JavaScript dynamically injects prediction results into the UI.

📊 Machine Learning Pipeline
Data Flow
Fetch OHLCV → Clean Data → Build Indicators
→ Scale Features → Train Model → Predict Next Close

Current Model

Type: Linear regression (TensorFlow / Keras)

Features used:

RSI (14)

Bollinger Upper / Middle / Lower

Target: Next-day closing price

Training: Per request (research phase)

This design keeps the model simple while validating the end-to-end ML system before adding complexity.

📈 Technical Indicator Engine

Located in:

indicators/


Each indicator:

Lives in its own file

Exposes a .calculate() method

Accepts and returns a DataFrame

Is chainable and ML-ready

Implemented Indicators
Indicator	Purpose
RSI (14)	Momentum / overbought-oversold
SMA	Trend smoothing
EMA	Fast trend tracking
MACD	Trend shifts
Bollinger Bands	Volatility
ATR	Volatility strength
MFI	Volume-weighted momentum
CCI	Statistical deviation

This modular design allows easy expansion (OBV, ADX, VWAP, etc.).

🧱 Backend (FastAPI)
Core Endpoints

POST /predict → price prediction

POST /register → user creation

POST /login → authentication

GET /health → service health check

Backend Responsibilities

Input validation

ML orchestration

JSON serialization

Authentication logic

Static frontend serving

🔐 Authentication

The platform includes:

User registration

Login flow

Client-side form validation

Backend credential verification

This provides a foundation for:

User-specific models

Prediction history

Role-based access (future)

🖥️ Frontend

Vanilla HTML, CSS, JavaScript

Served directly by FastAPI

Async API calls via fetch

Dynamic DOM rendering

Loading states & UI feedback

The frontend is intentionally simple to keep focus on backend + ML correctness.

📁 Project Structure
.
├── frontEnd/
│   ├── public/              # HTML pages
│   └── assets/              # CSS / JS
├── services/
│   ├── market.py            # Data orchestration
│   └── data_fetcher.py
├── indicators/              # Technical indicators
├── main/
│   └── predictions/
│       └── predict_tomorrow.py
├── tests/                   # Unit tests
├── requirements.txt
├── app.py                   # FastAPI entry point
└── README.md

🧪 Testing

Indicator-level unit tests

Validation of required columns

Defensive error handling in data pipeline

The architecture is intentionally test-friendly.

🧠 Roadmap
Near-term

✅ Direction classifier (UP / DOWN)

✅ Sentiment scoring (news + NLP)

✅ Feature selection experiments

Mid-term

🐳 Dockerized deployment

📊 Model persistence (no retrain per request)

🧵 Async background training

Long-term (Research)

CNN → LSTM hybrid models

Transformer-based time-series forecasting

Multi-asset portfolio modeling

🚀 Getting Started
git clone https://github.com/dself-dev/stock_prediction.git
cd stock_prediction

python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate
pip install -r requirements.txt

uvicorn app:app --reload


Open:

http://127.0.0.1:8000

🎯 Why This Project Matters

Demonstrates end-to-end ML system design

Shows clean separation of data, features, models, and API

Balances research flexibility with production discipline

Easy to extend, test, and deploy

This is not a notebook experiment — I tried to make it as close to a  real system as I can at this point in my journey. Thank you for taking the time to look at this.

⚠️ Disclaimer

This project is for educational and research purposes only.
It is not financial advice.
Markets are volatile and unpredictable.