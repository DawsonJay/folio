from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api.chat import router as chat_router
from pathlib import Path
import os

load_dotenv()

app = FastAPI(
    title="Folio API",
    description="AI-powered portfolio chatbot backend",
    version="0.1.0"
)

@app.on_event("startup")
async def startup_event():
    embeddings_file = Path(__file__).parent.parent / "embeddings.json"
    notes_dir = Path(__file__).parent.parent / "notes"
    
    if not embeddings_file.exists() and notes_dir.exists():
        print("⚠️  embeddings.json not found. Generating embeddings on startup...")
        try:
            from app.services.openai_service import OpenAIService
            from app.services.embedding_storage import LocalEmbeddingStorage
            
            if not os.getenv("OPENAI_API_KEY"):
                print("❌ OPENAI_API_KEY not set. Cannot generate embeddings.")
                return
            
            openai_service = OpenAIService()
            storage = LocalEmbeddingStorage(storage_path=str(embeddings_file))
            
            note_files = list(notes_dir.rglob("*.md"))
            print(f"Found {len(note_files)} note files to embed...")
            
            vectors_to_store = []
            for i, note_file in enumerate(note_files, 1):
                with open(note_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                note_id = note_file.stem
                category = note_file.parent.name
                
                print(f"  [{i}/{len(note_files)}] Embedding: {note_id}")
                embedding = openai_service.get_embedding(content)
                
                metadata = {
                    "category": category,
                    "file_path": str(note_file.relative_to(Path(__file__).parent.parent)),
                    "title": note_id.replace('-', ' ').title(),
                    "content_preview": content[:200]
                }
                
                vectors_to_store.append((note_id, embedding, metadata))
            
            storage.store_notes_batch(vectors_to_store)
            print(f"✅ Generated {len(vectors_to_store)} embeddings successfully!")
        except Exception as e:
            print(f"❌ Error generating embeddings: {e}")
            print("   The API will still start, but chat functionality may be limited.")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routers
app.include_router(chat_router, prefix="/api", tags=["chat"])

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "ok"}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Folio API",
        "version": "0.1.0",
        "status": "running"
    }

@app.get("/db-test")
async def test_database():
    """Test database connection endpoint"""
    from app.database import SessionLocal, engine, Base
    from app.models.test import TestItem
    
    try:
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        count = db.query(TestItem).count()
        db.close()
        return {"status": "connected", "test_items_count": count}
    except Exception as e:
        return {"status": "error", "error": str(e)}

