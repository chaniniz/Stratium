import pandas as pd
from .base import Strategy

class MomentumStrategy(Strategy):
    """단기 모멘텀을 이용한 매매 전략"""

    def __init__(self, window: int = 20, threshold: float = 0.05):
        self.window = window
        self.threshold = threshold

    def generate_signals(self, prices: pd.Series) -> pd.Series:
        if prices.empty:
            return pd.Series(dtype=int)

        ma = prices.rolling(self.window).mean()
        pct_change = prices.pct_change()
        signals = pd.Series(index=prices.index, data=0)
        signals[(prices > ma) & (pct_change > self.threshold)] = 1
        signals[(prices < ma) & (pct_change < -self.threshold)] = -1
        return signals
