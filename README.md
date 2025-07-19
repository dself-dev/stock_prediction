## 👨‍💻 Author

**Dennis Selfinger**  
* Machine Learning Engineer & Quantitative Analyst-Software Engineer*

- 📊 Achieved 96% accuracy on real-world stock prediction (July 2025)
- 🎯 Specialized in financial machine learning and technical analysis
- 💼 2+ years of data science and algorithmic trading experience
- 🏆 

**Contact:**
- GitHub: [@Dself76](https://github.com/Dself76)


# 🎯 Stock Prediction Model - 96% Accuracy


**Real-world tested machine learning model for stock price prediction using technical indicators**

![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.19-orange.svg)
![Accuracy](https://img.shields.io/badge/Accuracy-96%25-brightgreen.svg)

## 🚀 Results

**Real-world validation on AAPL (July 16, 2025):**
- **Predicted:** $211.02
- **Actual:** $210.16  
- **Error:** $0.86 (0.4%)
- **Direction:** ✅ Correctly predicted UP movement

## 📊 Model Performance

| Stock | R² Score | RMSE | Test Period |
|-------|----------|------|-------------|
| AAPL  | 95.1%    | $3.40| 5 years     |
| IONQ  | 97.6%    | $1.89| 5 years     |

## 🛠️ Features

**Technical Indicators Used:**
- RSI (14-period)
- Bollinger Bands (Upper, Middle, Lower)
- EMAs (12, 26-period)
- SMAs (10, 20, 50-period)
- MACD & MACD Signal
- Stochastic (K, D)
- Average True Range (ATR)
- Volume SMA

## 🏗️ Architecture

- **Model:** Keras Linear Regression
- **Training:** 500 epochs
- **Features:**  a perfect num of  technical indicators as not to overfit
- **Data:** 5 years of daily OHLCV data
- **Preprocessing:** StandardScaler normalization

## 📁 Files

```
├── predict.py                    # Main prediction model
├── predict_tomorrow_apple.py     # Real-time prediction script
├── combined_indicators.py        # Data fetching and indicator calculation
├── rsi_only.py                  # RSI-only model experiment
├── sma.py                       # SMA-based model
└── README.md                    # This file
```

## 📦 Dependencies

```
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
tensorflow>=2.19.0
yfinance>=0.2.0
ta>=0.10.0
```

Create a `requirements.txt` file:
```bash
echo "pandas>=2.0.0" > requirements.txt
echo "numpy>=1.24.0" >> requirements.txt
echo "scikit-learn>=1.3.0" >> requirements.txt
echo "tensorflow>=2.19.0" >> requirements.txt
echo "yfinance>=0.2.0" >> requirements.txt
echo "ta>=0.10.0" >> requirements.txt
```

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/Dself76/stock_prediction.git
cd stock_prediction
```

### 2. Create virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install pandas numpy scikit-learn tensorflow yfinance ta
```

### 4. Get stock data
```bash
python combined_indicators.py
# Enter ticker (e.g., AAPL)
# Enter date range
```

### 5. Train and predict
```bash
python predict.py                    # Historical backtesting
python predict_tomorrow_apple.py     # Real-time prediction
```

## 📈 Usage Examples

### Get Stock Data with Indicators
```python
python combined_indicators.py
# Enter: AAPL
# Enter: 1d  
# Enter: 2020-01-01
# Enter: 2025-07-15
```

### Make Predictions
```python
python predict_tomorrow_apple.py
# Outputs: Tomorrow's predicted closing price
```

## 🧮 How It Works

1. **Data Collection:** Fetches OHLCV data using yfinance
2. **Feature Engineering:** Calculates 19 technical indicators
3. **Preprocessing:** Normalizes features using StandardScaler
4. **Training:** Linear regression with TensorFlow/Keras
5. **Prediction:** Uses current indicators to predict next close

## 📊 Technical Details

**Model Architecture:**
```python
model = keras.Sequential([
    layers.Dense(1, input_shape=(19,), activation='linear')
])
```

**Training Configuration:**
- Optimizer: Adam
- Loss: Mean Squared Error
- Epochs: 500
- Batch Size: 32
- Validation Split: 10%

## 🎯 Results Analysis

**Why It Works:**
- **Technical indicators capture market patterns**
- **5 years of data provides robust training**
- **Linear model prevents overfitting**
- **Multiple indicators reduce noise**

**Performance Metrics:**
- High R² scores (95%+) indicate strong predictive power
- Low RMSE relative to stock prices
- Correct directional predictions in real-world tests

## ⚠️ Disclaimer

**This model is for educational and research purposes only. Not financial advice.**

- Past performance doesn't guarantee future results
- Markets are inher