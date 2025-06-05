# Stratium

이 저장소는 한국투자증권 REST API를 활용한 국내 주식 자동매매 시스템 예제입니다.
상세한 시스템 구조와 코드 샘플은 `docs/system_design_kr.md`, `docs/strategies_kr.md`와 API 문서 `docs/api_doc_kr.md`를 참고하세요. 코드 스타일은 `docs/coding_style.md`에 정리되어 있습니다.

## 개발 환경 설정

```bash
git clone <repo>
cd Stratium
pip install -r requirements.txt
pytest
```

환경 변수 설정을 위해 `.env.example` 파일을 복사하여 `.env`로 저장한 뒤 값 을 채웁니다.

```bash
cp .env.example .env
# 필요한 값 수정 후
docker-compose up --build
```

프론트엔드를 로컬에서 실행하려면 Node.js 환경에서 다음을 수행합니다.

```bash
cd frontend
npm install
npm run dev
```

OpenAI API 키를 설정하면 자동으로 주간 보고서를 생성하여 `/reports` 엔드포인트를 통해 확인할 수 있습니다.

## 참고 및 주의사항
이 프로젝트는 한국투자증권에서 공개한 [open-trading-api](https://github.com/koreainvestment/open-trading-api) 샘플 코드를 기반으로 작성되었습니다. 샘플 코드는 참고용이며 이를 이용한 투자 손실에 대해 개발자는 책임지지 않습니다.
