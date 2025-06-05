from abc import ABC, abstractmethod
import pandas as pd

class Strategy(ABC):
    """전략 인터페이스: 모든 전략은 generate_signals 메소드를 구현해야 한다."""

    @abstractmethod
    def generate_signals(self, prices: pd.Series) -> pd.Series:
        """시계열 데이터로부터 매수/매도(+1/-1) 신호를 생성한다."""
        raise NotImplementedError
