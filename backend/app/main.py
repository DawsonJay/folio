from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api.chat import router as chat_router

load_dotenv()

app = FastAPI(
    title="Folio API",
    description="AI-powered portfolio chatbot backend",
    version="0.1.0"
)


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

