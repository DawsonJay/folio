from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.analytics_event import AnalyticsEvent

class AnalyticsService:
    
    @staticmethod
    def log_question(
        db: Session,
        question: str,
        session_id: str,
        confidence: Optional[str] = None,
        top_score: Optional[float] = None,
        response_time_ms: Optional[int] = None,
        answer: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        event_metadata: Optional[Dict[str, Any]] = None
    ) -> AnalyticsEvent:
        event = AnalyticsEvent(
            event_type="question_asked",
            question_text=question,
            answer_text=answer,
            session_id=session_id,
            confidence=confidence,
            top_score=top_score,
            response_time_ms=response_time_ms,
            ip_address=ip_address,
            user_agent=user_agent,
            event_metadata=event_metadata
        )
        
        db.add(event)
        db.commit()
        db.refresh(event)
        
        return event
    
    @staticmethod
    def get_question_counts(
        db: Session,
        days: Optional[int] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        query = db.query(
            AnalyticsEvent.question_text,
            func.count(AnalyticsEvent.id).label('count'),
            func.max(AnalyticsEvent.timestamp).label('last_asked'),
            func.min(AnalyticsEvent.timestamp).label('first_asked')
        ).filter(
            AnalyticsEvent.event_type == 'question_asked',
            AnalyticsEvent.question_text.isnot(None)
        )
        
        if days:
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
            query = query.filter(AnalyticsEvent.timestamp >= cutoff_date)
        
        query = query.group_by(AnalyticsEvent.question_text).order_by(
            func.count(AnalyticsEvent.id).desc()
        )
        
        if limit:
            query = query.limit(limit)
        
        results = query.all()
        
        return [
            {
                "question": row.question_text,
                "count": row.count,
                "last_asked": row.last_asked.isoformat() if row.last_asked else None,
                "first_asked": row.first_asked.isoformat() if row.first_asked else None
            }
            for row in results
        ]
    
    @staticmethod
    def reset_questions(db: Session) -> int:
        count = db.query(AnalyticsEvent).filter(
            AnalyticsEvent.event_type == 'question_asked'
        ).delete()
        db.commit()
        return count
    
    @staticmethod
    def get_total_questions(db: Session, days: Optional[int] = None) -> int:
        query = db.query(func.count(AnalyticsEvent.id)).filter(
            AnalyticsEvent.event_type == 'question_asked'
        )
        
        if days:
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
            query = query.filter(AnalyticsEvent.timestamp >= cutoff_date)
        
        return query.scalar()

