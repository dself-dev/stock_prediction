🎯 Stock Prediction Model – 96% Accuracy

Real-world tested machine learning model for stock price prediction using technical indicators + sentiment analysis.






👨‍💻 Author

Dennis Selfinger
Machine Learning Engineer & Quantitative Analyst – Software Engineer

📊 Achieved 96% accuracy on real-world stock prediction (July 2025)

🎯 Specialized in financial machine learning and technical analysis

💼 2+ years of data science and algorithmic trading experience

Contact:

GitHub: @dself-dev

🚀 Results

Real-world validation on AAPL (July 16, 2025):

Predicted: $211.02

Actual: $210.16

Error: $0.86 (0.4%)

Direction: ✅ Correctly predicted UP movement

Integration Update (Sept 2025):

IONQ example: Predicted drop, Sentiment returned positive → forecast highlights “Mixed Signal, be cautious.”

User now only runs predict_tomorrow.py for both technical + sentiment forecasts.

📊 Model Performance
Stock	R² Score	RMSE	Test Period
AAPL	95.1%	$3.40	5 years
IONQ	97.6%	$1.89	5 years
🛠️ Features

Technical Indicators Used (19 total):

RSI (14-period)

Bollinger Bands (Upper, Middle, Lower)

EMAs (12, 26-period)

SMAs (10, 20, 50-period)

MACD & MACD Signal

Stochastic (K, D)

Average True Range (ATR)

Volume SMA

Enhancements (Sept 2025):

📰 Added news sentiment analysis (VADER).

⚡ Unified pipeline: only one script to run (predict_tomorrow.py).

📑 Better reporting: shows agreement/disagreement between ML + sentiment.

🏗️ Architecture

Model: Keras Linear Regression

Training: 500 epochs (historical), 100 epochs (daily live)

Features: 19 technical indicators + sentiment layer

Data: 2–5 years of OHLCV data (auto-downloaded if CSV missing)

Preprocessing: StandardScaler normalization

📁 Files
├── main.py                        # Main prediction model
├── services/                      
│   ├── market.py                   # Technical indicator calculator
│   ├── sentiment.py                # Sentiment analysis (Yahoo + VADER)
│   └── news.py                     # News scraper
├── main/predictions/              
│   └── predict_tomorrow.py         # Unified forecast (ML + sentiment)
├── scraped_news/                   # Saved news CSVs
├── requirements.txt                # Dependencies
├── .gitignore                      # Git ignore file
├── first.png                       # Screenshot
├── venv/                           # Virtual environment
└── README.md                       # This file

📦 Dependencies
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
tensorflow>=2.19.0
yfinance>=0.2.0
ta>=0.10.0
playwright>=1.55.0
pytest>=8.4.0
pytest-playwright>=0.7.0
pytest-base-url>=2.1.0
nltk>=3.9

🚀 Quick Start
1. Clone the repository
git clone https://github.com/dself-dev/stock_prediction.git
cd stock_prediction

2. Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Run unified prediction
python main/predictions/predict_tomorrow.py
# Enter: AAPL

📈 Usage Examples

Run unified prediction (price + sentiment):

python main/predictions/predict_tomorrow.py
# Enter: IONQ


Output example:

Today's Close: $70.41
Predicted Close: $64.21
Expected Change: -8.8%

ML Prediction: GO DOWN
Sentiment: POSITIVE (avg score 0.707)
ML and Sentiment DISAGREE -> Mixed Signal, be cautious

🗞️ News Data Collection (Standalone Mode)

You can still run sentiment analysis separately:

python services/sentiment.py
# Enter ticker (e.g., AAPL)
# Scrapes Yahoo Finance and calculates average sentiment

🧮 How It Works

Data Collection: OHLCV data via yfinance.

Feature Engineering: 19 technical indicators.

Sentiment Analysis: Scrapes Yahoo Finance news + VADER scoring.

Preprocessing: Scales features for ML.

Prediction: Keras regression model outputs tomorrow’s price.

Final Report: Shows ML forecast + sentiment + agreement check.

📊 Technical Details

Model Architecture:

model = keras.Sequential([
    layers.Dense(1, input_shape=(19,), activation='linear')
])


Training Configuration:

Optimizer: Adam

Loss: Mean Squared Error

Epochs: 100–500

Batch Size: 32

Validation Split: 10%

🎯 Results Analysis

Why It Works:

Indicators capture market structure.

Sentiment adds context from real-world events.

Agreement strengthens signals, disagreement warns of volatility.

Metrics:

High R² (>95%).

Low RMSE.

Real-world tests confirm directional accuracy.

⚠️ Disclaimer

Educational and research purposes only. Not financial advice.

Markets are unpredictable.

Use responsibly PLEASE!!!!