📈 Stock Prediction & Market Analysis Engine
Machine Learning · Technical Indicators · Sentiment AI · FastAPI App










A production-grade machine-learning engine that predicts next-day stock prices, UP/DOWN movement, sentiment flow, and market-structure levels.

This repo now includes:

🔍 A full technical indicator engine (each indicator = its own class)

🧪 Pytest suite with 100% passing tests

🧠 Machine learning models (regression + classifier)

📰 Sentiment scoring from Yahoo Finance

🔢 Fibonacci retracement engine

⚙️ FastAPI app with user auth (SQLite)

🚀 A deep-learning roadmap (CNN → LSTM → Hybrid → Transformer)

⚠️ All results are for research and educational use only. Markets can change quickly.

👨‍💻 Author

Dennis Selfinger
Machine Learning Engineer • Software Engineer • Quantitative Analyst

GitHub: @dself-dev

Focused on:

Financial ML

Algorithmic trading

AI engineering

Distributed backend systems

🚀 Overview

This system provides:

📈 Next-day close prediction (regression model)

🔮 UP/DOWN classifier

🧠 Sentiment layer from Yahoo Finance → VADER

⚙️ Modular indicator engine (clean, testable, scalable)

🧮 Fibonacci levels for market structure

🧵 FastAPI authentication (login, signup)

🌐 REST endpoints for predictions, indicators, and sentiment

📊 Model Performance (Sept 2025)
Model	Metric	Value
AAPL Regression	R²	95.1 %
	RMSE	$3.40
IONQ Regression	R²	97.6 %
	RMSE	$1.89
Direction Classifier	Accuracy	≈ 48 % (baseline)
🔧 Architecture Diagram
User → Frontend → FastAPI → ML Engine → Predictions
                              │
                              ├─ Indicator Engine (Classes)
                              ├─ Sentiment Engine (News → VADER)
                              ├─ Fibonacci Engine (Market Structure)
                              └─ Deep Learning Models (Future)

📈 Technical Indicators Engine (Modular + Tested)

Located in:

indicators/


Each indicator:

Lives in its own file

Has a .calculate() method

Includes input validation

Fully unit-tested

ML-ready

User-selectable (future upgrade)

✔ Implemented Indicators
Indicator	Purpose
RSI (14)	Overbought/oversold
SMA (10/20/50)	Slow trend direction
EMA (12/26)	Fast trend direction
MACD & Signal	Trend shifts
Bollinger Bands	Volatility squeeze
ATR (14)	Volatility strength
MFI (14)	Volume-weighted money flow
CCI (20)	Statistical deviation & reversals
Indicator Engine Diagram
Indicators/
│
├── rsi.py
├── sma.py
├── ema.py
├── macd.py
├── bollinger.py
├── atr.py
├── mfi.py
├── cci.py
└── __init__.py

🧪 Test Suite (pytest)

All indicators have their own dedicated tests under:

tests/


Run the full suite:

pytest


✔ All tests passing
✔ Validates shape, columns, calculations, and exceptions

🔢 Fibonacci Retracement Engine

Under:

main/fiboncacci/fib.py


Features:

Auto-detect swing high & swing low

Calculates 23.6%, 38.2%, 50%, 61.8%, 78.6% levels

Lays foundation for:

Take-profit suggestions

Pullback zones

ML integration

📁 Project Structure
Market_data/
│
├── api/                     # FastAPI backend
├── frontEnd/               # Login + UI pages
├── indicators/             # Modular indicator engine
├── tests/                  # Pytest suite
├── main/
│   ├── predictions/        # Regression + classifier
│   └── fiboncacci/         # Fibonacci calculations
├── services/               # Sentiment, scraping, utilities
├── scraped_news/
├── combined_indicators.py
├── requirements.txt
└── README.md

🧮 Workflow
Download OHLCV → Compute Indicators → Scrape News
→ Sentiment → Scale Features → Predict Price/Direction
→ Fibonacci Levels → Serve Via FastAPI + UI

🔧 Migration Notice: Indicator Engine Modernization

The project previously calculated every indicator inside:

predict_tomorrow.py


This was replaced with a modular class-based architecture:

Each indicator has its own file

Each has its own .calculate() method

100% test coverage

Easy expansion (OBV, ADX, VWAP, Keltner...)

Prepares for CNN/LSTM/Transformer models

Enables user-selectable indicators (future)

🧠 Deep Learning Roadmap (Major Upgrade)

This represents the next evolution of the ML system:

Raw OHLCV + Indicators + Sentiment
                 │
──────────────────────────────────────────────
Step 1 — 🧩 CNN (Convolutional Neural Net)
• Learns short-term local patterns
• Detects volatility clusters
──────────────────────────────────────────────
                 ▼
Step 2 — 🔁 LSTM (Long Short-Term Memory)
• Learns sequential price behavior
• Captures trend continuation & reversals
──────────────────────────────────────────────
                 ▼
Step 3 — 🧬 Hybrid CNN → LSTM
• CNN extracts features → LSTM interprets them
• Industry-standard for forecasting
──────────────────────────────────────────────
                 ▼
Step 4 — 🤖 Transformer Model
• Same architecture as GPT models
• Long-range dependency learning
• Future: TFT, Informer, Autoformer

Deep Learning Summary Table
Stage	Model	Purpose	Status
Step 1	CNN	Local pattern extraction	Planned
Step 2	LSTM	Sequence learning	Planned
Step 3	CNN → LSTM	Hybrid forecasting	Planned
Step 4	Transformer	Advanced temporal modeling	Future
🖥️ Optional GIF Demo (placeholder)

You can record a GIF of your prediction script or UI and drop it into:

docs/demo.gif


Then embed it:

![Demo](docs/demo.gif)

🚀 Quick Start
git clone https://github.com/dself-dev/stock_prediction.git
cd stock_prediction

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

python main/predictions/predict_tomorrow.py
python main/fiboncacci/fib.py

🎯 Why This Project Works

Indicators capture market structure

Sentiment captures external catalysts

Fibonacci captures trend exhaustion

ML captures non-linear patterns

Modular architecture makes everything scalable and testable

Deep-learning roadmap future-proofs the system

⚠️ Disclaimer

This project is for research and educational use only.
Not financial advice.
Markets are volatile — trade safely.