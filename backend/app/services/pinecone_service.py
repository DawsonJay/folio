import os
from typing import List, Dict, Any, Optional
from pinecone import Pinecone, ServerlessSpec

class PineconeService:
    def __init__(self):
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            raise ValueError("PINECONE_API_KEY environment variable is not set")
        
        self.pc = Pinecone(api_key=api_key)
        self.index_name = "folio-notes"
        self.dimension = 1536
        self.metric = "cosine"
        
        self._ensure_index_exists()
        self.index = self.pc.Index(self.index_name)
    
    def _ensure_index_exists(self):
        existing_indexes = [index.name for index in self.pc.list_indexes()]
        
        if self.index_name not in existing_indexes:
            self.pc.create_index(
                name=self.index_name,
                dimension=self.dimension,
                metric=self.metric,
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
    
    def upsert_note(self, note_id: str, embedding: List[float], metadata: Dict[str, Any]):
        self.index.upsert(vectors=[(note_id, embedding, metadata)])
    
    def upsert_notes_batch(self, notes: List[tuple]):
        self.index.upsert(vectors=notes)
    
    def query_similar(
        self,
        embedding: List[float],
        top_k: int = 5,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        results = self.index.query(
            vector=embedding,
            top_k=top_k,
            include_metadata=True,
            filter=filter
        )
        
        return [
            {
                "id": match.id,
                "score": match.score,
                "metadata": match.metadata
            }
            for match in results.matches
        ]
    
    def delete_note(self, note_id: str):
        self.index.delete(ids=[note_id])
    
    def delete_all_notes(self):
        self.index.delete(delete_all=True)
    
    def get_stats(self) -> Dict[str, Any]:
        return self.index.describe_index_stats()

