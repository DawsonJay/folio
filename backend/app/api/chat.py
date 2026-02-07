import asyncio
from typing import List, Optional, Dict, Literal
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Suggestion(BaseModel):
    text: str

class ProjectLinks(BaseModel):
    demo: Optional[str] = None
    github: Optional[str] = None

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    emotion: Literal['happy', 'thinking', 'surprised', 'derp', 'tired', 'annoyed']
    suggestions: List[Suggestion]
    projectLinks: Optional[Dict[str, ProjectLinks]] = None
    confidence: Optional[str] = None
    top_score: Optional[float] = None

class SuggestionsResponse(BaseModel):
    suggestions: List[Suggestion]

INITIAL_SUGGESTIONS = [
    {"text": "What is Folio?"},
    {"text": "Tell me about your current experience"},
    {"text": "Why are you looking for a new role?"},
    {"text": "What are your strongest technical skills?"},
    {"text": "Tell me about a project you're proud of"},
    {"text": "What are you looking for in your next role?"}
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
    from app.services.openai_service import OpenAIService
    from app.services.embedding_storage import LocalEmbeddingStorage
    from app.services.profanity_filter import ProfanityFilter
    from app.services.project_links import extract_project_links
    from pathlib import Path
    
    VERY_LOW_THRESHOLD = 0.20
    CONFIDENCE_HIGH = 0.40
    CONFIDENCE_MEDIUM = 0.30
    EMBEDDINGS_FILE = Path(__file__).parent.parent.parent / "embeddings.json"
    
    openai_service = OpenAIService()
    embedding_storage = LocalEmbeddingStorage(storage_path=str(EMBEDDINGS_FILE))
    profanity_filter = ProfanityFilter()
    
    profanity_check = profanity_filter.check_question(request.question)
    
    if profanity_check["has_profanity"]:
        result = openai_service.generate_boundary_response()
        return ChatResponse(
            answer=result["answer"],
            emotion=result["emotion"],
            suggestions=[Suggestion(**s) for s in result["suggestions"]],
            confidence="boundary",
            top_score=0.0
        )
    
    query_embedding = openai_service.get_embedding(request.question)
    similar_notes = embedding_storage.query_similar(query_embedding, top_k=5)
    
    if not similar_notes:
        result = openai_service.generate_off_topic_response()
        return ChatResponse(
            answer=result["answer"],
            emotion=result["emotion"],
            suggestions=[Suggestion(**s) for s in result["suggestions"]],
            confidence="off_topic",
            top_score=0.0
        )
    
    top_score = similar_notes[0]['score']
    
    if top_score < VERY_LOW_THRESHOLD:
        result = openai_service.generate_off_topic_response()
        return ChatResponse(
            answer=result["answer"],
            emotion=result["emotion"],
            suggestions=[Suggestion(**s) for s in result["suggestions"]],
            confidence="off_topic",
            top_score=top_score
        )
    
    context_parts = []
    note_ids = []
    for note in similar_notes:
        note_id = note['id']
        note_ids.append(note_id)
        content = note['metadata'].get('content_preview', '')
        context_parts.append(content)
    
    context = "\n\n".join(context_parts)
    
    project_links = extract_project_links(note_ids[:3])
    
    # Confidence tiers (defined at top of file):
    # >= 0.4: High confidence - full answer
    # 0.3 - 0.4: Medium confidence - qualified answer with acknowledgment
    # < 0.3: Low confidence - redirect
    
    if top_score < CONFIDENCE_MEDIUM:
        result = openai_service.generate_redirect_response(request.question, context)
        return ChatResponse(
            answer=result["answer"],
            emotion=result["emotion"],
            suggestions=[Suggestion(**s) for s in result["suggestions"]],
            confidence="redirect",
            top_score=top_score
        )
    
    # Medium confidence (0.3-0.4): Provide answer with qualification
    if top_score < CONFIDENCE_HIGH:
        qualification = "The question is a little vague - I'm better with more specific questions, but I'll try my best:"
        result = openai_service.generate_chat_response(
            request.question, 
            context, 
            project_links,
            qualification=qualification
        )
        
        project_links_response = None
        if result.get("projectLinks"):
            project_links_response = {
                k: ProjectLinks(**v) for k, v in result["projectLinks"].items()
            }
        
        return ChatResponse(
            answer=result["answer"],
            emotion=result["emotion"],
            suggestions=[Suggestion(**s) for s in result["suggestions"]],
            projectLinks=project_links_response,
            confidence="medium",
            top_score=top_score
        )
    
    # High confidence (>= 0.4): Full answer
    result = openai_service.generate_chat_response(request.question, context, project_links)
    
    project_links_response = None
    if result.get("projectLinks"):
        project_links_response = {
            k: ProjectLinks(**v) for k, v in result["projectLinks"].items()
        }
    
    return ChatResponse(
        answer=result["answer"],
        emotion=result["emotion"],
        suggestions=[Suggestion(**s) for s in result["suggestions"]],
        projectLinks=project_links_response,
        confidence="high",
        top_score=top_score
    )

