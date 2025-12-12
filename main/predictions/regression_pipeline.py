"""
End-to-end regression pipeline for stock price forecasting.

This module downloads OHLCV data, normalizes column names (handles MultiIndex),
builds a full technical-indicator feature set (using FeatureBuilder),
trains a Ridge regression model to predict the next day's closing price,
and saves/loads all trained artifacts. It also provides a public API
to generate a real-time "predict tomorrow" forecast for any ticker. May ust 86 this file since i am building seperte file for calling cleaning indicators and then training and predictin.
"""

# main/predictions/regression_pipeline.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List

import joblib
import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler

from indicators.feature_builder import FeatureBuilder


MODELS_DIR = Path("models")


@dataclass
class TrainedArtifacts:
    model: Ridge
    scaler_X: StandardScaler
    feature_names: List[str]


class TomorrowPriceRegressor:
    """
    Unified regression pipeline:
      - pulls OHLCV with yfinance
      - normalizes lowercase and MultiIndex column names
      - runs FeatureBuilder to add ALL indicators
      - trains a Ridge regression model to predict tomorrow's Close
      - saves/loads model + scaler
      - predicts tomorrow for a given ticker
    """

    def __init__(self) -> None:
        self.artifacts: TrainedArtifacts | None = None
        MODELS_DIR.mkdir(exist_ok=True)

    # ----------------------------------------------------------
    # Column normalization (fixes lowercase + MultiIndex issues)
    # ----------------------------------------------------------
    def _normalize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Ensures column names match indicator expectations.
        Handles MultiIndex output from yfinance.
        """
        # If yfinance returns MultiIndex, flatten it
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [
                "_".join(str(c) for c in col if c)  # remove empty second levels
                for col in df.columns
            ]

        # Convert all column names to strings and capitalize
        df.columns = [str(col).capitalize() for col in df.columns]

        return df

    # ----------------------------------------------------------
    # Data downloaders
    # ----------------------------------------------------------
    def _download_history(self, ticker: str, years: int = 3) -> pd.DataFrame:
        """Download OHLCV for training."""
        end = datetime.today()
        start = end - timedelta(days=years * 365 + 10)

        df = yf.download(ticker, start=start, end=end, progress=False)
        if df.empty:
            raise ValueError(f"No data returned for ticker: {ticker}")

        df = df.reset_index()
        df = self._normalize_columns(df)
        return df

    def _download_recent(self, ticker: str, days: int = 90) -> pd.DataFrame:
        """Download recent data for prediction."""
        df = yf.download(ticker, period=f"{days}d", progress=False)
        if df.empty:
            raise ValueError(f"No recent data for ticker: {ticker}")

        df = df.reset_index()
        df = self._normalize_columns(df)
        return df

    # ----------------------------------------------------------
    # Feature builder wrapper
    # ----------------------------------------------------------
    def _build_features(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
        """Run FeatureBuilder and construct X/y matrices."""

        fb = FeatureBuilder(df)
        full_df = fb.build().copy()
        print("DEBUG DF COLUMNS:", df.columns.tolist())


        # Remove non-numeric columns (e.g., Date)
        non_numeric = [
            col for col in full_df.columns
            if not np.issubdtype(full_df[col].dtype, np.number)
        ]
        full_df = full_df.drop(columns=non_numeric, errors="ignore")

        if "Close" not in full_df.columns:
            raise ValueError("FeatureBuilder output must contain 'Close' column.")

        full_df["Target"] = full_df["Close"].shift(-1)

        # Remove NaNs introduced by indicator windows
        full_df = full_df.dropna().reset_index(drop=True)

        y = full_df["Target"]
        X = full_df.drop(columns=["Target"])

        return X, y

    # ----------------------------------------------------------
    # Model save/load
    # ----------------------------------------------------------
    def _model_path(self, ticker: str) -> Path:
        return MODELS_DIR / f"{ticker.upper()}_ridge.pkl"

    def _save_artifacts(self, ticker: str, artifacts: TrainedArtifacts) -> None:
        joblib.dump(
            {
                "model": artifacts.model,
                "scaler_X": artifacts.scaler_X,
                "feature_names": artifacts.feature_names,
            },
            self._model_path(ticker),
        )

    def _load_artifacts(self, ticker: str) -> TrainedArtifacts:
        path = self._model_path(ticker)
        if not path.exists():
            raise FileNotFoundError(f"No trained model found for {ticker}: {path}")

        payload = joblib.load(path)
        return TrainedArtifacts(
            model=payload["model"],
            scaler_X=payload["scaler_X"],
            feature_names=payload["feature_names"],
        )

    # ----------------------------------------------------------
    # Public API — Training
    # ----------------------------------------------------------
    def train(self, ticker: str, years: int = 3) -> Dict[str, Any]:
        """Train Ridge regression using historical data + indicators."""
        ticker = ticker.upper()

        raw = self._download_history(ticker, years=years)
        X, y = self._build_features(raw)

        scaler_X = StandardScaler()
        X_scaled = scaler_X.fit_transform(X)

        model = Ridge(alpha=1.0)
        model.fit(X_scaled, y)

        artifacts = TrainedArtifacts(
            model=model,
            scaler_X=scaler_X,
            feature_names=list(X.columns),
        )

        self.artifacts = artifacts
        self._save_artifacts(ticker, artifacts)

        r2 = float(model.score(X_scaled, y))

        return {
            "ticker": ticker,
            "samples": int(len(y)),
            "features": len(artifacts.feature_names),
            "r2_train": round(r2, 4),
            "model_path": str(self._model_path(ticker)),
        }

    # ----------------------------------------------------------
    # Public API — Prediction
    # ----------------------------------------------------------
    def predict_tomorrow(self, ticker: str, years_if_not_trained: int = 3) -> Dict[str, Any]:
        """Predict tomorrow's closing price for the specified ticker."""
        ticker = ticker.upper()
        model_path = self._model_path(ticker)

        if model_path.exists():
            self.artifacts = self._load_artifacts(ticker)
        else:
            self.train(ticker, years=years_if_not_trained)

        assert self.artifacts is not None

        model = self.artifacts.model
        scaler_X = self.artifacts.scaler_X
        feature_names = self.artifacts.feature_names

        recent = self._download_recent(ticker, days=90)
        X_all, y_all = self._build_features(recent)

        if X_all.empty:
            raise ValueError(f"Not enough recent data to build features for {ticker}")

        latest_X = X_all.iloc[[-1]].copy()

        # Ensure perfect training/prediction alignment
        missing = [c for c in feature_names if c not in latest_X.columns]
        if missing:
            raise ValueError(f"Missing expected feature columns: {missing}")

        latest_X = latest_X[feature_names]

        latest_scaled = scaler_X.transform(latest_X)
        pred_tomorrow = float(model.predict(latest_scaled)[0])

        current_price = float(recent["Close"].iloc[-1])
        change_pct = (pred_tomorrow / current_price - 1) * 100.0

        return {
            "ticker": ticker,
            "current_price": round(current_price, 2),
            "predicted_tomorrow": round(pred_tomorrow, 2),
            "change_pct": round(change_pct, 2),
            "direction": "UP" if pred_tomorrow > current_price else "DOWN",
        }


# Optional manual test
if __name__ == "__main__":
    reg = TomorrowPriceRegressor()
    print("TRAIN:", reg.train("AAPL", years=3))
    print("PREDICT:", reg.predict_tomorrow("AAPL"))
