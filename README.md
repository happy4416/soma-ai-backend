# 소마 AI 백엔드 (soma-ai-backend)

경북소프트웨어마이스터고등학교 AI 챗봇 백엔드 API

## 📋 프로젝트 소개

RAG(Retrieval-Augmented Generation) 기반의 학교 정보 챗봇 백엔드입니다.
- FastAPI 기반 REST API
- Ollama를 활용한 로컬 LLM
- ChromaDB를 활용한 벡터 데이터베이스
- 학교 정보 자동 크롤링 및 학습

## 🛠️ 기술 스택

- **Framework**: FastAPI 0.115+
- **LLM**: Ollama (qwen2.5:3b)
- **Vector DB**: ChromaDB
- **Web Scraping**: BeautifulSoup4
- **Language**: Python 3.8+

## 📁 프로젝트 구조

```
backend/
├── app.py                      # FastAPI 메인 애플리케이션
├── requirements.txt            # Python 패키지 의존성
├── .env.example               # 환경 변수 예시
├── services/
│   ├── __init__.py
│   ├── crawler_service.py     # 학교 정보 크롤링
│   ├── ollama_service.py      # Ollama LLM 연동
│   └── vector_service.py      # ChromaDB 벡터 DB 관리
└── chroma_db/                 # ChromaDB 데이터 저장소 (자동 생성)
```

## 🚀 설치 및 실행

### 1. 필수 요구사항

- Python 3.8 이상
- Ollama 설치 및 실행 중
- qwen2.5:3b 모델 다운로드

```bash
# Ollama 설치 (Windows)
# https://ollama.com/download 에서 다운로드

# qwen2.5:3b 모델 다운로드
ollama pull qwen2.5:3b
```

### 2. 패키지 설치

```bash
# 가상환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate  # Windows

# 패키지 설치
pip install -r requirements.txt
```

### 3. 환경 변수 설정

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 수정
OLLAMA_API_URL=http://localhost:11434
```

### 4. 서버 실행

```bash
# 개발 서버 실행
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# 또는
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

서버가 실행되면 다음 주소에서 접속 가능합니다:
- API: http://localhost:8000
- API 문서 (Swagger): http://localhost:8000/docs
- API 문서 (ReDoc): http://localhost:8000/redoc

## 📡 API 엔드포인트

### 기본 정보

- `GET /` - 서버 상태 확인
- `GET /api/health` - 시스템 헬스 체크
- `GET /api/stats` - 데이터베이스 통계

### 모델 관리

- `GET /api/models` - 사용 가능한 Ollama 모델 목록

### 채팅

- `POST /api/chat` - RAG 기반 채팅
  ```json
  {
    "message": "학교 위치가 어디인가요?",
    "model": "qwen2.5:3b"
  }
  ```

### 데이터 관리

- `POST /api/recrawl` - 학교 정보 재크롤링

## 🔧 주요 기능

### 1. RAG (Retrieval-Augmented Generation)

사용자 질문에 대해:
1. ChromaDB에서 관련 문서 검색 (top 3)
2. 검색된 문서를 컨텍스트로 활용
3. Ollama LLM으로 답변 생성
4. 출처 정보와 함께 응답

### 2. 자동 크롤링

서버 시작 시 자동으로:
- 학교 기본 정보
- 학과 정보
- 입학 안내
- 기숙사 정보
- 취업 정보
- 학교 생활 정보

총 9개 문서를 ChromaDB에 저장

### 3. 벡터 검색

ChromaDB를 활용한 의미 기반 검색:
- 자동 임베딩 생성
- 유사도 기반 문서 검색
- 빠른 검색 성능

## 🔐 환경 변수

| 변수명 | 설명 | 기본값 |
|--------|------|--------|
| `OLLAMA_API_URL` | Ollama API 서버 주소 | `http://localhost:11434` |

## 📝 개발 가이드

### 새로운 문서 추가

`services/crawler_service.py`의 `crawl_school_info()` 메서드에 문서 추가:

```python
documents.append({
    "title": "문서 제목",
    "content": "문서 내용...",
    "source": "출처"
})
```

### 새로운 API 엔드포인트 추가

`app.py`에 라우터 추가:

```python
@app.get("/api/new-endpoint")
async def new_endpoint():
    return {"message": "새로운 엔드포인트"}
```

### 다른 LLM 모델 사용

```bash
# 다른 모델 다운로드
ollama pull llama2
ollama pull mistral

# API 요청 시 model 파라미터 변경
{
  "message": "질문",
  "model": "llama2"
}
```

## 🐛 트러블슈팅

### Ollama 연결 실패

```bash
# Ollama 서비스 상태 확인
ollama list

# Ollama 재시작
# Windows: 작업 관리자에서 Ollama 종료 후 재실행
```

### ChromaDB 오류

```bash
# ChromaDB 데이터 초기화
rm -rf chroma_db/  # Linux/Mac
# 또는
rmdir /s chroma_db  # Windows

# 서버 재시작하면 자동으로 재생성됨
```

### 포트 충돌

```bash
# 다른 포트로 실행
uvicorn app:app --reload --port 8001
```

## 📦 배포

### Docker 배포 (선택사항)

```bash
# Dockerfile 생성 후
docker build -t soma-ai-backend .
docker run -p 8000:8000 soma-ai-backend
```

### 프로덕션 배포

```bash
# gunicorn 설치
pip install gunicorn

# 프로덕션 서버 실행
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🤝 기여

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

## 📞 문의

- 프로젝트: [soma-ai](https://github.com/happy4416/soma-ai)
- 프론트엔드: [soma-ai (GitHub Pages)](https://happy4416.github.io/soma-ai)

## 🔗 관련 링크

- [FastAPI 문서](https://fastapi.tiangolo.com/)
- [Ollama 문서](https://ollama.com/)
- [ChromaDB 문서](https://docs.trychroma.com/)
- [경북소프트웨어마이스터고](https://gbsw.hs.kr)
