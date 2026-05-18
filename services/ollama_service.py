import httpx
import os
import replicate

class OllamaService:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "ollama").lower()
        self.api_url = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
        
        # Replicate 설정
        if self.provider == "replicate":
            replicate_token = os.getenv("REPLICATE_API_TOKEN")
            if replicate_token:
                os.environ["REPLICATE_API_TOKEN"] = replicate_token
    
    async def check_health(self) -> bool:
        """서버 상태 확인"""
        if self.provider == "replicate":
            # Replicate는 항상 사용 가능
            return bool(os.getenv("REPLICATE_API_TOKEN"))
        
        # Ollama 상태 확인
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}/api/tags", timeout=5.0)
                return response.status_code == 200
        except:
            return False
    
    async def get_models(self):
        """사용 가능한 모델 목록"""
        if self.provider == "replicate":
            # Replicate 모델 목록
            return {
                "models": [
                    {"name": "meta/llama-2-7b-chat"},
                    {"name": "meta/llama-2-13b-chat"},
                    {"name": "mistralai/mistral-7b-instruct-v0.2"},
                ]
            }
        
        # Ollama 모델 목록
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}/api/tags")
                return response.json()
        except Exception as e:
            return {"models": [], "error": str(e)}
    
    async def generate(self, prompt: str, model: str = "qwen2.5:3b") -> str:
        """텍스트 생성"""
        if self.provider == "replicate":
            return await self._generate_replicate(prompt, model)
        else:
            return await self._generate_ollama(prompt, model)
    
    async def _generate_replicate(self, prompt: str, model: str) -> str:
        """Replicate로 텍스트 생성"""
        try:
            # Replicate 모델 매핑
            model_map = {
                "qwen2.5:3b": "meta/llama-2-7b-chat",
                "llama2": "meta/llama-2-7b-chat",
                "mistral": "mistralai/mistral-7b-instruct-v0.2",
            }
            
            replicate_model = model_map.get(model, "meta/llama-2-7b-chat")
            
            # Replicate API 호출
            output = replicate.run(
                replicate_model,
                input={
                    "prompt": prompt,
                    "max_new_tokens": 500,
                    "temperature": 0.7,
                }
            )
            
            # 출력 결합
            if isinstance(output, list):
                return "".join(output)
            return str(output)
            
        except Exception as e:
            raise Exception(f"Replicate API error: {str(e)}")
    
    async def _generate_ollama(self, prompt: str, model: str) -> str:
        """Ollama로 텍스트 생성"""
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
