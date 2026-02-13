from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.analytics_service import AnalyticsService

router = APIRouter()

class QuestionCount(BaseModel):
    question: str
    count: int
    last_asked: Optional[str]
    first_asked: Optional[str]

class QuestionCountsResponse(BaseModel):
    questions: List[QuestionCount]
    total_unique: int
    total_questions: int

class ResetResponse(BaseModel):
    deleted_count: int
    message: str

@router.get("/questions", response_model=QuestionCountsResponse)
async def get_question_analytics(
    days: Optional[int] = Query(None, description="Filter questions from last N days"),
    limit: Optional[int] = Query(None, description="Limit number of results"),
    db: Session = Depends(get_db)
):
    analytics_service = AnalyticsService()
    
    questions = analytics_service.get_question_counts(db, days=days, limit=limit)
    total_questions = analytics_service.get_total_questions(db, days=days)
    
    return QuestionCountsResponse(
        questions=[QuestionCount(**q) for q in questions],
        total_unique=len(questions),
        total_questions=total_questions
    )

@router.post("/reset", response_model=ResetResponse)
async def reset_question_analytics(db: Session = Depends(get_db)):
    analytics_service = AnalyticsService()
    deleted_count = analytics_service.reset_questions(db)
    
    return ResetResponse(
        deleted_count=deleted_count,
        message=f"Successfully deleted {deleted_count} question records"
    )

