from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get DATABASE_URL from environment (Railway provides this automatically)
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine (only if DATABASE_URL is set)
if DATABASE_URL:
    # Handle Railway's postgresql:// format - SQLAlchemy needs postgresql+psycopg2://
    if DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)
    
    # Railway PostgreSQL requires SSL - add sslmode if not present
    if "sslmode" not in DATABASE_URL:
        separator = "&" if "?" in DATABASE_URL else "?"
        DATABASE_URL = f"{DATABASE_URL}{separator}sslmode=require"
    
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Verify connections before using
        echo=False  # Set to True for SQL query logging in development
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    engine = None
    SessionLocal = None

# Base class for models
Base = declarative_base()

# Dependency for FastAPI to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

