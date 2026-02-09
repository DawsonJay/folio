import os
import sys
from pathlib import Path
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent))

load_dotenv(Path(__file__).parent.parent / ".env")

from app.services.openai_service import OpenAIService
from app.services.embedding_storage import LocalEmbeddingStorage

def extract_question_title(file_path: Path) -> str:
    """Extract the question title from the first # header in the markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
    
    if first_line.startswith('# '):
        return first_line[2:].strip()
    
    raise ValueError(f"No question title found in {file_path} (expected # header on first line)")

def main():
    print("Initializing services...")
    openai_service = OpenAIService()
    
    direct_answer_embeddings_file = Path(__file__).parent.parent / "direct-answer-embeddings.json"
    storage = LocalEmbeddingStorage(storage_path=str(direct_answer_embeddings_file))
    
    direct_answers_dir = Path(__file__).parent.parent / "notes" / "tier-1-direct-answers"
    
    if not direct_answers_dir.exists():
        print(f"Direct answers directory not found: {direct_answers_dir}")
        return
    
    print(f"Reading direct answer files from {direct_answers_dir}...")
    note_files = list(direct_answers_dir.glob("*.md"))
    
    # Exclude metadata directory files (they're now in a subdirectory, but keep this for safety)
    metadata_dir = direct_answers_dir / "metadata"
    excluded_files = {
        "TEMPLATE.md",
        "COMMON-QUESTIONS.md",
        "HIGH-CONFIDENCE-QUESTIONS.md",
        "QUESTIONS-CANNOT-ANSWER.md",
        "FINAL-REVIEW-ASSESSMENT.md"
    }
    note_files = [f for f in note_files if f.name not in excluded_files]
    
    print(f"Found {len(note_files)} direct answer files (excluding metadata directory)")
    
    if not note_files:
        print("No direct answer files to embed.")
        return
    
    vectors_to_store = []
    
    for i, note_file in enumerate(note_files):
        print(f"  [{i+1}/{len(note_files)}] Processing: {note_file.name}")
        
        try:
            question_title = extract_question_title(note_file)
            print(f"      Question: {question_title}")
            
            print(f"      Generating embedding...")
            embedding = openai_service.get_embedding(question_title)
            
            file_path_relative = f"notes/tier-1-direct-answers/{note_file.name}"
            
            metadata = {
                "type": "direct_answer",
                "question": question_title,
                "file_path": file_path_relative
            }
            
            note_id = note_file.stem
            vectors_to_store.append((
                note_id,
                embedding,
                metadata
            ))
            
        except Exception as e:
            print(f"      ERROR: Failed to process {note_file.name}: {e}")
            continue
    
    if not vectors_to_store:
        print("\nNo valid direct answer files to embed.")
        return
    
    print(f"\nStoring {len(vectors_to_store)} direct answer embeddings...")
    storage.store_notes_batch(vectors_to_store)
    
    print("\nVerifying storage...")
    stats = storage.get_stats()
    print(f"Storage stats: {stats}")
    
    print(f"\n✅ Successfully embedded {len(vectors_to_store)} direct answer questions!")
    print(f"   Storage location: {storage.storage_path}")

if __name__ == "__main__":
    main()

