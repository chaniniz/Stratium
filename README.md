# Stratium

이 저장소는 한국투자증권 REST API를 활용한 국내 주식 자동매매 시스템 예제입니다.
상세한 시스템 구조와 코드 샘플은 `docs/system_design_kr.md`, `docs/strategies_kr.md`와 API 문서 `docs/api_doc_kr.md`를 참고하세요.


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
