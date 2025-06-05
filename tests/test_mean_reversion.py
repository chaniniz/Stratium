import sys, pathlib; sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
import pandas as pd
from backend.strategies.mean_reversion import MeanReversionStrategy


def test_generate_signals():
    prices = pd.Series([1, 1, 1, 1, 5, 1, 1, 1],
                       index=pd.date_range("2024-01-01", periods=8))
    strat = MeanReversionStrategy(window=3, z_threshold=1)
    signals = strat.generate_signals(prices)
    assert 1 in signals.values or -1 in signals.values
