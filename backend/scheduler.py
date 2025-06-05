import pandas as pd
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from .strategies.mean_reversion import MeanReversionStrategy
from . import models
from .database import get_db

scheduler = AsyncIOScheduler()


def run_strategy():
    db = next(get_db())
    prices = db.query(models.StockPrice).all()
    if not prices:
        return
    df = pd.DataFrame([(p.date, p.close) for p in prices], columns=["date", "close"]).set_index("date")
    strategy = MeanReversionStrategy()
    signals = strategy.generate_signals(df["close"])
    for dt, signal in signals.items():
        if signal != 0:
            log = models.TradeLog(symbol="TEST", action="BUY" if signal == 1 else "SELL", price=df.loc[dt, "close"], quantity=1)
            db.add(log)
    db.commit()


def schedule_jobs():
    scheduler.add_job(run_strategy, CronTrigger(day_of_week="mon", hour=9, minute=0))
    scheduler.add_job(run_strategy, CronTrigger(day_of_week="fri", hour=15, minute=0))
    scheduler.start()

