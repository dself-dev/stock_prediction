# main/predictions/regression_pipeline.py   ← create this file

# main/predictions/regression_pipeline.py  ← DELETE EVERYTHING ELSE. THIS WORKS.
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib
from pathlib import Path

from indicators.rsi import RSI
from indicators.ema import EMA
from indicators.macd import MACD
from indicators.bollinger import BollingerBands
from indicators.atr import ATR
from indicators.cci import CCI
from indicators.mfi import MFI


class TomorrowPriceRegressor:
    def __init__(self):
        self.model = Pipeline([
            ('scaler', StandardScaler()),
            ('ridge', Ridge(alpha=1.0))
        ])
        self.fitted = False

    def _build_features(self, df: pd.DataFrame) -> pd.DataFrame:
        # Fix index and make sure it's a proper DataFrame
        df = df.copy()
        if isinstance(df.columns, pd.MultiIndex):
            df = df['Close'].copy()
            df.name = 'Close'

        close = df['Close'] if 'Close' in df.columns else df
        high = df['High']
        low = df['Low']
        volume = df['Volume']

        f = pd.DataFrame(index=df.index)

        # YOUR exact way — no bullshit
        close_df = pd.DataFrame({'Close': close}, index=df.index)
        ohlc_df = df[['Open', 'High', 'Low', 'Close']].copy()
        ohlcv_df = df[['High', 'Low', 'Close', 'Volume']].copy()

        f['rsi_14'] = RSI(close_df).calculate()['rsi']
        f['ema_12'] = EMA(close_df).calculate()['ema']
        f['ema_26'] = EMA(close_df).calculate()['ema']
        f['close_ema12_ratio'] = close / f['ema_12']
        f['ema_ratio'] = f['ema_12'] / f['ema_26']

        macd_df = MACD(close_df).calculate()
        atr_df = ATR(ohlc_df).calculate()
        f['macd_hist_norm'] = macd_df['macd_hist'] / atr_df['atr']

        bb_df = BollingerBands(close_df).calculate()
        f['bb_position'] = (close - bb_df['lower_band']) / (bb_df['upper_band'] - bb_df['lower_band'] + 1e-8)

        f['atr_14'] = atr_df['atr']
        f['cci_20'] = CCI(ohlc_df).calculate()['cci']
        f['mfi_14'] = MFI(ohlcv_df).calculate()['mfi']

        f['target'] = close.shift(-1)

        return f.dropna()

    def train(self, ticker: str = "AAPL", years: int = 5):
        end = datetime.today()
        start = end - timedelta(days=years * 365 + 200)
        raw = yf.download(ticker, start=start, end=end, progress=False)
        df = raw.copy()

        if df.empty:
            raise ValueError(f"No data for {ticker}")

        Xy = self._build_features(df)
        X = Xy.drop('target', axis=1)
        y = Xy['target']

        self.model.fit(X, y)
        self.fitted = True

        Path("models").mkdir(exist_ok=True)
        joblib.dump(self, Path("models") / f"{ticker.upper()}_ridge.pkl")
        print(f"Trained {ticker.upper()} — R²: {self.model.score(X, y):.4f}")

    def predict_tomorrow(self, ticker: str):
        if not self.fitted:
            self.train(ticker)
        df = yf.download(ticker, period="60d", progress=False)
        Xy = self._build_features(df)
        latest = Xy.drop('target', axis=1).iloc[-1:]
        pred = float(self.model.predict(latest)[0])
        current = float(df['Close'].iloc[-1])
        return {
            "ticker": ticker.upper(),
            "current_price": round(current, 2),
            "predicted_tomorrow": round(pred, 2),
            "change_pct": round((pred/current-1)*100, 2),
            "direction": "UP" if pred > current else "DOWN"
        }