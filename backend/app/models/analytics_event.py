from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base

class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"
    
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), index=True)
    session_id = Column(String, nullable=True, index=True)
    
    question_text = Column(Text, nullable=True)
    answer_text = Column(Text, nullable=True)
    
    confidence = Column(String, nullable=True)
    top_score = Column(Float, nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    
    event_metadata = Column(JSON, nullable=True)

