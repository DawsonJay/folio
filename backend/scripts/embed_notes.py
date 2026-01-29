import os
import sys
from pathlib import Path
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent))

load_dotenv(Path(__file__).parent.parent / ".env")

from app.services.openai_service import OpenAIService
from app.services.embedding_storage import LocalEmbeddingStorage

def read_note_file(file_path: Path) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    note_id = file_path.stem
    category = file_path.parent.name
    
    return {
        "id": note_id,
        "content": content,
        "category": category,
        "file_path": str(file_path.relative_to(Path(__file__).parent.parent))
    }

def main():
    print("Initializing services...")
    openai_service = OpenAIService()
    storage = LocalEmbeddingStorage()
    
    notes_dir = Path(__file__).parent.parent / "notes"
    
    if not notes_dir.exists():
        print(f"Notes directory not found: {notes_dir}")
        return
    
    print(f"Reading notes from {notes_dir}...")
    note_files = list(notes_dir.rglob("*.md"))
    print(f"Found {len(note_files)} note files")
    
    notes_data = []
    for note_file in note_files:
        note_data = read_note_file(note_file)
        notes_data.append(note_data)
        print(f"  Read: {note_data['category']}/{note_data['id']}")
    
    print(f"\nGenerating embeddings for {len(notes_data)} notes...")
    vectors_to_store = []
    
    for i, note_data in enumerate(notes_data):
        print(f"  [{i+1}/{len(notes_data)}] Embedding: {note_data['id']}")
        
        embedding = openai_service.get_embedding(note_data['content'])
        
        metadata = {
            "category": note_data['category'],
            "file_path": note_data['file_path'],
            "title": note_data['id'].replace('-', ' ').title(),
            "content_preview": note_data['content'][:200]
        }
        
        vectors_to_store.append((
            note_data['id'],
            embedding,
            metadata
        ))
    
    print(f"\nStoring {len(vectors_to_store)} embeddings locally...")
    storage.store_notes_batch(vectors_to_store)
    
    print("\nVerifying storage...")
    stats = storage.get_stats()
    print(f"Storage stats: {stats}")
    
    print(f"\n✅ Successfully embedded {len(notes_data)} notes into local storage!")
    print(f"   Storage location: {storage.storage_path}")

if __name__ == "__main__":
    main()

