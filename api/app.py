# api/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import csv



app = FastAPI(title="Market Data API", version="0.1.0")

class TextIn(BaseModel):
    text: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/sentiment")
def sentiment(payload: TextIn):
   
    score = 0.0
    return {"text": payload.text, "score": score}

@app.get("/news/{symbol}")
def news(symbol: str):
  
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
