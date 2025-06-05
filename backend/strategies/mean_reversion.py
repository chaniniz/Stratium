import pandas as pd
from .base import Strategy

class MeanReversionStrategy(Strategy):
    """Z-score 기반 평균회귀 매매 전략"""

    def __init__(self, window: int = 20, z_threshold: float = 2.0,
                 stop_loss: float = -0.05, take_profit: float = 0.11):
        self.window = window
        self.z_threshold = z_threshold
        self.stop_loss = stop_loss
        self.take_profit = take_profit

    def generate_signals(self, prices: pd.Series) -> pd.Series:
        if prices.empty:
            return pd.Series(dtype=int)

        rolling_mean = prices.rolling(self.window).mean()
        rolling_std = prices.rolling(self.window).std()
        zscore = (prices - rolling_mean) / rolling_std
        signals = pd.Series(index=prices.index, data=0)
        signals[zscore < -self.z_threshold] = 1   # 매수
        signals[zscore > self.z_threshold] = -1  # 매도
        return signals
