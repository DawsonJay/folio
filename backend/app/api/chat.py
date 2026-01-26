import asyncio
from typing import List
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Suggestion(BaseModel):
    text: str

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    suggestions: List[Suggestion]

class SuggestionsResponse(BaseModel):
    suggestions: List[Suggestion]

INITIAL_SUGGESTIONS = [
    {"text": "What technologies did you use?"},
    {"text": "What can you build?"},
    {"text": "How long did that take?"},
    {"text": "What was your role in this project?"},
    {"text": "Show me your best work"},
    {"text": "What problems did you solve?"}
]

FOLLOW_UP_SUGGESTIONS = [
    {"text": "Tell me more about that"},
    {"text": "What was the biggest challenge?"},
    {"text": "Can you show me an example?"},
    {"text": "How did you handle that?"},
    {"text": "What did you learn from this?"},
    {"text": "What would you do differently?"}
]

@router.get("/suggestions", response_model=SuggestionsResponse)
async def get_suggestions():
    await asyncio.sleep(1)
    return SuggestionsResponse(suggestions=[Suggestion(**s) for s in INITIAL_SUGGESTIONS])

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    await asyncio.sleep(3)
    return ChatResponse(
        answer="I'm a full-stack developer with experience in React, TypeScript, Python, and FastAPI. I've built several portfolio projects including this chatbot interface.",
        suggestions=[Suggestion(**s) for s in FOLLOW_UP_SUGGESTIONS]
    )

