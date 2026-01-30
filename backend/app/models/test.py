from sqlalchemy import Column, Integer, String
from app.database import Base

class TestItem(Base):
    """Minimal test model to verify database connection"""
    __tablename__ = "test_items"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)







