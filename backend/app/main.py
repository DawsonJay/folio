from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    import os
    
    try:
        # Create tables if they don't exist (for minimal setup)
        Base.metadata.create_all(bind=engine)
        
        # Test database connection with a simple query
        db = SessionLocal()
        try:
            count = db.query(TestItem).count()
            return {
                "status": "connected",
                "database_url_set": bool(os.getenv("DATABASE_URL")),
                "test_items_count": count
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "database_url_set": bool(os.getenv("DATABASE_URL"))
            }
        finally:
            db.close()
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "database_url_set": bool(os.getenv("DATABASE_URL"))
        }

