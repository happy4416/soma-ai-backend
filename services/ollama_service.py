import httpx
import os

class OllamaService:
    def __init__(self):
        self.api_url = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
    
    async def check_health(self) -> bool:
        """Ollama 서버 상태 확인"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}/api/tags", timeout=5.0)
                return response.status_code == 200
        except:
            return False
    
    async def get_models(self):
        """사용 가능한 모델 목록"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}/api/tags")
                return response.json()
        except Exception as e:
            return {"models": [], "error": str(e)}
    
    async def generate(self, prompt: str, model: str = "qwen2.5:3b") -> str:
        """텍스트 생성"""
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.api_url}/api/generate",
                    json={
                        "model": model,
                        "prompt": prompt,
                        "stream": False
                    }
                )
                
                if response.status_code != 200:
                    raise Exception(f"Ollama API error: {response.status_code}")
                
                result = response.json()
                return result.get("response", "")
        except Exception as e:
            raise Exception(f"Failed to generate response: {str(e)}")
