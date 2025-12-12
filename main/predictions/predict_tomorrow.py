# import pandas as pd
# import yfinance as yf
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
# from sklearn.metrics import mean_squared_error
# import tensorflow as tf
# from tensorflow.keras import layers
# from indicators.feature_builder import FeatureBuilder


# class TomorrowPredictor:
#     """
#     ML pipeline:
#     - download historical data
#     - compute indicators (FeatureBuilder)
#     - train a simple regression model
#     - predict tomorrow's close
#     """

#     def __init__(self):
#         self.model = None
#         self.scaler_X = StandardScaler()
#         self.scaler_y = StandardScaler()

#     # ------------------------------------------------------------
#     # INTERNAL: Build features + target column
#     # ------------------------------------------------------------
#     def _prepare_data(self, df: pd.DataFrame) -> tuple:
#         """Runs FeatureBuilder, removes NaNs, returns (X, y)."""

#         df = df.copy()

#         # Build indicators
#         fb = FeatureBuilder(df)
#         out = fb.build()

#         # Remove warm-up NaNs
#         out = out.dropna().copy()

#         # Create target column (next-day close)
#         out.loc[:, "target"] = out["Close"].shift(-1)
#         out = out.dropna().copy()

#         # Remove non-numeric columns (Date)
#         for col in list(out.columns):
#             if out[col].dtype == "object":
#                 out = out.drop(columns=[col])

#         if "Date" in out.columns:
#             out = out.drop(columns=["Date"])

#         y = out["target"]
#         X = out.drop(columns=["target"])

#         return X, y

#     # ------------------------------------------------------------
#     # TRAIN MODEL
#     # ------------------------------------------------------------
#     def train(self, ticker: str, years: int = 5):
#         """Downloads data and trains the model."""

#         df = yf.download(
#             ticker,
#             period=f"{years}y",
#             interval="1d",
#             auto_adjust=False,   # IMPORTANT FIX
#             progress=False
#         )

#         if df.empty:
#             raise ValueError("Could not load data from yfinance.")

#         df = df.reset_index()

#         X, y = self._prepare_data(df)

#         # Scale features + target
#         X_scaled = self.scaler_X.fit_transform(X)
#         y_scaled = self.scaler_y.fit_transform(y.values.reshape(-1, 1)).flatten()

#         # Train/test split
#         X_train, X_test, y_train, y_test = train_test_split(
#             X_scaled, y_scaled, test_size=0.2, shuffle=False
#         )

#         # Build regression model
#         self.model = tf.keras.Sequential([
#             layers.Dense(1, input_shape=(X_train.shape[1],), activation="linear")
#         ])
#         self.model.compile(optimizer="adam", loss="mse")

#         # Train
#         self.model.fit(X_train, y_train, epochs=40, batch_size=32, verbose=0)

#         # Evaluate quickly
#         y_pred_scaled = self.model.predict(X_test, verbose=0)
#         y_pred = self.scaler_y.inverse_transform(y_pred_scaled).flatten()
#         y_test_orig = self.scaler_y.inverse_transform(y_test.reshape(-1, 1)).flatten()

#         mse = mean_squared_error(y_test_orig, y_pred)
#         print(f"Finished training {ticker}. Test MSE: {mse:.4f}")

#     # ------------------------------------------------------------
#     # PREDICT TOMORROW
#     # ------------------------------------------------------------
#     def predict_tomorrow(self, ticker: str):
#         """Predict tomorrow's closing price."""

#         if self.model is None:
#             raise RuntimeError("Model not trained yet. Call train(ticker) first.")

#         df = yf.download(
#             ticker,
#             period="90d",
#             interval="1d",
#             auto_adjust=False,   # IMPORTANT FIX
#             progress=False
#         ).reset_index()

#         X, y = self._prepare_data(df)

#         latest = X.iloc[-1:].copy()
#         latest_scaled = self.scaler_X.transform(latest)

#         pred_scaled = self.model.predict(latest_scaled, verbose=0)[0][0]
#         pred_price = float(self.scaler_y.inverse_transform([[pred_scaled]])[0][0])

#         current_price = float(df["Close"].iloc[-1])

#         return {
#             "ticker": ticker.upper(),
#             "current_price": round(current_price, 2),
#             "predicted_tomorrow": round(pred_price, 2),
#             "change_pct": round((pred_price / current_price - 1) * 100, 2),
#             "direction": "UP" if pred_price > current_price else "DOWN"
#         }


# # ------------------------------------------------------------
# # Manual run
# # ------------------------------------------------------------
# if __name__ == "__main__":
#     p = TomorrowPredictor()
#     p.train("AAPL", years=3)
#     print(p.predict_tomorrow("AAPL"))
"""
TomorrowPredictor
-----------------
This module trains a simple regression model to forecast tomorrow’s closing
price for a given ticker.

Workflow:
1. Download raw price data from yfinance.
2. Clean the data using DataCleaner ( goes to file data_cleaner.py so it doesnt have to handle it, this was problem)so the DataFrame consistently contains
   standardized OHLCV columns.
3. Build technical indicators using FeatureBuilder.
4. Prepare supervised learning data where the target is tomorrow’s Close.
5. Train a regression model using scaled features.
6. For prediction, download and clean the most recent data, rebuild features,
   and use the trained model to forecast the next closing price.

This ensures the model always receives clean, consistent data regardless of
whether yfinance returns lowercase columns, MultiIndex columns, or extra
fields like Dividends or Stock Splits.
"""

import pandas as pd
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import tensorflow as tf
from tensorflow.keras import layers

from indicators.feature_builder import FeatureBuilder
from data_pipeline.data_cleaner import DataCleaner   # NEW IMPORT


class TomorrowPredictor:
    """
    ML pipeline:
    - download historical data
    - clean data (DataCleaner)
    - compute indicators (FeatureBuilder)
    - train a simple regression model
    - predict tomorrow's close
    """

    def __init__(self):
        self.model = None
        self.scaler_X = StandardScaler()
        self.scaler_y = StandardScaler()

    # ------------------------------------------------------------
    # INTERNAL: Build features + target column
    # ------------------------------------------------------------
    def _prepare_data(self, df: pd.DataFrame) -> tuple:
        """Runs FeatureBuilder, removes NaNs, returns (X, y)."""

        df = df.copy()

        # Build indicators
        fb = FeatureBuilder(df)
        out = fb.build()

        # Remove warm-up NaNs
        out = out.dropna().copy()

        # Create target column (next-day close)
        out.loc[:, "target"] = out["Close"].shift(-1)
        out = out.dropna().copy()

        # Remove non-numeric columns (Date etc.)
        for col in list(out.columns):
            if out[col].dtype == "object":
                out = out.drop(columns=[col])

        if "Date" in out.columns:
            out = out.drop(columns=["Date"])

        y = out["target"]
        X = out.drop(columns=["target"])

        return X, y

    # ------------------------------------------------------------
    # TRAIN MODEL
    # ------------------------------------------------------------
    def train(self, ticker: str, years: int = 5):
        """Downloads data, cleans it, and trains the model."""

        df = yf.download(
            ticker,
            period=f"{years}y",
            interval="1d",
            auto_adjust=False,
            progress=False
        )

        if df.empty:
            raise ValueError("Could not load data from yfinance.")

        df = df.reset_index()
        df = DataCleaner(df).clean()    # CLEAN RAW DATA

        X, y = self._prepare_data(df)

        # Scale
        X_scaled = self.scaler_X.fit_transform(X)
        y_scaled = self.scaler_y.fit_transform(y.values.reshape(-1, 1)).flatten()

        # Split
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y_scaled, test_size=0.2, shuffle=False
        )

        # Regression model
        self.model = tf.keras.Sequential([
            layers.Dense(1, input_shape=(X_train.shape[1],), activation="linear")
        ])
        self.model.compile(optimizer="adam", loss="mse")

        # Train
        self.model.fit(X_train, y_train, epochs=40, batch_size=32, verbose=0)

        # Evaluate
        y_pred_scaled = self.model.predict(X_test, verbose=0)
        y_pred = self.scaler_y.inverse_transform(y_pred_scaled).flatten()
        y_test_orig = self.scaler_y.inverse_transform(y_test.reshape(-1, 1)).flatten()

        mse = mean_squared_error(y_test_orig, y_pred)
        print(f"Finished training {ticker}. Test MSE: {mse:.4f}")

    # ------------------------------------------------------------
    # PREDICT TOMORROW
    # ------------------------------------------------------------
    def predict_tomorrow(self, ticker: str):
        """Predict tomorrow's closing price."""

        if self.model is None:
            raise RuntimeError("Model not trained yet. Call train(ticker) first.")

        df = yf.download(
            ticker,
            period="90d",
            interval="1d",
            auto_adjust=False,
            progress=False
        ).reset_index()

        df = DataCleaner(df).clean()   # CLEAN RAW DATA

        X, y = self._prepare_data(df)

        latest = X.iloc[-1:].copy()
        latest_scaled = self.scaler_X.transform(latest)

        pred_scaled = self.model.predict(latest_scaled, verbose=0)[0][0]
        pred_price = float(self.scaler_y.inverse_transform([[pred_scaled]])[0][0])

        current_price = float(df["Close"].iloc[-1])

        return {
            "ticker": ticker.upper(),
            "current_price": round(current_price, 2),
            "predicted_tomorrow": round(pred_price, 2),
            "change_pct": round((pred_price / current_price - 1) * 100, 2),
            "direction": "UP" if pred_price > current_price else "DOWN"
        }


if __name__ == "__main__":
    p = TomorrowPredictor()
    p.train("AAPL", years=3)
    print(p.predict_tomorrow("AAPL"))
