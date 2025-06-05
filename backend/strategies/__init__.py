from .base import Strategy
from .mean_reversion import MeanReversionStrategy
from .momentum import MomentumStrategy
from .trend_following import TrendFollowingStrategy

STRATEGY_MAP = {
    "mean_reversion": {
        "class": MeanReversionStrategy,
        "description": "Z-score 기반 평균회귀 전략",
    },
    "momentum": {
        "class": MomentumStrategy,
        "description": "단기 모멘텀을 활용한 전략",
    },
    "trend_following": {
        "class": TrendFollowingStrategy,
        "description": "단기/장기 이평선을 이용한 추세 추종",
    },
}
