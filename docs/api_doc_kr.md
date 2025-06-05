# API 문서

이 문서는 FastAPI 백엔드에서 제공하는 주요 REST API를 정리한 것입니다.
각 요청은 `/token` 엔드포인트를 통해 발급한 JWT 토큰을 `Authorization: Bearer` 헤더로 전달하여 인증합니다.

## 인증
### `POST /users`
신규 사용자 등록.
- `username`: 사용자명
- `password`: 비밀번호

### `POST /token`
로그인하여 액세스 토큰을 발급받습니다.
- `username`
- `password`

## 가격 조회
### `GET /prices/{symbol}`
지정한 종목의 종가 시계열을 반환합니다.
```json
{
  "symbol": "005930",
  "prices": [{"date": "2024-01-01", "close": 70000.0}]
}
```

## 트레이드
### `POST /trade/{symbol}`
매수 예시 엔드포인트입니다. `quantity` 등 세부 파라미터는 추후 확장 가능합니다.

### `GET /trade/history`
사용자의 주문 기록을 최신순으로 반환합니다.

## 관심 종목 관리
### `GET /watchlist`
관심 종목 목록 조회.

### `POST /watchlist`
관심 종목 추가.
- `symbol`: 종목 코드

### `DELETE /watchlist/{symbol}`
관심 종목 삭제.

## 응답 예시
각 엔드포인트의 기본 응답 형식은 다음과 같습니다.
```json
{"status": "deleted"}
```
필요에 따라 필드가 추가될 수 있습니다.

## 전략 정보
### `GET /strategies`
사용 가능한 모든 전략 목록과 설명을 반환합니다.

### `POST /strategy/{name}/execute`
지정한 전략을 실행하여 매수/매도 신호에 따라 주문을 기록합니다.
- `name`: 전략 이름 (`mean_reversion`, `momentum`, `trend_following` 등)
- `symbol`: 대상 종목 코드 (쿼리 파라미터)

## 주간 리포트
### `GET /reports`
OpenAI API를 통해 생성된 주간 보고서 목록을 반환합니다.
