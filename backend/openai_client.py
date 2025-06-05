import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_weekly_report(symbol: str, stats: dict) -> str:
    """주간 종목 보고서를 OpenAI API로 생성한다."""
    if not openai.api_key:
        raise RuntimeError("OPENAI_API_KEY not configured")
    prompt = (
        f"다음은 {symbol} 종목의 주간 통계입니다: {stats}. 이 데이터를 기반으로 간단한 투자 "
        "요약 보고서를 작성해 주세요."
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message["content"].strip()
