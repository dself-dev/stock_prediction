from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from services.market import MarketDataService
from main.predictions.predict_tomorrow import TomorrowPredictor


# ------------------------------------------------------------
# FastAPI app
# ------------------------------------------------------------
app = FastAPI(title="Market Prediction API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------------------------------------------
# Singletons (kept in memory)
# ------------------------------------------------------------
market_service = MarketDataService()
predictor = TomorrowPredictor()


# ------------------------------------------------------------
# Health check
# ------------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# ------------------------------------------------------------
# PREDICT TOMORROW ENDPOINT
# ------------------------------------------------------------
@app.post("/predict")
def predict_price(ticker: str = Form(...)):
    """
    Predict tomorrow's closing price.

    Flow:
    FastAPI
      → MarketDataService (fetch + clean + indicators)
      → TomorrowPredictor (train + predict)
    """
    try:
        ticker = ticker.upper().strip()

        # 1. Fetch + clean + build indicators
        features_df = market_service.get_features(ticker)

        # 2. Train model (per request for now)
        predictor.train(features_df)

        # 3. Predict tomorrow (UNPACK VALUES)
        predicted_close, current_price, change_pct = predictor.predict(features_df)

        return {
            "ticker": ticker,
            "current_price": float(round(current_price, 2)),
            "predicted_close": float(round(predicted_close, 2)),
            "change_pct": float(round(change_pct, 2)),
            "direction": "UP" if predicted_close > current_price else "DOWN",
            "model": "Neural Regression (FeatureBuilder)",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------------------------------------
# FRONTEND (STATIC FILES)
# ------------------------------------------------------------
# IMPORTANT:
# - This MUST be at file scope
# - NOT inside any function
# - Directory must contain index.html
# ------------------------------------------------------------
#so when model trains but it does not show up in html or js is wrong check wiring(the way its mounted remind myself)
#-------------------------------------------------------------

app.mount("/", StaticFiles(directory="frontEnd/public", html=True), name="static")
app.mount("/assets", StaticFiles(directory="frontEnd/assets"), name="assets")
