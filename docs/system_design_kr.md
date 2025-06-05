# 시스템 설계 개요

이 문서는 한국투자증권 REST API를 기반으로 한 국내 주식 자동매매 시스템의 설계 예시를 제공합니다. 전체 구성 요소는 다음과 같습니다.
본 문서는 한국투자증권에서 제공하는 [open-trading-api](https://github.com/koreainvestment/open-trading-api) 샘플 코드를 참고하여 작성되었습니다. 샘플 코드를 활용한 투자 손실에 대한 책임은 사용자에게 있습니다.

## 아키텍처 요약

```text
[사용자] --(HTTPS)--> [Nginx/Frontend] --(REST)--> [FastAPI 백엔드] --(SQLAlchemy)--> [MySQL]
                                    \--(OpenAI API)
                                    \--(증권사 REST API)
```

- **백엔드**: Python / FastAPI
- **전략 모듈**: 여러 매매 전략을 Strategy 패턴으로 구현하며, 자세한 내용은 `docs/strategies_kr.md` 참고
- **데이터베이스**: MySQL (SQLAlchemy ORM 사용)
- **스케줄러**: APScheduler로 월요일 매수, 금요일 매도 등 예약
- **인증**: JWT + OAuth2 (카카오 로그인 확장 가능)
- **프론트엔드**: React.js 또는 Svelte.js + Chart.js
- **배포**: Docker Compose (DB, 백엔드, 프론트엔드 각각 컨테이너)

아래 섹션에서 각 구성 요소의 역할과 예시 코드를 설명합니다.

## 주요 컴포넌트 책임

- **전략 모듈**: 다양한 매매 전략을 클래스 형태로 구현한다. `Strategy` 인터페이스를 기반으로 평균회귀(`MeanReversionStrategy`) 등 여러 전략을 추가할 수 있다.
- **데이터 분석 모듈**: Pandas/Numpy/Scipy를 이용하여 종가 시계열 데이터 분석, 이상치 탐지, 통계 계산을 수행한다. 결과는 DB에 저장한다.
- **자동매매 스케줄러**: APScheduler로 월요일 매수, 금요일 손절/익절 또는 전량 청산 작업을 스케줄링한다.
- **API 서버**: FastAPI 기반 REST API. 사용자 인증(JWT, OAuth2), 전략 실행, 주문 전달, 실시간 시세 조회 등을 담당한다.
- **인증 시스템**: OAuth2, JWT를 기반으로 토큰 발급 및 검증. 카카오 로그인을 연동할 수 있도록 OAuth 클라이언트 구조를 확장 가능하게 설계한다.
- **프론트엔드**: React/Svelte + Chart.js로 종목 검색, 전략 설정, 통계 리포트, 실시간 차트 등을 제공한다.

## 평균회귀 전략 (예시 코드)
```python
# backend/strategies/base.py
from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, prices):
        """시계열 데이터로부터 매수/매도 신호를 생성"""
        pass
```
```python
# backend/strategies/mean_reversion.py
import numpy as np
import pandas as pd
from .base import Strategy

class MeanReversionStrategy(Strategy):
    def __init__(self, window:int=20, z_threshold:float=2.0,
                 stop_loss:float=-0.05, take_profit:float=0.11):
        self.window = window
        self.z_threshold = z_threshold
        self.stop_loss = stop_loss
        self.take_profit = take_profit

    def generate_signals(self, prices:pd.Series):
        mean = prices.rolling(self.window).mean()
        std = prices.rolling(self.window).std()
        zscore = (prices - mean) / std
        signals = pd.Series(index=prices.index, data=0)
        signals[zscore < -self.z_threshold] = 1  # 매수
        signals[zscore > self.z_threshold] = -1  # 매도
        return signals
```

## SQLAlchemy 모델 예시
```python
# backend/models.py
from datetime import datetime
from sqlalchemy import (Column, Integer, String, Float, DateTime, Boolean,
                        ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    kakao_id = Column(String(100))

class StockPrice(Base):
    __tablename__ = "stock_prices"
    id = Column(Integer, primary_key=True)
    symbol = Column(String(20), index=True)
    date = Column(DateTime, index=True)
    close = Column(Float)

class TradeLog(Base):
    __tablename__ = "trade_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    symbol = Column(String(20))
    action = Column(String(10))  # BUY/SELL
    price = Column(Float)
    quantity = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User")
```

## FastAPI 엔드포인트 예시
```python
# backend/main.py (발췌)
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import engine, get_db
from .models import Base
from .auth import login_for_access_token, get_current_user

app = FastAPI(title="Trading API")

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)

@app.post("/token")
async def login(form_data: Depends(login_for_access_token)):
    return form_data

@app.get("/prices/{symbol}")
async def get_prices(symbol: str, db: Session = Depends(get_db)):
    prices = db.query(StockPrice).filter(StockPrice.symbol == symbol).all()
    if not prices:
        raise HTTPException(status_code=404, detail="symbol not found")
    return {"prices": [{"date": p.date, "close": p.close} for p in prices]}

@app.post("/trade/{symbol}")
async def trade(symbol: str, user = Depends(get_current_user), db: Session = Depends(get_db)):
    log = TradeLog(user_id=user.id, symbol=symbol, action="BUY", price=0.0, quantity=1)
    db.add(log)
    db.commit()
    return {"trade_id": log.id}
```

## 프론트엔드 구조 예시
```
frontend/
  ├── public/
  │   └── index.html
  ├── src/
  │   ├── components/
  │   │   └── PriceChart.jsx
  │   ├── App.jsx
  │   └── index.js
  ├── package.json
  └── vite.config.js
```
프론트엔드는 React와 Vite 기반으로 동작하며 REST API를 호출해 실시간 시세 조회, 전략 설정, 통계 리포트를 제공한다.

### API 사용 예시
```javascript
// 종가 데이터 조회
axios.get(`/prices/005930`).then(res => console.log(res.data));

// 로그인 후 토큰 저장
axios.post('/token', new URLSearchParams({username:'user', password:'pass'}))
     .then(res => localStorage.setItem('token', res.data.access_token));

// 매수 요청
axios.post('/trade/005930', {}, {
  headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
});
```

### 환경 변수 관리
프로젝트 루트에 `.env` 파일을 두고 다음과 같은 값을 설정한다. 예시는
`.env.example` 파일에 포함되어 있다.

```
DATABASE_URL=mysql+pymysql://user:password@db:3306/trading
SECRET_KEY=<임의 문자열>
OPENAI_API_KEY=<OpenAI 키>
KIS_APP_KEY=<증권사 앱 키>
KIS_APP_SECRET=<증권사 시크릿>
KIS_ACCOUNT=<계좌번호 앞 8자리>
KIS_ACCOUNT_PRODUCT_CODE=<계좌번호 뒤 2자리>
KIS_URL_BASE=https://openapi.koreainvestment.com:9443
KIS_HTS_ID=<HTS ID>
```
Docker Compose와 로컬 실행 모두 동일한 `.env` 파일을 사용하므로, 사용자 는 이 파일만 적절히 작성하면 서비스를 즉시 실행할 수 있다.

## Docker Compose 및 Dockerfile 예시
```yaml
# docker-compose.yml
version: "3"
services:
  db:
    image: mysql:8
    env_file: .env
    volumes:
      - db-data:/var/lib/mysql
  backend:
    build: ./
    command: uvicorn backend.main:app --host 0.0.0.0 --port 8000
    volumes:
      - ./:/app
    env_file: .env
    depends_on:
      - db
  frontend:
    image: node:18
    working_dir: /app
    volumes:
      - ./frontend:/app
    command: npm run dev
    ports:
      - "3000:3000"
volumes:
  db-data:
```
```dockerfile
# Dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 시스템 전체 흐름
1. 매주 월요일 오전 APScheduler가 평균회귀 전략 실행 및 매수 주문 전송.
2. 데이터는 MySQL에 저장되며, 분석 결과는 주차별로 기록.
3. 매주 금요일 종가 기준 손절/익절 조건 확인 후 전량 매도.
4. 백엔드에서 `openai_client.py`를 통해 OpenAI GPT API를 호출해 주간 보고서를 작성하고 `weekly_reports` 테이블에 저장.
5. 사용자는 프론트엔드 대시보드에서 주간 리포트와 실시간 시세를 조회.

## 안정성 및 확장성 고려 사항
- 환경 변수는 `.env` 또는 Docker Secrets로 관리하여 API 키 노출 방지.
- 예외 처리와 로깅은 `logging` 모듈과 미들웨어로 일관성 있게 기록.
- 단위 테스트와 통합 테스트를 작성하여 CI 파이프라인에서 자동 실행.
- 주문 실행 시 네트워크 장애에 대비한 재시도 로직과 슬랙/메일 알림을 추가 가능.
- OAuth2 토큰 만료, 권한 체크 등을 엄격히 검증하여 보안성을 높인다.

전략별 세부 설명은 `strategies_kr.md` 문서를 참고하세요.
