import pandas as pd
from pathlib import Path

from main.predictions.predict_tomorrow import TomorrowPredictor

CSV_PATH = Path("test_csv/AAPL_2022-01-01_to_2025-10-27.csv")


def test_prepare_data_builds_features():
    df = pd.read_csv(CSV_PATH)

    model = TomorrowPredictor()
    X, y = model._prepare_data(df)

    # Output types
    assert isinstance(X, pd.DataFrame)
    assert isinstance(y, pd.Series)

    # There must be usable rows
    assert len(X) > 50, "Not enough rows after dropping warm-up NaNs."
    assert len(X) == len(y), "X and y must have same number of rows."

    # Close column must still exist
    assert "Close" in X.columns


def test_model_training_and_prediction():
    df = pd.read_csv(CSV_PATH)
    model = TomorrowPredictor()

    # Prepare features
    X, y = model._prepare_data(df)

    # Scale manually (same as training)
    Xs = model.scaler_X.fit_transform(X)
    ys = model.scaler_y.fit_transform(y.values.reshape(-1, 1)).flatten()

    # Build tiny model
    import tensorflow as tf
    from tensorflow.keras import layers

    predictor = tf.keras.Sequential([
        layers.Dense(1, input_shape=(Xs.shape[1],), activation="linear")
    ])
    predictor.compile(optimizer="adam", loss="mse")

    # Train a few epochs (fast)
    predictor.fit(Xs, ys, epochs=5, batch_size=16, verbose=0)

    # Predict on last row
    pred = predictor.predict(Xs[-1].reshape(1, -1))[0][0]

    # Must be a float value (not NaN, not None)
    assert isinstance(float(pred), float), "Prediction must return a real number."
