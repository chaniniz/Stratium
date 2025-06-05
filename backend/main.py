from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import engine, get_db
from .models import Base
from . import models
from .auth import (
    login_for_access_token,
    get_current_user,
    get_password_hash,
)
from .scheduler import schedule_jobs


app = FastAPI(title="Trading API")


@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    schedule_jobs()


@app.post("/token")
async def login(form_data: Depends(login_for_access_token)):
    return form_data


@app.get("/prices/{symbol}")
async def get_prices(symbol: str, db: Session = Depends(get_db)):
    prices = (
        db.query(models.StockPrice)
        .filter(models.StockPrice.symbol == symbol)
        .order_by(models.StockPrice.date)
        .all()
    )
    if not prices:
        raise HTTPException(status_code=404, detail="symbol not found")
    return {"symbol": symbol, "prices": [{"date": p.date.isoformat(), "close": p.close} for p in prices]}


@app.post("/trade/{symbol}")
async def trade(symbol: str, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    log = models.TradeLog(user_id=user.id, symbol=symbol, action="BUY", price=0.0, quantity=1)
    db.add(log)
    db.commit()
    db.refresh(log)
    return {"trade_id": log.id, "status": "logged"}


@app.get("/trade/history")
async def trade_history(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    logs = (
        db.query(models.TradeLog)
        .filter(models.TradeLog.user_id == user.id)
        .order_by(models.TradeLog.created_at.desc())
        .all()
    )
    return [
        {
            "symbol": l.symbol,
            "action": l.action,
            "price": l.price,
            "qty": l.quantity,
            "time": l.created_at.isoformat(),
        }
        for l in logs
    ]


@app.post("/users")
async def create_user(username: str, password: str, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.username == username).first():
        raise HTTPException(status_code=400, detail="username taken")
    user = models.User(username=username, hashed_password=get_password_hash(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username}


@app.get("/watchlist")
async def get_watchlist(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    items = db.query(models.Watchlist).filter(models.Watchlist.user_id == user.id).all()
    return [w.symbol for w in items]


@app.post("/watchlist")
async def add_watchlist(symbol: str, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = models.Watchlist(user_id=user.id, symbol=symbol)
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"id": item.id, "symbol": item.symbol}


@app.delete("/watchlist/{symbol}")
async def remove_watchlist(symbol: str, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = (
        db.query(models.Watchlist)
        .filter(models.Watchlist.user_id == user.id, models.Watchlist.symbol == symbol)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="not found")
    db.delete(item)
    db.commit()
    return {"status": "deleted"}

