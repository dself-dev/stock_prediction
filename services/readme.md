👨‍💻 Author

Dennis Selfinger
Machine Learning Engineer · Software Engineer · Quantitative Systems 
Email: dselfinger.dev@gmail.com (for project inquiries or collaboration, job/ resume info)

GitHub: @dself-dev
Docker Hub: https://hub.docker.com/r/dennis2026/stock-prediction-app

Primary interests:

 Software engineering, Back End, Data, Data Modeling, Dealing with all types of Data of I never get bored of

Financial machine learning

Time-series modeling

Backend API design

Scalable data pipelines

📈 Stock Prediction & Market Intelligence Platform

FastAPI · Machine Learning · Technical Indicators · Modular Architecture

A full-stack market analysis platform that combines technical indicators, machine-learning price prediction, and a web-based user interface with authentication.
Designed with clean separation of concerns, extensibility, and production deployment in mind. As this is my first major project that I've completed independently, I wanted to explain why I emphasized "clean separation of concerns" in the design—it might otherwise sound like generic AI-generated text. When I built this, I didn't even know there was a formal term like SoC (Separation of Concerns); I just implemented it intuitively because it made sense to keep the code organized, easier to maintain and debug, and more scalable in the long run. It also struck me that this approach would help any potential collaborator quickly grasp what's happening, as each component handles one specific task without overlapping responsibilities (meaning no duplication of effort or files performing similar jobs). For example, I split everything into dedicated modules—like keeping data fetching in one folder, indicators in another, and the ML models isolated—so it's simpler for me (or anyone else) to fix, expand, or tweak parts without disrupting the entire system. Plus, it's designed to grow and deploy smoothly without major headaches. I'm adding this note to the README to highlight how much I've learned through this process: not just coding, but also how to structure projects thoughtfully, ensure maintainability, and plan for future enhancements and production readiness.(I hope this makes sense and is not to much)

⚠️ Educational & research use only. Not financial advice.

🚀 Project Overview

This project provides an end-to-end pipeline for predicting next-day stock prices (and crypto) using historical market data and engineered technical features.

Current capabilities:

📊 Next-day price regression with custom date ranges
🧮 Modular technical indicator engine (9 indicators)
🧠 Neural-network regression model (linear + nonlinear ensemble)
🔮 Direction classification with confidence scoring
🌐 FastAPI backend with REST endpoints
🖥️ Browser-based frontend (served directly from the API)
🔐 User registration & login (SQLAlchemy + Pydantic)
🧱 Clean, testable architecture with Docker support

Recent updates:
✅ 🐳 Dockerized deployment (with .dockerignore)
✅ Full test suite for data pipeline and indicators

🧠 System Architecture (Runtime Flow)
User (Browser)
  ↓
HTML / JavaScript Frontend
  ↓
FastAPI (/predict)
  ↓
MarketDataService
  ├─ DataFetcher (yfinance with custom dates)
  ├─ DataCleaner
  ├─ FeatureBuilder
  ↓
TomorrowPredictor (linear + nonlinear)
  ├─ Train
  ├─ Predict & Average
  ↓
DirectionClassifier (binary probability)
  ├─ Train
  ├─ Predict Confidence
  ↓
JSON Response
  ↓
Frontend DOM Update

FastAPI serves both the API and the frontend. JavaScript handles the form and dynamically updates the prediction card.

📊 Machine Learning Pipeline
Data Flow
Fetch OHLCV (custom dates) → Clean Data → Build Indicators → Scale Features → Train Models → Predict Next Close & Direction

Current Models

Price Prediction (TomorrowPredictor in main/predictions/predict_tomorrow.py):
- Linear regression (simple Dense layer)
- Nonlinear MLP (64 → 32 ReLU layers)
- Ensemble: Average of linear and nonlinear outputs
- Uses early stopping and deterministic seeds

Features used (from FeatureBuilder):
- RSI_14
- Bollinger_Upper / Middle / Lower
- Plus SMA, EMA, MACD, ATR, MFI, CCI, Stochastic (for the classifier)

Direction Confidence (classify_direction.py):
- Binary neural network (ReLU hidden layers + sigmoid)
- Predicts UP/DOWN probability and adds confidence % to the JSON response

📈 Technical Indicator Engine

Located in: indicators/

Each indicator lives in its own file, has a .calculate() method, and returns the full DataFrame (chainable).

Implemented Indicators
Indicator          | Purpose
-------------------|--------------------------------
RSI (14)           | Momentum / overbought-oversold
SMA                | Trend smoothing
EMA                | Fast trend tracking
MACD               | Trend shifts
Bollinger Bands    | Volatility
ATR                | Volatility strength
MFI                | Volume-weighted momentum
CCI                | Statistical deviation
Stochastic         | Oscillator for momentum

This modular design makes it super easy to add more later (OBV, ADX, VWAP, etc.).

🧱 Backend (FastAPI)
Core Endpoints
POST /predict      → price + direction prediction
POST /register     → user creation (with country/state)
POST /login        → authentication
GET /health        → service health check

Backend also serves the static frontend and includes SQLAlchemy database setup.

🔐 Authentication
- User registration & login forms
- Backend credential verification (hashed passwords)
- Ready for JWT in production (demo mode leaves /predict open so anyone can test it right away)

🖥️ Frontend
- Vanilla HTML, CSS, JavaScript
- Served directly by FastAPI (frontEnd/public + assets)
- Async fetch calls
- Nice prediction result card with color coding, loading spinner, and close button

📁 Project Structure
.
├── app.py                      # FastAPI entry point (mounts frontend + all routes)
├── frontEnd/
│   ├── public/                 # index.html, login.html, create_new_user.html
│   └── assets/                 # CSS + JS (homepage.css, index.js, login_script.js, etc.)
├── services/
│   ├── market.py               # MarketDataService orchestrator
│   ├── data_fetcher.py
│   ├── data_cleaner.py
│   ├── indicator_engine.py
│   ├── news.py                 # (planned)
│   └── sentiment.py            # (planned)
├── indicators/
│   ├── atr.py
│   ├── bollinger.py
│   ├── cci.py
│   ├── ema.py
│   ├── macd.py
│   ├── mfi.py
│   ├── rsi.py
│   ├── sma.py
│   └── stochastic.py
├── main/predictions/
│   ├── predict_tomorrow.py     # TomorrowPredictor (linear + nonlinear)
│   └── classify_direction.py
├── database.py                 # SQLAlchemy + User model
├── models.py                   # Pydantic UserCreate
├── tests/                      # Full pytest coverage
├── .dockerignore
├── Dockerfile                  # (Dockerized)
├── requirements.txt
└── README.md

🧪 Testing
I wrote unit tests for almost everything:
- DataCleaner, DataFetcher
- Every single indicator
- FeatureBuilder
- TomorrowPredictor training/prediction

The architecture is built to be test-friendly.

🧠 Roadmap
Near-term
✅ Direction classifier with confidence
✅ Custom date ranges
Mid-term
📰 Market sentiment analysis
📊 Model persistence (save trained models)
Long-term
CNN → LSTM hybrids
Transformer time-series models
Multi-asset portfolio stuff

🚀 Getting Started
git clone https://github.com/dself-dev/stock_prediction.git
cd stock_prediction

python -m venv venv
.\venv\Scripts\activate     # Windows
# or source venv/bin/activate on Mac/Linux

pip install -r requirements.txt

uvicorn app:app --reload

Open your browser to http://127.0.0.1:8000 and try it out!

🐳 Docker Deployment
The project is fully Dockerized now.

docker build -t stock-prediction .
docker run -p 8000:8000 stock-prediction

Image is also on Docker Hub: https://hub.docker.com/r/dennis2026/stock-prediction-app

---

That’s it bro — it still sounds like **you** wrote it, but now it’s up-to-date, complete, and covers every file you showed me.  

Just replace your old README.md with this and push.  

If you want any tiny tweaks (make a section shorter, add something, etc.) just tell me and I’ll fix it instantly. You good? 🚀




<!-- # services/

This directory contains the application's **business logic layer** — reusable
services that perform core operations needed across the system.

These modules do not handle UI, ML model definition, or raw indicator math.
Instead, they orchestrate higher-level workflows that other components rely on.

---

## ✅ Purpose of This Folder

- Central place for shared application logic  
- Keeps prediction scripts small and readable  
- Allows FastAPI, CLI tools, and notebooks to reuse the same functionality  
- Enables clean separation between **data**, **logic**, and **presentation**

This mirrors real-world backend architecture patterns.

---

## 📦 Current Services

### `indicator_engine.py`
Runs multiple technical indicator classes in sequence.

Responsibilities:
- Accept a pandas DataFrame with OHLCV data
- Run selected indicator classes (RSI, SMA, MACD, etc.)
- Return a feature-rich DataFrame ready for ML or analysis
- Future support for user-selected indicator sets

This file is the “glue” that connects raw market data to indicators.

---

### `sentiment.py`
Applies VADER sentiment analysis to financial news.

Responsibilities:
- Load scraped headlines
- Score sentiment polarity
- Aggregate and classify sentiment

Used to combine market psychology with technical data.

---

### `news.py`
Retrieves news articles for a given ticker symbol.

Responsibilities:
- Scrape or request Yahoo Finance headlines
- Save structured results to CSV
- Sanitize text for sentiment scoring

This allows real-time narrative context for predictions.

---

## 🎯 Long-Term Product Vision

The services layer will support:

✅ Automatic **next-day price prediction**  
✅ A future **FastAPI backend** powering a web dashboard  
✅ User controls for:
- selecting indicators
- enabling sentiment
- choosing timeframes

✅ Modular expansion:
- real-time data streaming
- brokerage integrations
- portfolio monitoring
- alerts & notifications

By keeping services isolated, the system can evolve without breaking core logic.

---

## 🧩 Why This Layer Exists

- Prevents duplicated logic across scripts
- Makes testing and debugging easier
- Keeps indicator classes focused on math only
- Keeps prediction scripts focused on orchestration
- Prepares project for multi-user, production deployment

This is the “middle tier” of the application — scalable and reusable.

---

## ✅ Usage Example

```python
from services.indicator_engine import IndicatorEngine

df = IndicatorEngine(df).run()
The same call works in:

predict_tomorrow.py

Jupyter notebooks

future API routes

batch-processing jobs

🔧 Contributing Guidelines
When adding a new service:

Keep responsibilities small and focused

Write clear docstrings

Add tests if logic is complex

Never compute indicators here — use indicators/

This folder forms the operational backbone of the stock-prediction platform —
connecting raw market data, indicators, sentiment, and future ML services. -->