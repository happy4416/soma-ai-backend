import chromadb
from chromadb.config import Settings
from typing import List, Dict
import os

class VectorService:
    def __init__(self):
        # ChromaDB 초기화 (로컬 저장)
        self.client = chromadb.Client(Settings(
            persist_directory="./chroma_db",
            anonymized_telemetry=False
        ))
        
        # 컬렉션 생성 또는 가져오기
        try:
            self.collection = self.client.get_collection("school_docs")
            print("기존 컬렉션 로드됨")
        except:
            self.collection = self.client.create_collection(
                name="school_docs",
                metadata={"description": "경북소프트웨어마이스터고 문서"}
            )
            print("새 컬렉션 생성됨")
    
    def add_documents(self, documents: List[Dict[str, str]]):
        """문서 추가"""
        for i, doc in enumerate(documents):
            doc_id = f"doc_{i}_{hash(doc['content'])}"
            
            # 이미 존재하는지 확인
            try:
                existing = self.collection.get(ids=[doc_id])
                if existing['ids']:
                    continue
            except:
                pass
            
            # 문서 추가 (ChromaDB가 자동으로 임베딩)
            self.collection.add(
                ids=[doc_id],
                documents=[doc['content']],
                metadatas=[{
                    "title": doc['title'],
                    "source": doc['source']
                }]
            )
        
        print(f"{len(documents)}개 문서 추가 완료")
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """유사 문서 검색"""
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        documents = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                documents.append({
                    "content": doc,
                    "title": metadata.get("title", ""),
                    "source": metadata.get("source", ""),
                    "distance": results['distances'][0][i] if results['distances'] else 0
                })
        
        return documents
    
    def get_stats(self) -> Dict:
        """통계 정보"""
        count = self.collection.count()
        return {
            "total_documents": count,
            "collection_name": "school_docs"
        }
