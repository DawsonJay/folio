import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional
import os

class LocalEmbeddingStorage:
    def __init__(self, storage_path: str = "backend/embeddings.json"):
        self.storage_path = Path(storage_path)
        self.embeddings: Dict[str, Dict[str, Any]] = {}
        self._load()
    
    def _load(self):
        if self.storage_path.exists():
            with open(self.storage_path, 'r') as f:
                self.embeddings = json.load(f)
        else:
            self.embeddings = {}
    
    def _save(self):
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.storage_path, 'w') as f:
            json.dump(self.embeddings, f, indent=2)
    
    def store_note(self, note_id: str, embedding: List[float], metadata: Dict[str, Any]):
        self.embeddings[note_id] = {
            "embedding": embedding,
            "metadata": metadata
        }
        self._save()
    
    def store_notes_batch(self, notes: List[tuple]):
        for note_id, embedding, metadata in notes:
            self.embeddings[note_id] = {
                "embedding": embedding,
                "metadata": metadata
            }
        self._save()
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    
    def query_similar(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        results = []
        
        for note_id, data in self.embeddings.items():
            embedding = data["embedding"]
            metadata = data["metadata"]
            
            if filter:
                match = True
                for key, value in filter.items():
                    if metadata.get(key) != value:
                        match = False
                        break
                if not match:
                    continue
            
            similarity = self.cosine_similarity(query_embedding, embedding)
            
            results.append({
                "id": note_id,
                "score": float(similarity),
                "metadata": metadata
            })
        
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_notes": len(self.embeddings),
            "storage_path": str(self.storage_path)
        }
    
    def delete_note(self, note_id: str):
        if note_id in self.embeddings:
            del self.embeddings[note_id]
            self._save()
    
    def delete_all(self):
        self.embeddings = {}
        self._save()

