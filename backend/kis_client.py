import os
import json
import requests

APP_KEY = os.getenv("KIS_APP_KEY")
APP_SECRET = os.getenv("KIS_APP_SECRET")
ACCOUNT = os.getenv("KIS_ACCOUNT")
ACCOUNT_PRODUCT_CODE = os.getenv("KIS_ACCOUNT_PRODUCT_CODE", "01")
URL_BASE = os.getenv("KIS_URL_BASE", "https://openapi.koreainvestment.com:9443")
HTS_ID = os.getenv("KIS_HTS_ID", "")

_token = None


def get_access_token() -> str:
    """한국투자증권 Open API 토큰 발급"""
    global _token
    if _token:
        return _token
    if not APP_KEY or not APP_SECRET:
        raise RuntimeError("KIS_APP_KEY or KIS_APP_SECRET not configured")
    url = f"{URL_BASE}/oauth2/tokenP"
    headers = {"content-type": "application/json"}
    body = {"grant_type": "client_credentials", "appkey": APP_KEY, "appsecret": APP_SECRET}
    res = requests.post(url, headers=headers, data=json.dumps(body))
    res.raise_for_status()
    _token = res.json().get("access_token")
    return _token


def place_order(symbol: str, qty: int, price: float, side: str = "buy") -> dict:
    """시장가 주문 예시"""
    token = get_access_token()
    tr_id = "TTTC0802U" if side == "buy" else "TTTC0801U"
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {token}",
        "appKey": APP_KEY,
        "appSecret": APP_SECRET,
        "tr_id": tr_id,
    }
    payload = {
        "CANO": ACCOUNT,
        "ACNT_PRDT_CD": ACCOUNT_PRODUCT_CODE,
        "PDNO": symbol,
        "ORD_DVSN": "00",
        "ORD_QTY": str(qty),
        "ORD_UNPR": str(price),
        "CTAC_TLNO": "",
        "SLL_TYPE": "00",
        "ALGO_NO": "",
    }
    url = f"{URL_BASE}/uapi/domestic-stock/v1/trading/order-cash"
    res = requests.post(url, headers=headers, data=json.dumps(payload))
    res.raise_for_status()
    return res.json()
