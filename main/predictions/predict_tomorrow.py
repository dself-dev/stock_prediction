

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.preprocessing import StandardScaler

# -------------------------------------------------
# DETERMINISM
# -------------------------------------------------
tf.random.set_seed(42)
np.random.seed(42)


class TomorrowPredictor:
    """
    Trains and predicts using only RSI and Bollinger Band features.
    """

    FEATURE_COLUMNS = [
        "RSI_14",
        "Bollinger_Upper",
        "Bollinger_Middle",
        "Bollinger_Lower",
    ]

    KEY_COLUMNS = FEATURE_COLUMNS

    def __init__(self):
        self.model = None
        self.scaler_X = StandardScaler()
        self.scaler_y = StandardScaler()
        self.trained = False

    # -------------------------------------------------
    # TRAIN
    # -------------------------------------------------
    def train(self, df: pd.DataFrame):
        df = df.copy()

        # Ensure required indicators exist
        df_clean = df.dropna(subset=self.KEY_COLUMNS)

        X = (
            df_clean[self.FEATURE_COLUMNS]
            .ffill()
            .bfill()
        )

        y = df_clean["Close"]

        # Scale features and target
        X_scaled = self.scaler_X.fit_transform(X)
        y_scaled = self.scaler_y.fit_transform(
            y.values.reshape(-1, 1)
        ).flatten()

        # TRUE linear regression (no hidden layers)
        self.model = keras.Sequential([
            keras.Input(shape=(X_scaled.shape[1],)),
            layers.Dense(1, activation="linear"),
        ])

        self.model.compile(
            optimizer="adam",
            loss="mse",
            metrics=["mae"],
        )

        self.model.fit(
            X_scaled,
            y_scaled,
            epochs=100,
            batch_size=32,
            validation_split=0.1,
            verbose=0,
        )

        self.trained = True

    # -------------------------------------------------
    # PREDICT TOMORROW
    # -------------------------------------------------
    def predict(self, df: pd.DataFrame):
        if not self.trained:
            raise RuntimeError("Model not trained")

        df = df.copy()
        df_clean = df.dropna(subset=self.KEY_COLUMNS)

        today = df_clean.iloc[-1]
        current_price = today["Close"]

        # Preserve feature names for scaler
        X_today_df = pd.DataFrame(
            [today[self.FEATURE_COLUMNS].values],
            columns=self.FEATURE_COLUMNS,
        )

        X_today_scaled = self.scaler_X.transform(X_today_df)

        prediction_scaled = self.model.predict(
            X_today_scaled, verbose=0
        )

        predicted_close = self.scaler_y.inverse_transform(
            prediction_scaled.reshape(-1, 1)
        )[0][0]

        change = predicted_close - current_price
        change_pct = (change / current_price) * 100

        return predicted_close, current_price, change_pct
