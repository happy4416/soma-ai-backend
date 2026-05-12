# Railway 배포 가이드

## 📋 Railway란?

Railway는 간단하게 백엔드 애플리케이션을 배포할 수 있는 클라우드 플랫폼입니다.
- 무료 플랜 제공 (월 $5 크레딧)
- 자동 HTTPS 제공
- GitHub 연동 자동 배포
- 환경 변수 관리

## 🚀 배포 방법

### 1. Railway 계정 생성

1. https://railway.app 접속
2. "Start a New Project" 클릭
3. GitHub 계정으로 로그인

### 2. 프로젝트 생성

#### 방법 A: GitHub 저장소 연동 (추천)

1. Railway 대시보드에서 "New Project" 클릭
2. "Deploy from GitHub repo" 선택
3. `soma-ai-backend` 저장소 선택
4. 자동으로 배포 시작

#### 방법 B: CLI로 배포

```bash
# Railway CLI 설치
npm i -g @railway/cli

# 로그인
railway login

# 프로젝트 초기화
cd backend
railway init

# 배포
railway up
```

### 3. 환경 변수 설정

Railway 대시보드에서 환경 변수 추가:

```
OLLAMA_API_URL=http://localhost:11434
```

⚠️ **중요**: Railway에서는 Ollama를 직접 실행할 수 없습니다!

#### 해결 방법:

**옵션 1: 외부 Ollama 서버 사용**
- 자체 서버에 Ollama 설치
- 공개 URL로 접근 가능하게 설정
- `OLLAMA_API_URL`을 해당 URL로 설정

**옵션 2: OpenAI API 사용 (권장)**
- Ollama 대신 OpenAI API 사용
- 코드 수정 필요

**옵션 3: Replicate API 사용**
- Replicate에서 LLM 모델 사용
- API 키 발급 필요

### 4. 배포 확인

1. Railway 대시보드에서 "Deployments" 탭 확인
2. 배포 완료 후 "Settings" → "Domains"에서 URL 확인
3. 예시: `https://soma-ai-backend-production.up.railway.app`

### 5. API 테스트

```bash
# 헬스 체크
curl https://your-app.railway.app/api/health

# API 문서
https://your-app.railway.app/docs
```

## 🔧 Railway 설정 파일

### railway.json

Railway 배포 설정:

```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn app:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Procfile

프로세스 실행 명령:

```
web: uvicorn app:app --host 0.0.0.0 --port $PORT
```

### nixpacks.toml

빌드 설정:

```toml
[phases.setup]
nixPkgs = ["python310"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[start]
cmd = "uvicorn app:app --host 0.0.0.0 --port $PORT"
```

## ⚠️ Ollama 문제 해결

Railway는 컨테이너 환경이므로 Ollama를 직접 실행할 수 없습니다.

### 해결 방법 1: OpenAI API 사용 (권장)

`services/ollama_service.py` 수정:

```python
import openai
import os

class OllamaService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def generate(self, prompt: str, model: str = "gpt-3.5-turbo") -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
```

환경 변수 추가:
```
OPENAI_API_KEY=sk-...
```

### 해결 방법 2: 외부 Ollama 서버

1. 자체 서버에 Ollama 설치
2. 공개 URL 설정 (예: ngrok, Cloudflare Tunnel)
3. Railway 환경 변수 설정:
   ```
   OLLAMA_API_URL=https://your-ollama-server.com
   ```

### 해결 방법 3: Replicate API

```bash
pip install replicate
```

```python
import replicate
import os

class OllamaService:
    def __init__(self):
        self.client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))
    
    async def generate(self, prompt: str, model: str = "meta/llama-2-7b-chat") -> str:
        output = self.client.run(model, input={"prompt": prompt})
        return "".join(output)
```

## 💰 비용

### 무료 플랜
- 월 $5 크레딧
- 500시간 실행 시간
- 소규모 프로젝트에 충분

### 유료 플랜
- 사용한 만큼 지불
- 더 많은 리소스
- 프로덕션 환경 권장

## 🔄 자동 배포

GitHub 저장소 연동 시:
1. `main` 브랜치에 푸시
2. Railway가 자동으로 감지
3. 자동 빌드 및 배포
4. 배포 완료 알림

## 📊 모니터링

Railway 대시보드에서:
- CPU/메모리 사용량
- 로그 확인
- 배포 히스토리
- 트래픽 통계

## 🐛 트러블슈팅

### 배포 실패

```bash
# 로그 확인
railway logs

# 재배포
railway up --detach
```

### 환경 변수 문제

```bash
# 환경 변수 확인
railway variables

# 환경 변수 설정
railway variables set OLLAMA_API_URL=http://...
```

### 포트 문제

Railway는 자동으로 `$PORT` 환경 변수를 제공합니다.
코드에서 반드시 `$PORT`를 사용해야 합니다:

```python
import os
port = int(os.getenv("PORT", 8000))
```

## 🔗 유용한 링크

- [Railway 문서](https://docs.railway.app/)
- [Railway CLI](https://docs.railway.app/develop/cli)
- [Railway 가격](https://railway.app/pricing)
- [Railway 커뮤니티](https://discord.gg/railway)

## 📞 문의

배포 관련 문제가 있으면:
1. Railway Discord 커뮤니티
2. Railway 문서 확인
3. GitHub Issues

## 🎯 다음 단계

1. ✅ Railway 배포 완료
2. ✅ 환경 변수 설정
3. ✅ API 테스트
4. ⬜ 프론트엔드에서 Railway URL 연결
5. ⬜ 커스텀 도메인 설정 (선택)

## 🌐 프론트엔드 연결

프론트엔드 `.env.production` 수정:

```bash
NEXT_PUBLIC_API_URL=https://your-app.railway.app
```

프론트엔드 재배포:

```bash
cd frontend
npm run deploy
```

완료! 🎉
