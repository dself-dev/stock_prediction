✅ indicators/README.md
# indicators/

This directory contains all **modular technical indicator classes** used by the
market-analysis and stock-prediction system.

Each file represents **one indicator**, follows a consistent interface, and adds
its calculated feature(s) directly to a pandas DataFrame.

---

## ✅ Design Principles

- **Single Responsibility** — one class per indicator  
- **Reusable** — consumed by ML models, FastAPI, CLI tools, or notebooks  
- **Consistent API** — every indicator exposes `.calculate()`  
- **Testable** — each indicator has a matching pytest file in `tests/`  
- **Non-destructive** — input DataFrame is copied before modification  
- **Extensible** — new indicators can be added without touching existing code

---

## 📦 Example Usage

```python
from indicators.rsi import RSI

df = RSI(df).calculate()

All classes follow the same pattern:
class IndicatorName:
    def __init__(self, df):
        self.df = df.copy()

    def calculate(self):
        # compute indicator
        return self.df


📁 Current Indicators


rsi.py — Relative Strength Index (momentum)


sma.py — Simple Moving Averages (trend)


ema.py — Exponential Moving Averages (trend velocity)


macd.py — MACD + Signal (momentum shift)


bollinger.py — Bollinger Bands (volatility squeeze)


atr.py — Average True Range (volatility strength)


mfi.py — Money Flow Index (volume-weighted pressure)


cci.py — Commodity Channel Index (reversal detection)



🎯 Long-Term Purpose (Product Vision)
This modular indicator engine will power:
✅ Automatic next-day stock price prediction
✅ A user-selectable indicator toolbox, where users can choose:


RSI only


RSI + MACD + SMA


volatility-focused set


custom combinations


✅ Personalized strategy creation
✅ Future AI-assisted recommendation engine
Meaning — the app will support two usage paths:


Full ML prediction mode
→ the system chooses & weighs indicators automatically


Manual / analyst mode
→ the user decides which indicators guide decisions


This flexibility is only possible because each indicator lives independently here.

🚀 Why This Folder Matters
Keeping indicators separated:
✅ prevents giant, tangled scripts
✅ makes ML feature engineering modular
✅ supports UI checkboxes & API selection
✅ improves maintainability & readability
✅ mirrors real fintech data-science architecture

🔧 Adding a New Indicator


Create <indicator_name>.py


Follow the class structure above


Add a matching test under tests/


Register it in services/indicator_engine.py if needed



This directory transforms traditional technical analysis into a scalable,
production-ready feature system that powers a full financial-intelligence platform.

---

### ✅ What to do next
Paste that into:


indicators/README.md

Commit → push → done ✅

---

If you want, I can now update:

✅ services/README.md with the same product vision  
✅ main/README.md to explain execution flow  
✅ tests/README.md to explain why pytest exists  
✅ architecture diagram showing indicator engine → ML → prediction

Just tell me 👍
