


import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.preprocessing import StandardScaler

# -------------------------------------------------
#  - Setting seeds so results are the same every time
# -------------------------------------------------
tf.random.set_seed(42)
np.random.seed(42)

class TomorrowPredictor:
    """
    Trains and predicts tomorrow's close using RSI and Bollinger features from FeatureBuilder.
    Supports linear regression, nonlinear MLP, or both at the same time.
    I set it up this way so it can spit out numbers from linear and nonlinear together if I want.
    Data comes from FastAPI: user picks ticker and dates, it fetches/cleans, adds indicators, then here.
    """

    FEATURE_COLUMNS = [
        "RSI_14",
        "Bollinger_Upper",
        "Bollinger_Middle",
        "Bollinger_Lower",
    ]

    KEY_COLUMNS = FEATURE_COLUMNS

    def __init__(self, model_type='both'):
        """
        Sets up the predictor with what model to use.
        'both' does linear and nonlinear, which is cool for seeing both outputs side by side.
        """
        if model_type not in ['linear', 'nonlinear', 'both']:
            raise ValueError("model_type must be 'linear', 'nonlinear', or 'both'")
        self.model_type = model_type
        self.model_linear = None  # Holds the linear model if I pick it or both
        self.model_nonlinear = None  # Holds the nonlinear MLP model if I pick it or both
        self.scaler_X = StandardScaler()
        self.scaler_y = StandardScaler()
        self.trained = False

    # -------------------------------------------------
    # PREPARE DATA - Same prep for linear and nonlinear
    # -------------------------------------------------
    def _prepare_data(self, df: pd.DataFrame):
        """
        Gets data ready by adding indicators and cleaning up.
        No difference between linear and nonlinear here - shared step.
        DF should already be cleaned from DataCleaner before this.
        """
        if df is None or df.empty:
            raise ValueError("Input DataFrame is empty.")

        df = df.copy()

        # BUILD INDICATORS FIRST - Pulls in RSI_14, Bollinger, etc. from FeatureBuilder
        from indicators.feature_builder import FeatureBuilder
        df = FeatureBuilder(df).build()

        df_clean = df.dropna(subset=self.KEY_COLUMNS).copy()

        if len(df_clean) < 50:
            raise ValueError(f"Not enough clean data. Rows: {len(df_clean)}")

        X = df_clean[["Close", *self.FEATURE_COLUMNS]].ffill().bfill()
        y = df_clean["Close"]

        return X, y

    # -------------------------------------------------
    # BUILD MODELS - One for linear, one for nonlinear
    # -------------------------------------------------
    def _build_linear_model(self, input_shape):
        """
        Sets up the linear regression model.
        This is the linear part - simple single layer with linear activation.
        """
        model = keras.Sequential([
            keras.Input(shape=input_shape),
            layers.Dense(1, activation="linear"),
        ])
        model.compile(optimizer="adam", loss="mse", metrics=["mae"])
        return model

    def _build_nonlinear_model(self, input_shape):
        """
        Sets up the nonlinear MLP model.
        This is the nonlinear part - layers with ReLU to capture more complex patterns.
        """
        model = keras.Sequential([
            keras.Input(shape=input_shape),
            layers.Dense(64, activation="relu"),
            layers.Dense(32, activation="relu"),
            layers.Dense(1, activation="linear"),
        ])
        model.compile(optimizer="adam", loss="mse", metrics=["mae"])
        return model

    # -------------------------------------------------
    # TRAIN - Handles training for linear, nonlinear, or both
    # -------------------------------------------------
    def train(self, df: pd.DataFrame):
        """
        Trains whatever model(s) I picked on the data.
        If 'both', it trains linear and nonlinear on the same scaled features.
        Added early stopping to both so they don't overfit.
        """
        X, y = self._prepare_data(df)

        X_scaled = self.scaler_X.fit_transform(X[self.FEATURE_COLUMNS])
        y_scaled = self.scaler_y.fit_transform(y.values.reshape(-1, 1)).flatten()

        input_shape = (X_scaled.shape[1],)

        # Early stopping - same for linear and nonlinear
        early_stop = keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=10,
            restore_best_weights=True,
        )

        if self.model_type in ['linear', 'both']:
            # Building and training the linear model here
            self.model_linear = self._build_linear_model(input_shape)
            self.model_linear.fit(
                X_scaled, y_scaled,
                epochs=100, batch_size=32, validation_split=0.1,
                callbacks=[early_stop], verbose=0
            )

        if self.model_type in ['nonlinear', 'both']:
            # Building and training the nonlinear MLP model here
            self.model_nonlinear = self._build_nonlinear_model(input_shape)
            self.model_nonlinear.fit(
                X_scaled, y_scaled,
                epochs=100, batch_size=32, validation_split=0.1,
                callbacks=[early_stop], verbose=0
            )

        self.trained = True

    # -------------------------------------------------
    # PREDICT - Spits out predictions from linear, nonlinear, or both
    # -------------------------------------------------
    def predict(self, df: pd.DataFrame):
        """
        Predicts tomorrow's close price.
        Returns a dict so if 'both', I get linear and nonlinear results.
        Each has predicted_close, current_price, change_pct.
        This is the part that spits out the numbers - can do both in one go.
        """
        if not self.trained:
            raise RuntimeError("Model not trained")

        df = df.copy()

        # BUILD INDICATORS AGAIN - Just like in prepare_data
        from indicators.feature_builder import FeatureBuilder
        df = FeatureBuilder(df).build()

        df_clean = df.dropna(subset=self.KEY_COLUMNS).copy()

        if len(df_clean) == 0:
            raise ValueError("No valid rows for prediction")

        today = df_clean.iloc[-1]
        current_price = today["Close"]

        X_today_df = pd.DataFrame(
            [today[self.FEATURE_COLUMNS].values],
            columns=self.FEATURE_COLUMNS,
        )
        X_today_scaled = self.scaler_X.transform(X_today_df)

        results = {}

        def get_prediction(model):
            """
            Quick helper to calculate prediction - works for linear or nonlinear models.
            """
            prediction_scaled = model.predict(X_today_scaled, verbose=0)
            predicted_close = self.scaler_y.inverse_transform(
                prediction_scaled.reshape(-1, 1)
            )[0][0]
            change = predicted_close - current_price
            change_pct = (change / current_price) * 100
            return predicted_close, current_price, change_pct

        if self.model_type in ['linear', 'both']:
            if self.model_linear is None:
                raise RuntimeError("Linear model not trained")
            # Getting the prediction from the linear model
            results['linear'] = get_prediction(self.model_linear)

        if self.model_type in ['nonlinear', 'both']:
            if self.model_nonlinear is None:
                raise RuntimeError("Nonlinear model not trained")
            # Getting the prediction from the nonlinear MLP model
            results['nonlinear'] = get_prediction(self.model_nonlinear)

        return results  # Like {'linear': (pred, curr, pct), 'nonlinear': (pred, curr, pct)}