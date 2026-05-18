# Replicate API 설정 가이드

Railway에서 Ollama 대신 Replicate API를 사용하는 방법입니다.

## 🎯 Replicate란?

Replicate는 클라우드에서 AI 모델을 실행할 수 있는 서비스입니다.
- Llama 2, Mistral 등 다양한 오픈소스 LLM 지원
- 사용한 만큼만 비용 지불
- 무료 크레딧 제공

## 🚀 설정 방법

### 1. Replicate 계정 생성

1. https://replicate.com 접속
2. GitHub 계정으로 로그인
3. 무료 크레딧 받기

### 2. API 토큰 발급

1. https://replicate.com/account/api-tokens 접속
2. "Create token" 클릭
3. 토큰 복사 (예: `r8_...`)

### 3. Railway 환경 변수 설정

Railway 대시보드에서 환경 변수 추가:

```bash
LLM_PROVIDER=replicate
REPLICATE_API_TOKEN=r8_your_token_here
```

### 4. 배포

GitHub에 푸시하면 Railway가 자동으로 재배포합니다!

## 💰 비용

### 무료 크레딧
- 가입 시 무료 크레딧 제공
- 테스트 및 소규모 프로젝트에 충분

### 유료 사용
- Llama 2 7B: $0.00025/초 (~$0.015/분)
- Llama 2 13B: $0.00070/초 (~$0.042/분)
- Mistral 7B: $0.00025/초 (~$0.015/분)

예시: 100개 질문 (평균 5초/질문) = $0.125

## 🔧 로컬 개발

로컬에서는 Ollama를 계속 사용할 수 있습니다:

```bash
# .env 파일
LLM_PROVIDER=ollama
OLLAMA_API_URL=http://localhost:11434
```

## 📊 지원 모델

### Llama 2 7B Chat (권장)
- 모델: `meta/llama-2-7b-chat`
- 빠르고 저렴
- 한국어 지원 (제한적)

### Llama 2 13B Chat
- 모델: `meta/llama-2-13b-chat`
- 더 정확한 응답
- 비용 약 3배

### Mistral 7B Instruct
- 모델: `mistralai/mistral-7b-instruct-v0.2`
- 빠른 속도
- 영어 최적화

## 🔄 전환 방법

### Ollama → Replicate

Railway 환경 변수:
```bash
LLM_PROVIDER=replicate
REPLICATE_API_TOKEN=r8_...
```

### Replicate → Ollama

Railway 환경 변수:
```bash
LLM_PROVIDER=ollama
OLLAMA_API_URL=https://your-ollama-server.com
```

## 🐛 트러블슈팅

### API 토큰 오류

```
Error: REPLICATE_API_TOKEN not set
```

해결: Railway 환경 변수에 `REPLICATE_API_TOKEN` 추가

### 모델 로딩 느림

첫 요청은 모델 로딩으로 10-30초 소요될 수 있습니다.
이후 요청은 빠릅니다.

### 비용 초과

Replicate 대시보드에서 사용량 모니터링:
https://replicate.com/account/billing

## 🔗 유용한 링크

- [Replicate 문서](https://replicate.com/docs)
- [Replicate 가격](https://replicate.com/pricing)
- [지원 모델 목록](https://replicate.com/explore)
- [Python 클라이언트](https://github.com/replicate/replicate-python)

## 📝 참고사항

### 장점
- ✅ Railway에서 바로 작동
- ✅ 서버 관리 불필요
- ✅ 다양한 모델 선택 가능
- ✅ 무료 크레딧 제공

### 단점
- ❌ 비용 발생 (사용량 기반)
- ❌ 첫 요청 느림 (콜드 스타트)
- ❌ 인터넷 연결 필요

## 🎯 추천 설정

**개발 환경:**
```bash
LLM_PROVIDER=ollama
OLLAMA_API_URL=http://localhost:11434
```

**프로덕션 환경 (Railway):**
```bash
LLM_PROVIDER=replicate
REPLICATE_API_TOKEN=r8_...
```

이렇게 하면 로컬에서는 무료로 Ollama를 사용하고,
프로덕션에서는 Replicate를 사용할 수 있습니다! 🚀
