
from datetime import date, timedelta

from fastapi import FastAPI, Form, HTTPException
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
def predict_price(
    ticker: str = Form(...),
    from_date: str | None = Form(None),
    to_date: str | None = Form(None),
):
    """
    Predict tomorrow's closing price.

    Accepts:
      - ticker (required)
      - from_date (optional)
      - to_date (optional)

    If dates are not provided, defaults to:
      - to_date = today
      - from_date = 2 years ago
    """
    try:
        ticker = ticker.upper().strip()

        # Default date range if not supplied
        if to_date is None:
            to_date = date.today().isoformat()
        if from_date is None:
            from_date = (date.today() - timedelta(days=365 * 2)).isoformat()

        # Fetch + clean + build indicators
        # If your MarketDataService supports dates, this will use them.
        # If not, it falls back to ticker-only.
        try:
            features_df = market_service.get_features(
                ticker, from_date=from_date, to_date=to_date
            )
        except TypeError:
            features_df = market_service.get_features(ticker)

        # Train + predict
        predictor.train(features_df)
        predicted_close, current_price, change_pct = predictor.predict(features_df)

        # Ensure JSON-safe values
        predicted_close = float(predicted_close)
        current_price = float(current_price)
        change_pct = float(change_pct)

        return {
            "ticker": ticker,
            "current_price": round(current_price, 2),
            "predicted_close": round(predicted_close, 2),
            "change_pct": round(change_pct, 2),
            "direction": "UP" if predicted_close > current_price else "DOWN",
            "model": "Neural Regression (FeatureBuilder)",
            "from_date": from_date,
            "to_date": to_date,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------------------------------------
# FRONTEND (STATIC FILES)
# ------------------------------------------------------------
app.mount("/", StaticFiles(directory="frontEnd/public", html=True), name="static")
app.mount("/assets", StaticFiles(directory="frontEnd/assets"), name="assets")


# from fastapi import FastAPI, Form
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles

# from services.market import MarketDataService
# from main.predictions.predict_tomorrow import TomorrowPredictor


# # ------------------------------------------------------------
# # FastAPI app
# # ------------------------------------------------------------
# app = FastAPI(title="Market Prediction API", version="1.0.0")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # ------------------------------------------------------------
# # Singletons (kept in memory)
# # ------------------------------------------------------------
# market_service = MarketDataService()
# predictor = TomorrowPredictor()


# # ------------------------------------------------------------
# # Health check
# # ------------------------------------------------------------
# @app.get("/health")
# def health():
#     return {"status": "ok"}


# # ------------------------------------------------------------
# # PREDICT TOMORROW ENDPOINT
# # ------------------------------------------------------------
# @app.post("/predict")
# def predict_price(ticker: str = Form(...)):
#     """
#     Predict tomorrow's closing price.

#     Flow:
#     FastAPI
#       → MarketDataService (fetch + clean + indicators)
#       → TomorrowPredictor (train + predict)
#     """

#     try:
#         ticker = ticker.upper().strip()

#         # 1. Fetch + clean + build indicators
#         features_df = market_service.get_features(ticker)

#         # DEBUG: Show columns
#         print("FEATURE COLUMNS:", list(features_df.columns))

#         # 2. Train model
#         predictor.train(features_df)

#         # 3. Predict tomorrow
#         predicted_close, current_price, change_pct = predictor.predict(features_df)

#         return {
#             "ticker": ticker,
#             "current_price": float(round(current_price, 2)),
#             "predicted_close": float(round(predicted_close, 2)),
#             "change_pct": float(round(change_pct, 2)),
#             "direction": "UP" if predicted_close > current_price else "DOWN",
#             "model": "Neural Regression (FeatureBuilder)",
#         }

#     except Exception:
#         import traceback
#         traceback.print_exc()
#         raise


# # ------------------------------------------------------------
# # FRONTEND (STATIC FILES)
# # ------------------------------------------------------------
# app.mount("/", StaticFiles(directory="frontEnd/public", html=True), name="static")
# app.mount("/assets", StaticFiles(directory="frontEnd/assets"), name="assets")




# from fastapi import FastAPI, HTTPException, Form
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles

# from services.market import MarketDataService
# from main.predictions.predict_tomorrow import TomorrowPredictor


# # ------------------------------------------------------------
# # FastAPI app
# # ------------------------------------------------------------
# app = FastAPI(title="Market Prediction API", version="1.0.0")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # ------------------------------------------------------------
# # Singletons (kept in memory)
# # ------------------------------------------------------------
# market_service = MarketDataService()
# predictor = TomorrowPredictor()


# # ------------------------------------------------------------
# # Health check
# # ------------------------------------------------------------
# @app.get("/health")
# def health():
#     return {"status": "ok"}


# # ------------------------------------------------------------
# # PREDICT TOMORROW ENDPOINT
# # ------------------------------------------------------------
# @app.post("/predict")
# def predict_price(ticker: str = Form(...)):
#     """
#     Predict tomorrow's closing price.

#     Flow:
#     FastAPI
#       → MarketDataService (fetch + clean + indicators)
#       → TomorrowPredictor (train + predict)
#     """
#     try:
#         ticker = ticker.upper().strip()

#         # 1. Fetch + clean + build indicators
#         features_df = market_service.get_features(ticker)

#         # 2. Train model (per request for now)
#         predictor.train(features_df)

#         # 3. Predict tomorrow (UNPACK VALUES)
#         predicted_close, current_price, change_pct = predictor.predict(features_df)

#         return {
#             "ticker": ticker,
#             "current_price": float(round(current_price, 2)),
#             "predicted_close": float(round(predicted_close, 2)),
#             "change_pct": float(round(change_pct, 2)),
#             "direction": "UP" if predicted_close > current_price else "DOWN",
#             "model": "Neural Regression (FeatureBuilder)",
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # ------------------------------------------------------------
# # FRONTEND (STATIC FILES)
# # ------------------------------------------------------------
# # IMPORTANT:
# # - This MUST be at file scope
# # - NOT inside any function
# # - Directory must contain index.html
# # ------------------------------------------------------------
# #so when model trains but it does not show up in html or js is wrong check wiring(the way its mounted remind myself)
# #-------------------------------------------------------------

# app.mount("/", StaticFiles(directory="frontEnd/public", html=True), name="static")
# app.mount("/assets", StaticFiles(directory="frontEnd/assets"), name="assets")
