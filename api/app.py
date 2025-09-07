# api/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import csv

# If you have functions in sentiment1.py or main/main.py, import them here:
# from sentiment1 import analyze_text   # example
# from main.main import run_pipeline     # example

app = FastAPI(title="Market Data API", version="0.1.0")

class TextIn(BaseModel):
    text: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/sentiment")
def sentiment(payload: TextIn):
    # swap this stub with your real function call
    # score = analyze_text(payload.text)
    score = 0.0
    return {"text": payload.text, "score": score}

@app.get("/news/{symbol}")
def news(symbol: str):
    """
    Returns rows from a CSV like scraped_news/news_AAPL.csv
    Adjust the path or filename pattern to match your repo.
    """
    candidates = [
        Path("scraped_news") / f"news_{symbol.upper()}.csv",
        Path("scraped_news") / f"{symbol.lower()}_news_*.csv",  # optional pattern
    ]
    # Pick the first existing file
    csv_path = next((p for p in candidates if p.exists()), None)
    if not csv_path:
        raise HTTPException(status_code=404, detail=f"No CSV found for {symbol}")

    rows = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return {"symbol": symbol.upper(), "count": len(rows), "items": rows[:100]}
