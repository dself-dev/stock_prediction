# ------------------------------------------------------------------
# NOTE ON AUTHENTICATION
# ------------------------------------------------------------------
# This project includes authentication logic (JWT-based) for
# production-style security. However, the /predict endpoint is
# intentionally left open for demonstration purposes so that
# recruiters and reviewers  or anyone that want to try it out
# can run the application immediately
# without account setup.
#
# In a production deployment, this endpoint would be protected
# via dependency injection (e.g., Depends(get_current_user)) and
# token validation middleware to prevent unauthorized usage.
#
# This design decision balances demo usability with awareness of
# proper backend security practices.

#------------------------------------------------------------------
# 
# ------------------------------------------------------------------


from datetime import date, timedelta
from pathlib import Path
import traceback  # NEW - for printing full error details

from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from services.market import MarketDataService
from main.predictions.predict_tomorrow import TomorrowPredictor
from main.classify_direction import DirectionClassifier  # NEW IMPORT


# ------------------------------------------------------------
# BASE DIRECTORY (ABSOLUTE PATH FIX)
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

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
    """

    try:
        ticker = ticker.upper().strip()

        # Default date range if not supplied
        if to_date is None:
            to_date = date.today().isoformat()

        if from_date is None:
            from_date = (date.today() - timedelta(days=365 * 2)).isoformat()

        # Fetch + clean + build indicators
        try:
            features_df = market_service.get_features(
                ticker,
                from_date=from_date,
                to_date=to_date
            )
        except TypeError:
            features_df = market_service.get_features(ticker)

        # Train + predict price with 'both' (FIXED unpacking for dict return)
        predictor = TomorrowPredictor(model_type='both')
        predictor.train(features_df)
        results = predictor.predict(features_df)
        linear_pred, linear_curr, linear_pct = results['linear']
        nonlinear_pred, nonlinear_curr, nonlinear_pct = results['nonlinear']
        predicted_close = (linear_pred + nonlinear_pred) / 2
        current_price = linear_curr
        change_pct = (linear_pct + nonlinear_pct) / 2

        # NEW: Train + predict direction classifier
        classifier = DirectionClassifier()
        classifier.train(features_df)
        class_direction, prob = classifier.predict_direction(features_df)
        direction_prob = round(prob * 100, 2) if class_direction == "UP" else round((1 - prob) * 100, 2)
        direction_conf = f"{direction_prob}%"

        return {
            "ticker": ticker,
            "current_price": round(float(current_price), 2),
            "predicted_close": round(float(predicted_close), 2),
            "change_pct": round(float(change_pct), 2),
            "direction": "UP" if predicted_close > current_price else "DOWN",
            "model": "Neural Regression (FeatureBuilder)",
            "from_date": from_date,
            "to_date": to_date,
            "direction_conf": direction_conf  # NEW FIELD
        }

    except Exception as e:
        print(traceback.format_exc()) # NEW - prints full error to terminal for debugging
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------------------------------------
# STATIC FILES (ABSOLUTE PATH — FIXED)
# ------------------------------------------------------------
app.mount(
    "/assets",
    StaticFiles(directory=BASE_DIR / "frontEnd" / "assets"),
    name="assets"
)

app.mount(
    "/",
    StaticFiles(directory=BASE_DIR / "frontEnd" / "public", html=True),
    name="static"
)






#<---------------adding classify---------------->

# ------------------------------------------------------------------
# NOTE ON AUTHENTICATION
# ------------------------------------------------------------------
# This project includes authentication logic (JWT-based) for
# production-style security. However, the /predict endpoint is
# intentionally left open for demonstration purposes so that
# recruiters and reviewers  or anyone that want to try it out
# can run the application immediately
# without account setup.
#
# In a production deployment, this endpoint would be protected
# via dependency injection (e.g., Depends(get_current_user)) and
# token validation middleware to prevent unauthorized usage.
#
# This design decision balances demo usability with awareness of
# proper backend security practices.

#------------------------------------------------------------------
# 
# ------------------------------------------------------------------


# from datetime import date, timedelta
# from pathlib import Path

# from fastapi import FastAPI, Form, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles

# from services.market import MarketDataService
# from main.predictions.predict_tomorrow import TomorrowPredictor
# from main.classify_direction import DirectionClassifier  # NEW IMPORT


# # ------------------------------------------------------------
# # BASE DIRECTORY 
# # ------------------------------------------------------------
# BASE_DIR = Path(__file__).resolve().parent.parent

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
# def predict_price(
#     ticker: str = Form(...),
#     from_date: str | None = Form(None),
#     to_date: str | None = Form(None),
# ):
#     """
#     Predict tomorrow's closing price.
#     """

#     try:
#         ticker = ticker.upper().strip()

#         # Default date range if not supplied
#         if to_date is None:
#             to_date = date.today().isoformat()

#         if from_date is None:
#             from_date = (date.today() - timedelta(days=365 * 2)).isoformat()

#         # Fetch + clean + build indicators
#         try:
#             features_df = market_service.get_features(
#                 ticker,
#                 from_date=from_date,
#                 to_date=to_date
#             )
#         except TypeError:
#             features_df = market_service.get_features(ticker)

#         # Train + predict price
#         predictor.train(features_df)
#         predicted_close, current_price, change_pct = predictor.predict(features_df)

#         # NEW: Train + predict direction classifier
#         classifier = DirectionClassifier()
#         classifier.train(features_df)
#         class_direction, prob = classifier.predict_direction(features_df)
#         direction_prob = round(prob * 100, 2) if class_direction == "UP" else round((1 - prob) * 100, 2)
#         direction_conf = f"{direction_prob}%"

#         return {
#             "ticker": ticker,
#             "current_price": round(float(current_price), 2),
#             "predicted_close": round(float(predicted_close), 2),
#             "change_pct": round(float(change_pct), 2),
#             "direction": "UP" if predicted_close > current_price else "DOWN",
#             "model": "Neural Regression (FeatureBuilder)",
#             "from_date": from_date,
#             "to_date": to_date,
#             "direction_conf": direction_conf  # NEW FIELD
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # ------------------------------------------------------------
# # STATIC FILES (ABSOLUTE PATH — FIXED)
# # ------------------------------------------------------------
# app.mount(
#     "/assets",
#     StaticFiles(directory=BASE_DIR / "frontEnd" / "assets"),
#     name="assets"
# )

# app.mount(
#     "/",
#     StaticFiles(directory=BASE_DIR / "frontEnd" / "public", html=True),
#     name="static"
# )


#below works...............


# # ------------------------------------------------------------------
# # NOTE ON AUTHENTICATION
# # ------------------------------------------------------------------
# # This project includes authentication logic (JWT-based) for
# # production-style security. However, the /predict endpoint is
# # intentionally left open for demonstration purposes so that
# # recruiters and reviewers  or anyone that want to try it out
# # can run the application immediately
# # without account setup.
# #
# # In a production deployment, this endpoint would be protected
# # via dependency injection (e.g., Depends(get_current_user)) and
# # token validation middleware to prevent unauthorized usage.
# #
# # This design decision balances demo usability with awareness of
# # proper backend security practices.

# #------------------------------------------------------------------
# # 
# # ------------------------------------------------------------------


# from datetime import date, timedelta
# from pathlib import Path

# from fastapi import FastAPI, Form, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles

# from services.market import MarketDataService
# from main.predictions.predict_tomorrow import TomorrowPredictor


# # ------------------------------------------------------------
# # BASE DIRECTORY (ABSOLUTE PATH FIX)
# # ------------------------------------------------------------
# BASE_DIR = Path(__file__).resolve().parent.parent

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
# def predict_price(
#     ticker: str = Form(...),
#     from_date: str | None = Form(None),
#     to_date: str | None = Form(None),
# ):
#     """
#     Predict tomorrow's closing price.
#     """

#     try:
#         ticker = ticker.upper().strip()

#         # Default date range if not supplied
#         if to_date is None:
#             to_date = date.today().isoformat()

#         if from_date is None:
#             from_date = (date.today() - timedelta(days=365 * 2)).isoformat()

#         # Fetch + clean + build indicators
#         try:
#             features_df = market_service.get_features(
#                 ticker,
#                 from_date=from_date,
#                 to_date=to_date
#             )
#         except TypeError:
#             features_df = market_service.get_features(ticker)

#         # Train + predict
#         predictor.train(features_df)
#         predicted_close, current_price, change_pct = predictor.predict(features_df)

#         return {
#             "ticker": ticker,
#             "current_price": round(float(current_price), 2),
#             "predicted_close": round(float(predicted_close), 2),
#             "change_pct": round(float(change_pct), 2),
#             "direction": "UP" if predicted_close > current_price else "DOWN",
#             "model": "Neural Regression (FeatureBuilder)",
#             "from_date": from_date,
#             "to_date": to_date,
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # ------------------------------------------------------------
# # STATIC FILES (ABSOLUTE PATH — FIXED)
# # ------------------------------------------------------------
# app.mount(
#     "/assets",
#     StaticFiles(directory=BASE_DIR / "frontEnd" / "assets"),
#     name="assets"
# )

# app.mount(
#     "/",
#     StaticFiles(directory=BASE_DIR / "frontEnd" / "public", html=True),
#     name="static"
# )







