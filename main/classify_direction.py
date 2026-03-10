import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras import layers

class DirectionClassifier:
    """
    Binary classifier to predict UP (1) or DOWN (0) for next-day movement
    based on technical indicators from FeatureBuilder.
    """

    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.trained = False

    def _prepare_data(self, df: pd.DataFrame):
        if df is None or df.empty:
            raise ValueError("Input DataFrame is empty.")

        df = df.copy()

        # Assume df already has indicators from FeatureBuilder
        # Create label: 1 if next close >= current, else 0 (shift for training)
        df['Tomorrow_Close'] = df['Close'].shift(-1)
        df['Label'] = np.where(df['Tomorrow_Close'] >= df['Close'], 1, 0)

        # Drop NaNs (last row has no label)
        df = df.dropna()

        # Features: All numeric except labels/helpers
        feature_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        for col in ['Label', 'Tomorrow_Close', 'Volume']:  # Exclude these
            if col in feature_cols:
                feature_cols.remove(col)

        X = df[feature_cols].values
        y = df['Label'].values

        return X, y, feature_cols

    def train(self, df: pd.DataFrame):
        X, y, _ = self._prepare_data(df)

        if len(X) < 50:
            raise ValueError("Not enough data for training.")

        # Split and scale
        X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, shuffle=False)
        X_train = self.scaler.fit_transform(X_train)

        # Build model
        self.model = keras.Sequential([
            layers.Input(shape=(X_train.shape[1],)),
            layers.Dense(32, activation='relu'),
            layers.Dense(16, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])

        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        # Train
        self.model.fit(
            X_train, y_train,
            validation_split=0.1,
            epochs=25,
            batch_size=32,
            verbose=0
        )

        self.trained = True

    def predict_direction(self, df: pd.DataFrame):
        if not self.trained:
            raise RuntimeError("Model not trained")

        # Get latest row's features (no shift needed for prediction)
        _, _, feature_cols = self._prepare_data(df)  # Get cols
        latest = df.iloc[-1][feature_cols].values.reshape(1, -1)
        latest_scaled = self.scaler.transform(latest)

        prob = self.model.predict(latest_scaled, verbose=0)[0][0]
        direction = "UP" if prob >= 0.5 else "DOWN"
        return direction, prob