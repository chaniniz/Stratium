from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import engine, get_db
from .models import Base
from . import models
from .auth import login_for_access_token, get_current_user
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

