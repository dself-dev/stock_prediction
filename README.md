👨‍💻 Author

Dennis Selfinger
Machine Learning Engineer · Software Engineer · Quantitative Systems 
Email: dselfinger.dev@gmail.com (for project inquiries or collaboration, job/ resume info)

GitHub: @dself-dev

Primary interests:

Data, Data Modeling, Dealing with all types of Data of I never get bored of

Financial machine learning

Time-series modeling

Backend API design

Scalable data pipelines


📈 Stock Prediction & Market Intelligence Platform

FastAPI · Machine Learning · Technical Indicators · Modular Architecture

A full-stack market analysis platform that combines technical indicators, machine-learning price prediction, and a web-based user interface with authentication.
Designed with clean separation of concerns, extensibility, and production deployment in mind. As this is my first major project that I've completed independently, I wanted to explain why I emphasized "clean separation of concerns" in the design—it might otherwise sound like generic AI-generated text. When I built this, I didn't even know there was a formal term like SoC (Separation of Concerns); I just implemented it intuitively because it made sense to keep the code organized, easier to maintain and debug, and more scalable in the long run. It also struck me that this approach would help any potential collaborator quickly grasp what's happening, as each component handles one specific task without overlapping responsibilities (meaning no duplication of effort or files performing similar jobs). For example, I split everything into dedicated modules—like keeping data fetching in one folder, indicators in another, and the ML models isolated—so it's simpler for me (or anyone else) to fix, expand, or tweak parts without disrupting the entire system. Plus, it's designed to grow and deploy smoothly without major headaches. I'm adding this note to the README to highlight how much I've learned through this process: not just coding, but also how to structure projects thoughtfully, ensure maintainability, and plan for future enhancements and production readiness.(I hope this makes sense and is not to much)

⚠️ Educational & research use only. Not financial advice.

👨‍💻 Author

Dennis Selfinger
Machine Learning Engineer · Software Engineer · Quantitative Systems 
Email: dselfinger.dev@gmail.com (for project inquiries or collaboration, job/ resume info)

GitHub: @dself-dev

Primary interests:

Data, Data Modeling, Dealing with all types of Data of I never get bored of

Financial machine learning

Time-series modeling

Backend API design

Scalable data pipelines

🚀 Project Overview

This project provides an end-to-end pipeline for predicting next-day stock prices using historical market data and engineered technical features.

Current capabilities:

📊 Next-day price regression with custom date ranges

🧮 Modular technical indicator engine

🧠 Neural-network regression model (linear + nonlinear ensemble)

🔮 Direction classification with confidence scoring

🌐 FastAPI backend

🖥️ Browser-based frontend

🔐 User registration & login

🧱 Clean, testable architecture

Planned extensions (in progress):

📰 Market sentiment analysis

📈 Advanced deep-learning models

Recent updates:

✅ 🐳 Dockerized deployment

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


FastAPI serves both the API and the frontend, while JavaScript dynamically injects prediction results into the UI.

📊 Machine Learning Pipeline
Data Flow
Fetch OHLCV (custom dates) → Clean Data → Build Indicators
→ Scale Features → Train Models → Predict Next Close & Direction

Current Models

Price Prediction (TomorrowPredictor):
- Linear regression (simple Dense layer)
- Nonlinear MLP (multi-layer ReLU network)
- Ensemble: Average of linear and nonlinear outputs for robustness

Features used:
- RSI (14)
- Bollinger Bands (Upper, Middle, Lower)
- Additional indicators (SMA, EMA, MACD, etc. for classifier)

Target: Next-day closing price (regression) + UP/DOWN direction (classification)

Training: Per request (research phase, with early stopping to prevent overfitting)

Why per-request training?
- The current system trains per request so users can submit arbitrary tickers and receive a symbol-specific prediction without requiring pretraining across the full market.
- This was a deliberate design choice for the research/demo phase given limited compute resources and the large universe of stocks and crypto assets.
- A planned production enhancement is model persistence with freshness checks, so recently requested symbols can reuse saved models while stale models are retrained when needed.

Direction Confidence (DirectionClassifier):
- Binary neural network (ReLU hidden layers, sigmoid output)
- Predicts probability of UP (close tomorrow >= today) or DOWN
- Adds confidence % to output (e.g., 62% UP)

This design keeps the models simple while validating the end-to-end ML system before adding complexity.

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
Stochastic	Oscillator for momentum

This modular design allows easy expansion (OBV, ADX, VWAP, etc.).

🧱 Backend (FastAPI)
Core Endpoints

POST /predict → price prediction with direction confidence

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
├── api/
│   └── app.py               # FastAPI entry point
├── frontEnd/
│   ├── public/              # HTML pages (index.html, login.html, create_new_user.html)
│   └── assets/              # CSS / JS (homepage.css, index.js, login_script.js, create_user_script.js)
├── services/
│   ├── market.py            # Data orchestration
│   ├── data_fetcher.py      # yfinance data retrieval
│   ├── indicator_engine.py  # Indicator application wrapper
│   ├── news.py              # News fetching (planned)
│   └── sentiment.py         # Sentiment analysis (planned)
├── indicators/              # Technical indicators
│   ├── atr.py
│   ├── bollinger.py
│   ├── cci.py
│   ├── ema.py
│   ├── macd.py
│   ├── mfi.py
│   ├── rsi.py
│   ├── sma.py
│   └── stochastic.py
├── main/
│   ├── fibonacci/           # Fibonacci tools (planned)
│   └── predictions/
│       └── classify_direction.py  # Direction classifier
│       └── predict_tomorrow.py    # Price predictor
├── tests/                   # Unit tests
│   ├── test_atr.py
│   ├── test_bollinger.py
│   ├── test_cci.py
│   ├── test_data_cleaner.py
│   ├── test_data_fetcher.py
│   ├── test_ema.py
│   ├── test_feature_build.py
│   ├── test_indicator_engine.py
│   ├── test_macd.py
│   ├── test_mfi.py
│   ├── test_rsi.py
│   ├── test_sma.py
│   └── test_tomorrow_predict.py
├── database.py              # SQLite user database
├── models.py                # Pydantic models for validation
├── requirements.txt
├── .gitignore
├── Dockerfile               # Docker configuration for containerized deployment
├── .dockerignore            # Excludes unnecessary files for Docker builds
└── README.md

🧪 Testing

Indicator-level unit tests

Validation of required columns

Defensive error handling in data pipeline

The architecture is intentionally test-friendly.

🧠 Roadmap
Near-term

✅ Direction classifier (UP / DOWN with confidence)

✅ Custom date ranges for data fetch

Mid-term

📰 Market sentiment analysis

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
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt

uvicorn api.app:app --reload


Open:

http://127.0.0.1:8000

🐳 Docker Deployment

The project is now Dockerized for easy, reproducible deployment.

Build and run:
```bash
docker build -t stock-prediction .
docker run -p 8000:8000 stock-prediction

For more details on the image, visit the [Docker Hub repository](https://hub.docker.com/r/dennis2026/stock-prediction-app).