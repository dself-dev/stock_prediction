from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

# Import your pipeline
from services.market import MarketDataService

from main.predictions.predict_tomorrow import TomorrowPredictor


app = FastAPI()


# Serve frontend assets
app.mount("/assets", StaticFiles(directory="frontEnd/assets"), name="assets")


# Homepage
@app.get("/")
def home():
    return FileResponse("frontEnd/public/index.html")


# Prediction endpoint
@app.post("/predict")
def predict(
    ticker: str = Form(...),
    from_date: str = Form(...),
    to_date: str = Form(...)
):
    try:
        # 1. Get processed market data
        service = MarketDataService()
        df = service.get_features(ticker, start_date=from_date, end_date=to_date)

        # 2. Train model with both
        model = TomorrowPredictor(model_type='both')
        model.train(df)

        # 3. Predict (get dict with both)
        results = model.predict(df)

        # Average the two for single output (since frontend expects one)
        linear_pred, linear_curr, linear_pct = results['linear']
        nonlinear_pred, nonlinear_curr, nonlinear_pct = results['nonlinear']
        predicted_close = (linear_pred + nonlinear_pred) / 2
        current_price = linear_curr  # Same for both
        change_pct = (linear_pct + nonlinear_pct) / 2

        direction = "UP" if predicted_close > current_price else "DOWN"

        # 4. Return result
        return {
            "ticker": ticker,
            "predicted_close": round(predicted_close, 2),
            "current_price": round(current_price, 2),
            "change_pct": round(change_pct, 2),
            "direction": direction
        }

    except Exception as e:
        # Send readable error to frontend
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
# from fastapi import FastAPI, Form
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse, JSONResponse

# # Import your pipeline
# from services.market import MarketDataService

# from main.predictions.predict_tomorrow import TomorrowPredictor


# app = FastAPI()


# # Serve frontend assets
# app.mount("/assets", StaticFiles(directory="frontEnd/assets"), name="assets")


# # Homepage
# @app.get("/")
# def home():
#     return FileResponse("frontEnd/public/index.html")


# # Prediction endpoint
# @app.post("/predict")
# def predict(
#     ticker: str = Form(...),
#     from_date: str = Form(...),
#     to_date: str = Form(...)
# ):
#     try:
#         # 1. Get processed market data
#         service = MarketDataService()
#         df = service.get_features(ticker)

#         # 2. Train model
#         model = TomorrowPredictor()
#         model.train(df)

#         # 3. Predict
#         predicted_close, current_price, change_pct = model.predict(df)

#         direction = "UP" if predicted_close > current_price else "DOWN"

#         # 4. Return result
#         return {
#             "ticker": ticker,
#             "predicted_close": round(predicted_close, 2),
#             "current_price": round(current_price, 2),
#             "change_pct": round(change_pct, 2),
#             "direction": direction
#         }

#     except Exception as e:
#         # Send readable error to frontend
#         return JSONResponse(
#             status_code=500,
#             content={"error": str(e)}
#         )
# and should there be pytests for this stuff


# # from fastapi import FastAPI, Form
# # from fastapi.staticfiles import StaticFiles
# # from fastapi.responses import FileResponse, JSONResponse

# # # Import your pipeline
# # from services.market import MarketDataService

# # from main.predictions.predict_tomorrow import TomorrowPredictor


# # app = FastAPI()


# # # Serve frontend assets
# # app.mount("/assets", StaticFiles(directory="frontEnd/assets"), name="assets")


# # # Homepage
# # @app.get("/")
# # def home():
# #     return FileResponse("frontEnd/public/index.html")


# # # Prediction endpoint
# # @app.post("/predict")
# # def predict(
# #     ticker: str = Form(...),
# #     from_date: str = Form(...),
# #     to_date: str = Form(...)
# # ):
# #     try:
# #         # 1. Get processed market data
# #         service = MarketDataService()
# #         df = service.get_features(ticker)

# #         # 2. Train model
# #         model = TomorrowPredictor()
# #         model.train(df)

# #         # 3. Predict
# #         predicted_close, current_price, change_pct = model.predict(df)

# #         direction = "UP" if predicted_close > current_price else "DOWN"

# #         # 4. Return result
# #         return {
# #             "ticker": ticker,
# #             "predicted_close": round(predicted_close, 2),
# #             "current_price": round(current_price, 2),
# #             "change_pct": round(change_pct, 2),
# #             "direction": direction
# #         }

# #     except Exception as e:
# #         # Send readable error to frontend
# #         return JSONResponse(
# #             status_code=500,
# #             content={"error": str(e)}
# #         )
