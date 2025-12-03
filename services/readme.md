# services/

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
connecting raw market data, indicators, sentiment, and future ML services.