import pandas as pd
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from .strategies.mean_reversion import MeanReversionStrategy
from . import models
from .database import get_db
from .openai_client import generate_weekly_report


scheduler = AsyncIOScheduler()


def run_strategy():
    db = next(get_db())
    prices = db.query(models.StockPrice).all()
    if not prices:
        return
    df = pd.DataFrame([(p.date, p.close) for p in prices], columns=["date", "close"]).set_index("date")
    strategy = MeanReversionStrategy()
    signals = strategy.generate_signals(df["close"])
    trades = []
    for dt, signal in signals.items():
        if signal != 0:
            action = "BUY" if signal == 1 else "SELL"
            log = models.TradeLog(symbol="TEST", action=action, price=df.loc[dt, "close"], quantity=1)
            db.add(log)
            trades.append({"time": dt.isoformat(), "action": action})
    db.commit()

    if trades:
        report_text = generate_weekly_report("TEST", {"trade_count": len(trades)})
        report = models.WeeklyReport(symbol="TEST", content=report_text)
        db.add(report)
        db.commit()


def schedule_jobs():
    scheduler.add_job(run_strategy, CronTrigger(day_of_week="mon", hour=9, minute=0))
    scheduler.add_job(run_strategy, CronTrigger(day_of_week="fri", hour=15, minute=0))
    scheduler.start()

