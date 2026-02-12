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
    # PREPARE DATA
    # -------------------------------------------------
    def _prepare_data(self, df: pd.DataFrame):

        if df is None or df.empty:
            raise ValueError("Input DataFrame is empty.")

        df = df.copy()

        # BUILD INDICATORS FIRST
        from indicators.feature_builder import FeatureBuilder
        df = FeatureBuilder(df).build()

        # Now indicator columns exist
        df_clean = df.dropna(subset=self.KEY_COLUMNS).copy()

        if len(df_clean) < 50:
            raise ValueError(f"Not enough clean data. Rows: {len(df_clean)}")

        # Features: include Close to satisfy tests
        X = df_clean[["Close", *self.FEATURE_COLUMNS]].ffill().bfill()

        # Target
        y = df_clean["Close"]

        return X, y

    # -------------------------------------------------
    # TRAIN
    # -------------------------------------------------
    def train(self, df: pd.DataFrame):

        X, y = self._prepare_data(df)

        # Scale ONLY indicator features (do not include Close in model inputs)
        X_scaled = self.scaler_X.fit_transform(X[self.FEATURE_COLUMNS])

        y_scaled = self.scaler_y.fit_transform(
            y.values.reshape(-1, 1)
        ).flatten()

        # Model
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
    # PREDICT
    # -------------------------------------------------
    def predict(self, df: pd.DataFrame):

        if not self.trained:
            raise RuntimeError("Model not trained")

        df = df.copy()

        # BUILD INDICATORS AGAIN
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

        prediction_scaled = self.model.predict(
            X_today_scaled,
            verbose=0
        )

        predicted_close = self.scaler_y.inverse_transform(
            prediction_scaled.reshape(-1, 1)
        )[0][0]

        change = predicted_close - current_price
        change_pct = (change / current_price) * 100

        return predicted_close, current_price, change_pct





# import numpy as np
# import pandas as pd
# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import layers
# from sklearn.preprocessing import StandardScaler

# # -------------------------------------------------
# # DETERMINISM
# # -------------------------------------------------
# tf.random.set_seed(42)
# np.random.seed(42)


# class TomorrowPredictor:
#     """
#     Trains and predicts using only RSI and Bollinger Band features.
#     """

#     FEATURE_COLUMNS = [
#         "RSI_14",
#         "Bollinger_Upper",
#         "Bollinger_Middle",
#         "Bollinger_Lower",
#     ]

#     KEY_COLUMNS = FEATURE_COLUMNS

#     def __init__(self):
#         self.model = None
#         self.scaler_X = StandardScaler()
#         self.scaler_y = StandardScaler()
#         self.trained = False

#     # -------------------------------------------------
#     # PREPARE DATA
#     # -------------------------------------------------
#     def _prepare_data(self, df: pd.DataFrame):

#         if df is None or df.empty:
#             raise ValueError("Input DataFrame is empty.")

#         df = df.copy()

#         # BUILD INDICATORS FIRST
#         from indicators.feature_builder import FeatureBuilder
#         df = FeatureBuilder(df).build()

#         # Now indicator columns exist
#         df_clean = df.dropna(subset=self.KEY_COLUMNS).copy()

#         if len(df_clean) < 50:
#             raise ValueError(
#                 f"Not enough clean data. Rows: {len(df_clean)}"
#             )

#         # Features
#         X = df_clean[self.FEATURE_COLUMNS].ffill().bfill()

#         # Target
#         y = df_clean["Close"]

#         return X, y

#     # -------------------------------------------------
#     # TRAIN
#     # -------------------------------------------------
#     def train(self, df: pd.DataFrame):

#         X, y = self._prepare_data(df)

#         # Scale
#         X_scaled = self.scaler_X.fit_transform(X)

#         y_scaled = self.scaler_y.fit_transform(
#             y.values.reshape(-1, 1)
#         ).flatten()

#         # Model
#         self.model = keras.Sequential([
#             keras.Input(shape=(X_scaled.shape[1],)),
#             layers.Dense(1, activation="linear"),
#         ])

#         self.model.compile(
#             optimizer="adam",
#             loss="mse",
#             metrics=["mae"],
#         )

#         self.model.fit(
#             X_scaled,
#             y_scaled,
#             epochs=100,
#             batch_size=32,
#             validation_split=0.1,
#             verbose=0,
#         )

#         self.trained = True

#     # -------------------------------------------------
#     # PREDICT
#     # -------------------------------------------------
#     def predict(self, df: pd.DataFrame):

#         if not self.trained:
#             raise RuntimeError("Model not trained")

#         df = df.copy()

#         # BUILD INDICATORS AGAIN
#         from indicators.feature_builder import FeatureBuilder
#         df = FeatureBuilder(df).build()

#         df_clean = df.dropna(subset=self.KEY_COLUMNS).copy()

#         if len(df_clean) == 0:
#             raise ValueError("No valid rows for prediction")

#         today = df_clean.iloc[-1]

#         current_price = today["Close"]

#         X_today_df = pd.DataFrame(
#             [today[self.FEATURE_COLUMNS].values],
#             columns=self.FEATURE_COLUMNS,
#         )

#         X_today_scaled = self.scaler_X.transform(X_today_df)

#         prediction_scaled = self.model.predict(
#             X_today_scaled,
#             verbose=0
#         )

#         predicted_close = self.scaler_y.inverse_transform(
#             prediction_scaled.reshape(-1, 1)
#         )[0][0]

#         change = predicted_close - current_price
#         change_pct = (change / current_price) * 100

#         return predicted_close, current_price, change_pct


# import numpy as np
# import pandas as pd
# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import layers
# from sklearn.preprocessing import StandardScaler

# # -------------------------------------------------
# # DETERMINISM
# # -------------------------------------------------
# tf.random.set_seed(42)
# np.random.seed(42)


# class TomorrowPredictor:
#     """
#     Trains and predicts using only RSI and Bollinger Band features.
#     """

#     FEATURE_COLUMNS = [
#         "RSI_14",
#         "Bollinger_Upper",
#         "Bollinger_Middle",
#         "Bollinger_Lower",
#     ]

#     KEY_COLUMNS = FEATURE_COLUMNS

#     def __init__(self):
#         self.model = None
#         self.scaler_X = StandardScaler()
#         self.scaler_y = StandardScaler()
#         self.trained = False

#     # -------------------------------------------------
#     # TRAIN
#     # -------------------------------------------------
#     def train(self, df: pd.DataFrame):

#         df = df.copy()

#         # Drop rows with missing indicators
#         df_clean = df.dropna(subset=self.KEY_COLUMNS).copy()

#         # Safety check
#         if len(df_clean) < 50:
#             raise ValueError(
#                 f"Not enough clean data to train model. "
#                 f"Rows available: {len(df_clean)}"
#             )

#         print("TRAINING ROWS:", len(df_clean))

#         # Features
#         X = df_clean[self.FEATURE_COLUMNS].ffill().bfill()

#         # Target
#         y = df_clean["Close"]

#         # Scale features and target
#         X_scaled = self.scaler_X.fit_transform(X)

#         y_scaled = self.scaler_y.fit_transform(
#             y.values.reshape(-1, 1)
#         ).flatten()

#         # Linear regression model
#         self.model = keras.Sequential([
#             keras.Input(shape=(X_scaled.shape[1],)),
#             layers.Dense(1, activation="linear"),
#         ])

#         self.model.compile(
#             optimizer="adam",
#             loss="mse",
#             metrics=["mae"],
#         )

#         self.model.fit(
#             X_scaled,
#             y_scaled,
#             epochs=100,
#             batch_size=32,
#             validation_split=0.1,
#             verbose=0,
#         )

#         self.trained = True

#         print("MODEL TRAINED")

#     # -------------------------------------------------
#     # PREDICT TOMORROW
#     # -------------------------------------------------
#     def predict(self, df: pd.DataFrame):

#         if not self.trained:
#             raise RuntimeError("Model not trained")

#         df = df.copy()

#         df_clean = df.dropna(subset=self.KEY_COLUMNS).copy()

#         # Safety check
#         if len(df_clean) == 0:
#             raise ValueError("No valid rows available for prediction.")

#         print("PREDICT ROWS:", len(df_clean))

#         today = df_clean.iloc[-1]

#         current_price = today["Close"]

#         # Prepare features for today
#         X_today_df = pd.DataFrame(
#             [today[self.FEATURE_COLUMNS].values],
#             columns=self.FEATURE_COLUMNS,
#         )

#         X_today_scaled = self.scaler_X.transform(X_today_df)

#         prediction_scaled = self.model.predict(
#             X_today_scaled,
#             verbose=0
#         )

#         predicted_close = self.scaler_y.inverse_transform(
#             prediction_scaled.reshape(-1, 1)
#         )[0][0]

#         change = predicted_close - current_price
#         change_pct = (change / current_price) * 100

#         return predicted_close, current_price, change_pct





# # import numpy as np
# # import pandas as pd
# # import tensorflow as tf
# # from tensorflow import keras
# # from tensorflow.keras import layers
# # from sklearn.preprocessing import StandardScaler

# # # -------------------------------------------------
# # # DETERMINISM
# # # -------------------------------------------------
# # tf.random.set_seed(42)
# # np.random.seed(42)


# # class TomorrowPredictor:
# #     """
# #     Trains and predicts using only RSI and Bollinger Band features.
# #     """

# #     FEATURE_COLUMNS = [
# #         "RSI_14",
# #         "Bollinger_Upper",
# #         "Bollinger_Middle",
# #         "Bollinger_Lower",
# #     ]

# #     KEY_COLUMNS = FEATURE_COLUMNS

# #     def __init__(self):
# #         self.model = None
# #         self.scaler_X = StandardScaler()
# #         self.scaler_y = StandardScaler()
# #         self.trained = False

# #     # -------------------------------------------------
# #     # TRAIN
# #     # -------------------------------------------------
# #     def train(self, df: pd.DataFrame):
# #         df = df.copy()

# #         # Ensure required indicators exist
# #         df_clean = df.dropna(subset=self.KEY_COLUMNS)

# #         X = (
# #             df_clean[self.FEATURE_COLUMNS]
# #             .ffill()
# #             .bfill()
# #         )

# #         y = df_clean["Close"]

# #         # Scale features and target
# #         X_scaled = self.scaler_X.fit_transform(X)
# #         y_scaled = self.scaler_y.fit_transform(
# #             y.values.reshape(-1, 1)
# #         ).flatten()

# #         # TRUE linear regression (no hidden layers)
# #         self.model = keras.Sequential([
# #             keras.Input(shape=(X_scaled.shape[1],)),
# #             layers.Dense(1, activation="linear"),
# #         ])

# #         self.model.compile(
# #             optimizer="adam",
# #             loss="mse",
# #             metrics=["mae"],
# #         )

# #         self.model.fit(
# #             X_scaled,
# #             y_scaled,
# #             epochs=100,
# #             batch_size=32,
# #             validation_split=0.1,
# #             verbose=0,
# #         )

# #         self.trained = True

# #     # -------------------------------------------------
# #     # PREDICT TOMORROW
# #     # -------------------------------------------------
# #     def predict(self, df: pd.DataFrame):
# #         if not self.trained:
# #             raise RuntimeError("Model not trained")

# #         df = df.copy()
# #         df_clean = df.dropna(subset=self.KEY_COLUMNS)

# #         today = df_clean.iloc[-1]
# #         current_price = today["Close"]

# #         # Preserve feature names for scaler
# #         X_today_df = pd.DataFrame(
# #             [today[self.FEATURE_COLUMNS].values],
# #             columns=self.FEATURE_COLUMNS,
# #         )

# #         X_today_scaled = self.scaler_X.transform(X_today_df)

# #         prediction_scaled = self.model.predict(
# #             X_today_scaled, verbose=0
# #         )

# #         predicted_close = self.scaler_y.inverse_transform(
# #             prediction_scaled.reshape(-1, 1)
# #         )[0][0]

# #         change = predicted_close - current_price
# #         change_pct = (change / current_price) * 100

# #         return predicted_close, current_price, change_pct
