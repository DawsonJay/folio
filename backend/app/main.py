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
    import os
    import traceback
    
    try:
        database_url = os.getenv("DATABASE_URL")
        
        # Check if DATABASE_URL is set
        if not database_url:
            return {
                "status": "error",
                "error": "DATABASE_URL environment variable not set",
                "database_url_set": False
            }
        
        # Import database components
        try:
            from app.database import SessionLocal, engine, Base
            from app.models.test import TestItem
        except Exception as import_error:
            return {
                "status": "error",
                "error": f"Import error: {str(import_error)}",
                "traceback": traceback.format_exc()
            }
        
        # Check if engine and SessionLocal are initialized
        if not engine or not SessionLocal:
            return {
                "status": "error",
                "error": "Database engine not initialized",
                "database_url_set": True,
                "database_url_preview": database_url[:20] + "..." if database_url else None
            }
        
        try:
            # Create tables if they don't exist (for minimal setup)
            Base.metadata.create_all(bind=engine)
            
            # Test database connection with a simple query
            db = SessionLocal()
            try:
                count = db.query(TestItem).count()
                return {
                    "status": "connected",
                    "database_url_set": True,
                    "test_items_count": count
                }
            except Exception as query_error:
                return {
                    "status": "error",
                    "error": f"Query error: {str(query_error)}",
                    "error_type": type(query_error).__name__,
                    "traceback": traceback.format_exc()
                }
            finally:
                db.close()
        except Exception as connection_error:
            return {
                "status": "error",
                "error": f"Connection error: {str(connection_error)}",
                "error_type": type(connection_error).__name__,
                "traceback": traceback.format_exc()
            }
    except Exception as e:
        return {
            "status": "error",
            "error": f"Unexpected error: {str(e)}",
            "error_type": type(e).__name__,
            "traceback": traceback.format_exc()
        }

