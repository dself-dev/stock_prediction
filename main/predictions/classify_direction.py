"""
classify_direction.py
---------------------
Simple binary classifier using Keras to predict
UP (1) or DOWN (0) for next-day stock movement
based on technical indicators from combined_indicators.py
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# ---------------------------------------------------------
# 1. Load dataset
# ---------------------------------------------------------
csv_file = input("Enter CSV filename (e.g. AAPL_1d_complete.csv): ").strip()
df = pd.read_csv(csv_file)

print(f" Loaded {csv_file} with shape: {df.shape}")

# ---------------------------------------------------------
# 2. Prepare features for the (X) and  (y) labels hopefully here if not I quit and I'll start learnit front end or learn philosophy!!!
# ---------------------------------------------------------
# Make sure there is a 'Close' column for price
if 'Close' not in df.columns:
    raise ValueError("CSV must contain a 'Close' column")

# Create label: 1 if tomorrow's close >= today's close else 0
df['Tomorrow_Close'] = df['Close'].shift(-1)
df['Label'] = np.where(df['Tomorrow_Close'] >= df['Close'], 1, 0)

# Drop last row (no label because shift is going to  create NaN)
df = df.dropna()

# Choose feature columns – drop non-numeric or date-time columns
feature_cols = df.select_dtypes(include=[np.number]).columns.tolist()

# Remove columns we don’t want as features
for col in ['Label', 'Tomorrow_Close', 'Volume']:  # remove label & helper
    if col in feature_cols:
        feature_cols.remove(col)

X = df[feature_cols].values
y = df['Label'].values

print(f"Using {len(feature_cols)} features: {feature_cols[:5]} ...")

# ---------------------------------------------------------
# 3. Train / Test split
# ---------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

# ---------------------------------------------------------
# 4. Scale features
# ---------------------------------------------------------
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# ---------------------------------------------------------
# 5. Build Keras classifier
# ---------------------------------------------------------
model = keras.Sequential([
    layers.Input(shape=(X_train.shape[1],)),
    layers.Dense(32, activation='relu'),
    layers.Dense(16, activation='relu'),
    layers.Dense(1, activation='sigmoid')     # sigmoid → outputs probability [0,1]
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# ---------------------------------------------------------
# 6. Train model
# ---------------------------------------------------------
print(" Training classifier...")
history = model.fit(
    X_train, y_train,
    validation_split=0.1,
    epochs=25,
    batch_size=32,
    verbose=1
)

# ---------------------------------------------------------
# 7. Evaluate
# ---------------------------------------------------------
y_pred_prob = model.predict(X_test)
y_pred = (y_pred_prob >= 0.5).astype(int).flatten()

acc = accuracy_score(y_test, y_pred)
print(f"\n✅ Test Accuracy: {acc:.3f}")
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# ---------------------------------------------------------
# 8. Predict last known day’s direction
# ---------------------------------------------------------
latest_features = X[-1].reshape(1, -1)
latest_prob = model.predict(latest_features)[0][0]
direction = "UP" if latest_prob >= 0.5 else "DOWN"

print(f"\n📈 Latest day prediction → {direction} "
      f"(Probability UP={latest_prob:.2f})")

print("\nDone.")
