import pandas as pd
from .base import Strategy

class TrendFollowingStrategy(Strategy):
    """단기/장기 이동평균을 이용한 추세 추종 전략"""

    def __init__(self, short_window: int = 5, long_window: int = 20):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, prices: pd.Series) -> pd.Series:
        if prices.empty or self.long_window <= self.short_window:
            return pd.Series(dtype=int)

        short_ma = prices.rolling(self.short_window).mean()
        long_ma = prices.rolling(self.long_window).mean()
        signals = pd.Series(index=prices.index, data=0)
        signals[short_ma > long_ma] = 1
        signals[short_ma < long_ma] = -1
        return signals
