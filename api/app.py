# from datetime import date, timedelta
# from pathlib import Path
# import traceback

# from fastapi import FastAPI, Form, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles

# from services.market import MarketDataService
# from main.predictions.predict_tomorrow import TomorrowPredictor
# from main.classify_direction import DirectionClassifier


# # ------------------------------------------------------------------
# # Authentication note
# # ------------------------------------------------------------------
# # This module acts as the API composition layer for the market
# # prediction application.
# #
# # The project includes JWT-based authentication in the broader
# # codebase, but the /predict endpoint is intentionally left open in
# # this demo build so reviewers can test the application immediately
# # without creating an account.
# #
# # In a production deployment, this route would typically be protected
# # through dependency injection and token validation to restrict access.
# # This tradeoff was intentional: prioritize demo accessibility while
# # still designing with production security practices in mind.


# # ------------------------------------------------------------------
# # Base directory
# # ------------------------------------------------------------------
# # Resolve paths relative to the project root so static frontend assets
# # can be mounted reliably across environments.
# BASE_DIR = Path(__file__).resolve().parent.parent


# # ------------------------------------------------------------------
# # FastAPI application setup
# # ------------------------------------------------------------------
# app = FastAPI(title="Market Prediction API", version="1.0.0")

# # CORS is fully open in this demo configuration to simplify frontend
# # integration and testing from different origins.
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # ------------------------------------------------------------------
# # Shared services
# # ------------------------------------------------------------------
# # Keep reusable services in memory so they do not need to be rebuilt
# # on every request.
# market_service = MarketDataService()


# # ------------------------------------------------------------------
# # Health check
# # ------------------------------------------------------------------
# @app.get("/health")
# def health():
#     """Simple endpoint for confirming the API is running."""
#     return {"status": "ok"}


# # ------------------------------------------------------------------
# # Prediction endpoint
# # ------------------------------------------------------------------
# @app.post("/predict")
# def predict_price(
#     ticker: str = Form(...),
#     from_date: str | None = Form(None),
#     to_date: str | None = Form(None),
# ):
#     """
#     Generate a next-day market prediction for the requested ticker.

#     The endpoint:
#     - normalizes request input
#     - retrieves engineered market features
#     - trains regression models for next-close prediction
#     - runs a direction classifier for confidence scoring
#     - returns the aggregated forecast as JSON
#     """
#     try:
#         ticker = ticker.upper().strip()

#         # Use a default two-year historical window when dates are not supplied.
#         if to_date is None:
#             to_date = date.today().isoformat()

#         if from_date is None:
#             from_date = (date.today() - timedelta(days=365 * 2)).isoformat()

#         # Retrieve feature-engineered market data for the requested period.
#         # Fallback to the legacy method signature if needed.
#         try:
#             features_df = market_service.get_features(
#                 ticker,
#                 from_date=from_date,
#                 to_date=to_date
#             )
#         except TypeError:
#             features_df = market_service.get_features(ticker)

#         # Train both regression models and combine their outputs into a
#         # single predicted close.
#         predictor = TomorrowPredictor(model_type="both")
#         predictor.train(features_df)
#         results = predictor.predict(features_df)

#         linear_pred, linear_curr, linear_pct = results["linear"]
#         nonlinear_pred, nonlinear_curr, nonlinear_pct = results["nonlinear"]

#         predicted_close = (linear_pred + nonlinear_pred) / 2
#         current_price = linear_curr
#         change_pct = (linear_pct + nonlinear_pct) / 2

#         # Run a separate direction classifier to estimate directional
#         # confidence for the next session.
#         classifier = DirectionClassifier()
#         classifier.train(features_df)
#         class_direction, prob = classifier.predict_direction(features_df)

#         direction_prob = (
#             round(prob * 100, 2)
#             if class_direction == "UP"
#             else round((1 - prob) * 100, 2)
#         )
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
#             "direction_conf": direction_conf,
#         }

#     except Exception as e:
#         # Print the full traceback to support local debugging.
#         print(traceback.format_exc())
#         raise HTTPException(status_code=500, detail=str(e))


# # ------------------------------------------------------------------
# # Static frontend hosting
# # ------------------------------------------------------------------
# # Mount the built frontend so the API and UI can be served together in
# # a single deployment for demo purposes.
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


# # # ------------------------------------------------------------------
# # # NOTE ON AUTHENTICATION
# # # ------------------------------------------------------------------
# # #This module is the API orchestration layer for my market prediction app. It exposes a prediction endpoint, normalizes request parameters, retrieves engineered market features, trains regression models to estimate the next closing price, uses a separate classifier for directional confidence, and returns the aggregated forecast as JSON. It also serves the frontend bundle for a single-deploy demo experience.
# # # This project includes authentication logic (JWT-based) for
# # # production-style security. However, the /predict endpoint is
# # # intentionally left open for demonstration purposes so that
# # # recruiters and reviewers  or anyone that want to try it out
# # # can run the application immediately
# # # without account setup.
# # #
# # # In a production deployment, this endpoint would be protected
# # # via dependency injection (e.g., Depends(get_current_user)) and
# # # token validation middleware to prevent unauthorized usage.
# # #
# # # This design decision balances demo usability with awareness of
# # # proper backend security practices.

# # #------------------------------------------------------------------
# # # 
# # # ------------------------------------------------------------------




from datetime import date, timedelta
from pathlib import Path
import traceback
import logging

from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from services.market import MarketDataService
from main.predictions.predict_tomorrow import TomorrowPredictor
from main.classify_direction import DirectionClassifier


# ------------------------------------------------------------------
# Authentication note
# ------------------------------------------------------------------
# This module acts as the API composition layer for the market
# prediction application.
#
# The project includes JWT-based authentication in the broader
# codebase, but the /predict endpoint is intentionally left open in
# this demo build so reviewers can test the application immediately
# without creating an account.
#
# In a production deployment, this route would typically be protected
# through dependency injection and token validation to restrict access.
# This tradeoff was intentional: prioritize demo accessibility while
# still designing with production security practices in mind.


# ------------------------------------------------------------------
# Logging setup
# ------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ------------------------------------------------------------------
# Base directory
# ------------------------------------------------------------------
# Resolve paths relative to the project root so static frontend assets
# can be mounted reliably across environments.
BASE_DIR = Path(__file__).resolve().parent.parent


# ------------------------------------------------------------------
# FastAPI application setup
# ------------------------------------------------------------------
app = FastAPI(title="Market Prediction API", version="1.0.0")

# CORS is fully open in this demo configuration to simplify frontend
# integration and testing from different origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------------------------------------------------
# Shared services
# ------------------------------------------------------------------
# Keep reusable services in memory so they do not need to be rebuilt
# on every request.
market_service = MarketDataService()


# ------------------------------------------------------------------
# Health check
# ------------------------------------------------------------------
@app.get("/health")
def health():
    """Simple endpoint for confirming the API is running."""
    logger.info("Health check requested")
    return {"status": "ok"}


# ------------------------------------------------------------------
# Prediction endpoint
# ------------------------------------------------------------------
@app.post("/predict")
def predict_price(
    ticker: str = Form(...),
    from_date: str | None = Form(None),
    to_date: str | None = Form(None),
):
    """
    Generate a next-day market prediction for the requested ticker.

    The endpoint:
    - normalizes request input
    - retrieves engineered market features
    - trains regression models for next-close prediction
    - runs a direction classifier for confidence scoring
    - returns the aggregated forecast as JSON
    """
    try:
        ticker = ticker.upper().strip()
        logger.info(f"Prediction requested for ticker={ticker}, from_date={from_date}, to_date={to_date}")

        # Use a default two-year historical window when dates are not supplied.
        if to_date is None:
            to_date = date.today().isoformat()

        if from_date is None:
            from_date = (date.today() - timedelta(days=365 * 2)).isoformat()

        # Retrieve feature-engineered market data for the requested period.
        # Fallback to the legacy method signature if needed.
        try:
            features_df = market_service.get_features(
                ticker,
                from_date=from_date,
                to_date=to_date
            )
        except TypeError:
            features_df = market_service.get_features(ticker)

        # Train both regression models and combine their outputs into a
        # single predicted close.
        predictor = TomorrowPredictor(model_type="both")
        predictor.train(features_df)
        results = predictor.predict(features_df)

        linear_pred, linear_curr, linear_pct = results["linear"]
        nonlinear_pred, nonlinear_curr, nonlinear_pct = results["nonlinear"]

        predicted_close = (linear_pred + nonlinear_pred) / 2
        current_price = linear_curr
        change_pct = (linear_pct + nonlinear_pct) / 2

        # Run a separate direction classifier to estimate directional
        # confidence for the next session.
        classifier = DirectionClassifier()
        classifier.train(features_df)
        class_direction, prob = classifier.predict_direction(features_df)

        direction_prob = (
            round(prob * 100, 2)
            if class_direction == "UP"
            else round((1 - prob) * 100, 2)
        )
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
            "direction_conf": direction_conf,
        }

    except Exception as e:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------------------------------------------
# Static frontend hosting
# ------------------------------------------------------------------
# Mount the built frontend so the API and UI can be served together in
# a single deployment for demo purposes.
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


# # ------------------------------------------------------------------
# # NOTE ON AUTHENTICATION
# # ------------------------------------------------------------------
# #This module is the API orchestration layer for my market prediction app. It exposes a prediction endpoint, normalizes request parameters, retrieves engineered market features, trains regression models to estimate the next closing price, uses a separate classifier for directional confidence, and returns the aggregated forecast as JSON. It also serves the frontend bundle for a single-deploy demo experience.
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



