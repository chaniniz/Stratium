import sys, pathlib; sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
import pandas as pd
from backend.strategies.momentum import MomentumStrategy
from backend.strategies.trend_following import TrendFollowingStrategy


def test_momentum_signals():
    prices = pd.Series([1, 1.1, 1.2, 1.3, 1.4], index=pd.date_range("2024-01-01", periods=5))
    strat = MomentumStrategy(window=2, threshold=0.05)
    signals = strat.generate_signals(prices)
    assert 1 in signals.values or -1 in signals.values


def test_trend_following_signals():
    prices = pd.Series([1, 1, 2, 2, 3, 3], index=pd.date_range("2024-01-01", periods=6))
    strat = TrendFollowingStrategy(short_window=2, long_window=3)
    signals = strat.generate_signals(prices)
    assert 1 in signals.values or -1 in signals.values
