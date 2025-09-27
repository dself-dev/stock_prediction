# # api/app.py
# from fastapi import FastAPI, HTTPException, Depends
# from pydantic import BaseModel
# from pathlib import Path
# import csv
# from passlib.context import CryptContext
# from sqlalchemy.orm import Session
# from .database import SessionLocal, User  # Adjust import based on your folder
# from .models import UserCreate  # Import your Pydantic model
# from fastapi.staticfiles import StaticFiles

# app = FastAPI(title="Market Data API", version="0.1.0")



# # Serve your front-end folders/files
# app.mount("/", StaticFiles(directory="frontEnd/public", html=True), name="static")

# # Serve CSS/JS/assets
# app.mount("/assets", StaticFiles(directory="frontEnd/assets"), name="assets")

# class TextIn(BaseModel):
#     text: str

# # Password hashing
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # Dependency to get DB session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.get("/health")
# def health():
#     return {"status": "ok"}

# @app.post("/sentiment")
# def sentiment(payload: TextIn):
#     score = 0.0
#     return {"text": payload.text, "score": score}

# @app.get("/news/{symbol}")
# def news(symbol: str):
#     candidates = [
#         Path("scraped_news") / f"news_{symbol.upper()}.csv",
#         Path("scraped_news") / f"{symbol.lower()}_news_*.csv",  # optional pattern
#     ]
#     csv_path = next((p for p in candidates if p.exists()), None)
#     if not csv_path:
#         raise HTTPException(status_code=404, detail=f"No CSV found for {symbol}")

#     rows = []
#     with open(csv_path, newline="", encoding="utf-8") as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             rows.append(row)
#     return {"symbol": symbol.upper(), "count": len(rows), "items": rows[:100]}

# @app.post("/register")
# def register(user: UserCreate, db: Session = Depends(get_db)):
#     # Check if username or email already exists
#     existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Username or email already exists")
    
#     # Hash password
#     hashed_password = pwd_context.hash(user.password)
    
#     # Create new user
#     new_user = User(
#         username=user.username,
#         email=user.email,
#         country=user.country,
#         state=user.state,
#         hashed_password=hashed_password
#     )
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return {"message": "User created successfully"}

#version 2 below
# api/app.py
# 

#version 3
import os
import csv
from pathlib import Path
from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import BaseModel

from .database import SessionLocal, User        # SQLAlchemy model
from .models import UserCreate                  # Pydantic schema


# ------------------------------------------------------------
#  FastAPI app
# ------------------------------------------------------------
app = FastAPI(title="Market Data API", version="0.1.0")

# password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------------------------------------------------
#  API routes  (must come BEFORE mounting static files)
# ------------------------------------------------------------
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
        Path("scraped_news") / f"{symbol.lower()}_news_*.csv",
    ]
    csv_path = next((p for p in candidates if p.exists()), None)
    if not csv_path:
        raise HTTPException(status_code=404, detail=f"No CSV found for {symbol}")

    rows = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return {"symbol": symbol.upper(), "count": len(rows), "items": rows[:100]}


@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    hashed_password = pwd_context.hash(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        country=user.country,
        state=user.state,
        hashed_password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}


# ------------------------------------------------------------
#  Mount static files  (do this LAST!)
# ------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "frontEnd", "assets")
PUBLIC_DIR = os.path.join(BASE_DIR, "frontEnd", "public")

app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")
app.mount("/", StaticFiles(directory=PUBLIC_DIR, html=True), name="static")
