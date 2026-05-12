from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

from services.vector_service import VectorService
from services.ollama_service import OllamaService
from services.crawler_service import CrawlerService

load_dotenv()

app = FastAPI(
    title="소마 AI - 경북소프트웨어마이스터고 도우미",
    description="경북소프트웨어마이스터고등학교 AI 챗봇 백엔드 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://happy4416.github.io",
        "*"  # 개발 중에는 모든 도메인 허용
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 서비스 초기화
vector_service = VectorService()
ollama_service = OllamaService()
crawler_service = CrawlerService()

class ChatRequest(BaseModel):
    message: str
    model: Optional[str] = "qwen2.5:3b"

class ChatResponse(BaseModel):
    response: str
    sources: List[str] = []

@app.on_event("startup")
async def startup_event():
    """서버 시작 시 학교 정보 크롤링"""
    print("학교 정보 크롤링 시작...")
    
    # 이미 데이터가 있는지 확인
    stats = vector_service.get_stats()
    if stats['total_documents'] == 0:
        documents = crawler_service.crawl_school_info()
        vector_service.add_documents(documents)
        print(f"크롤링 완료: {len(documents)}개 문서")
    else:
        print(f"기존 데이터 사용: {stats['total_documents']}개 문서")

@app.get("/")
async def root():
    return {
        "message": "소마 AI - 경북소프트웨어마이스터고 도우미",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/api/health")
async def health_check():
    """시스템 상태 확인"""
    ollama_status = await ollama_service.check_health()
    stats = vector_service.get_stats()
    
    return {
        "status": "healthy" if ollama_status else "unhealthy",
        "ollama": "running" if ollama_status else "not running",
        "vector_db": "connected",
        "documents": stats['total_documents']
    }

@app.get("/api/models")
async def get_models():
    """사용 가능한 Ollama 모델 목록"""
    return await ollama_service.get_models()

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """RAG 기반 채팅"""
    try:
        # 1. 관련 문서 검색
        relevant_docs = vector_service.search(
            query=request.message,
            top_k=3
        )
        
        # 2. 컨텍스트 생성
        context = "\n\n".join([f"[{doc['title']}]\n{doc['content']}" for doc in relevant_docs])
        sources = [doc['title'] for doc in relevant_docs]
        
        # 3. 프롬프트 생성
        prompt = f"""당신은 경북소프트웨어마이스터고등학교의 도우미 AI입니다.
다음은 학교 관련 정보입니다:

{context}

위 정보를 바탕으로 학생의 질문에 친절하고 정확하게 답변해주세요.
정보에 없는 내용은 "해당 정보를 찾을 수 없습니다"라고 답변하세요.

학생 질문: {request.message}

답변:"""
        
        # 4. Ollama로 응답 생성
        response = await ollama_service.generate(
            prompt=prompt,
            model=request.model
        )
        
        return ChatResponse(
            response=response,
            sources=sources
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats():
    """통계 정보"""
    return vector_service.get_stats()

@app.post("/api/recrawl")
async def recrawl():
    """학교 정보 재크롤링"""
    try:
        documents = crawler_service.crawl_school_info()
        vector_service.add_documents(documents)
        return {"message": f"{len(documents)}개 문서 크롤링 완료"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
