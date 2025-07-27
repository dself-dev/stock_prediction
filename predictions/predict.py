

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import warnings
warnings.filterwarnings('ignore')

def main():
    # Load the data
    df = pd.read_csv('AAPL_1d_complete.csv')
    
    # Convert Date to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Remove rows where key indicators are missing
    key_columns = ['RSI_14', 'Bollinger_Upper', 'Bollinger_Middle', 'Bollinger_Lower', 
                   'EMA_12', 'EMA_26', 'SMA_10', 'SMA_20', 'SMA_50', 'MACD', 'MACD_Signal']
    
    df_clean = df.dropna(subset=key_columns)
    print(f"Dataset after cleaning: {df_clean.shape[0]} rows")
    
    # Define features and target
    feature_columns = [
        'Open', 'High', 'Low', 'Volume',
        'RSI_14', 'Bollinger_Upper', 'Bollinger_Middle', 'Bollinger_Lower',
        'EMA_12', 'EMA_26', 'SMA_10', 'SMA_20', 'SMA_50',
        'MACD', 'MACD_Signal', 'Stoch_K', 'Stoch_D', 'ATR', 'Volume_SMA'
    ]
    
    target_column = 'Close'
    
    # Select features and target
    X = df_clean[feature_columns].copy()
    y = df_clean[target_column].copy()
    
    # Handle any remaining NaN values
    X = X.fillna(method='ffill').fillna(method='bfill')
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, shuffle=False
    )
    
    print(f"Training set: X_train {X_train.shape}, y_train {y_train.shape}")
    print(f"Test set: X_test {X_test.shape}, y_test {y_test.shape}")
    
    # Scale the features
    scaler_X = StandardScaler()
    X_train_scaled = scaler_X.fit_transform(X_train)
    X_test_scaled = scaler_X.transform(X_test)
    
    # Scale the target
    scaler_y = StandardScaler()
    y_train_scaled = scaler_y.fit_transform(y_train.values.reshape(-1, 1)).flatten()
    y_test_scaled = scaler_y.transform(y_test.values.reshape(-1, 1)).flatten()
    
    # Build the Keras linear regression model
    model = keras.Sequential([
        layers.Dense(1, input_shape=(X_train_scaled.shape[1],), activation='linear')
    ])
    
    # Compile the model
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    
    print("Training model...")
    # Train the model
    model.fit(X_train_scaled, y_train_scaled, epochs=100, batch_size=32, 
              validation_split=0.2, verbose=0)
    
    # Make predictions
    y_pred_scaled = model.predict(X_test_scaled, verbose=0)
    y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1)).flatten()
    
    # Calculate metrics
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\nModel Performance:")
    print(f"Mean Squared Error: {mse:.6f}")
    print(f"Root Mean Squared Error: {rmse:.6f}")
    print(f"R² Score: {r2:.6f}")
    
    # Show some sample predictions
    print(f"\nSample predictions:")
    for i in range(min(5, len(y_test))):
        print(f"Actual: ${y_test.iloc[i]:.2f}, Predicted: ${y_pred[i]:.2f}")
    
    print("\nModel training complete!")

if __name__ == "__main__":
    main()