# Confidence Threshold Implementation Guide

Practical guide for implementing and maintaining the confidence threshold system in Folio's RAG architecture.

## Quick Reference

```python
CONFIDENCE_THRESHOLD = 0.40

if top_score >= 0.40:
    # Generate detailed answer (500 tokens max)
    mode = "full_answer"
else:
    # Generate redirect response (200 tokens max)
    mode = "redirect"
```

## Architecture Overview

### Components

1. **Embedding Storage Service** (`embedding_storage.py`)
   - Returns similarity scores with retrieved notes
   - No modifications needed (already returns scores)

2. **OpenAI Service** (`openai_service.py`)
   - Two response generation methods:
     - `generate_chat_response()` - Full answers
     - `generate_redirect_response()` - Redirects with suggestions

3. **Chat Endpoint** (`api/chat.py`)
   - Routes based on confidence score
   - Returns confidence metadata in response

### Data Flow

```
User Question
    ↓
Embed Question
    ↓
Retrieve Top 5 Notes + Scores
    ↓
Check Top Score
    ↓
    ├─ High (≥0.40) → Full Answer (500 tokens)
    └─ Low (<0.40)  → Redirect (200 tokens)
    ↓
Return Response + Confidence Metadata
```

## Implementation Steps

### Step 1: Update OpenAI Service

Add a second generation method for low-confidence responses.

**File: `backend/app/services/openai_service.py`**

```python
class OpenAIService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = OpenAI(api_key=api_key)
        self.embedding_model = "text-embedding-3-small"
        self.chat_model = "gpt-4o-mini"
    
    def generate_chat_response(self, prompt: str, context: str) -> str:
        """Generate full detailed answer (high confidence)"""
        messages = [
            {
                "role": "system", 
                "content": "You are a helpful assistant answering questions about James Dawson's background, skills, and projects. Use the provided context to give accurate, personalized responses in first person as if you are James."
            },
            {
                "role": "user", 
                "content": f"Context:\n{context}\n\nQuestion: {prompt}"
            }
        ]
        
        response = self.client.chat.completions.create(
            model=self.chat_model,
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    
    def generate_redirect_response(self, question: str, weak_context: str) -> str:
        """Generate redirect response with suggestions (low confidence)"""
        messages = [
            {
                "role": "system",
                "content": """You are a helpful assistant for James Dawson's portfolio chatbot. 
When you don't have enough information to fully answer a question, acknowledge 
this honestly but helpfully suggest 2-3 specific related questions that you 
CAN answer well based on the weak context provided."""
            },
            {
                "role": "user",
                "content": f"""Question: {question}

Available context (limited):
{weak_context}

I don't have enough detailed information to fully answer this question. 
Based on what limited context I do have, please:
1. Briefly acknowledge what the question is asking about
2. Mention what related information I DO have (based on context)
3. Suggest 2-3 specific alternative questions I can answer well

Keep the response friendly, honest, and helpful. Make it clear James can 
discuss this topic in detail during an actual interview."""
            }
        ]
        
        response = self.client.chat.completions.create(
            model=self.chat_model,
            messages=messages,
            temperature=0.7,
            max_tokens=200
        )
        
        return response.choices[0].message.content
```

### Step 2: Update Chat Endpoint

Add confidence-based routing logic.

**File: `backend/app/api/chat.py`**

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.openai_service import OpenAIService
from app.services.embedding_storage import LocalEmbeddingStorage

router = APIRouter()

CONFIDENCE_THRESHOLD = 0.40

class ChatRequest(BaseModel):
    question: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    suggestions: List[str]
    confidence: str
    top_score: float
    mode: str

openai_service = OpenAIService()
embedding_storage = LocalEmbeddingStorage()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # 1. Embed question
        query_embedding = openai_service.get_embedding(request.question)
        
        # 2. Retrieve similar notes
        similar_notes = embedding_storage.find_similar_notes(
            query_embedding, 
            k=5
        )
        
        if not similar_notes:
            raise HTTPException(
                status_code=500, 
                detail="No notes found in knowledge base"
            )
        
        # 3. Extract top score
        top_score = similar_notes[0]['score']
        
        # 4. Build context from retrieved notes
        context_parts = []
        for note in similar_notes:
            note_content = note['metadata'].get('content_preview', '')
            context_parts.append(note_content)
        context = "\n\n".join(context_parts)
        
        # 5. Route based on confidence
        if top_score >= CONFIDENCE_THRESHOLD:
            # HIGH CONFIDENCE: Generate detailed answer
            answer = openai_service.generate_chat_response(
                prompt=request.question,
                context=context
            )
            
            # TODO: Generate contextual suggestions based on answer
            suggestions = [
                "Tell me more about that",
                "What was the biggest challenge?",
                "How did you approach this?"
            ]
            
            return ChatResponse(
                answer=answer,
                suggestions=suggestions,
                confidence="high",
                top_score=top_score,
                mode="direct_answer"
            )
        
        else:
            # LOW CONFIDENCE: Generate redirect
            answer = openai_service.generate_redirect_response(
                question=request.question,
                weak_context=context
            )
            
            # TODO: Extract suggested questions from answer or generate them
            suggestions = [
                "What projects have you built?",
                "Tell me about your technical skills",
                "What's your experience with AI?"
            ]
            
            return ChatResponse(
                answer=answer,
                suggestions=suggestions,
                confidence="low",
                top_score=top_score,
                mode="redirect"
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Step 3: Create Test Script

Test the system with known weak questions from the 200-question tests.

**File: `backend/scripts/test_confidence_threshold.py`**

```python
import sys
from pathlib import Path
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent))

from app.services.openai_service import OpenAIService
from app.services.embedding_storage import LocalEmbeddingStorage

load_dotenv()

EMBEDDINGS_FILE = Path(__file__).parent.parent / "embeddings.json"
CONFIDENCE_THRESHOLD = 0.40

WEAK_QUESTIONS = [
    "What's your typical workday like?",
    "What conferences do you attend?",
    "What's your strongest programming language?",
    "How do you organize your tasks?",
    "What's your management style?",
    "Describe a time you missed a deadline",
    "What are your salary expectations?",
    "What questions do you have for us?",
    "Tell me about a time you had to learn something quickly",
    "How would your colleagues describe you?",
]

STRONG_QUESTIONS = [
    "Tell me about WhatNow",
    "What's your Python experience?",
    "How do you approach problem-solving?",
    "Tell me about your React experience",
    "Why did you build your portfolio projects?",
]

def test_question(question: str, openai_service, embedding_storage):
    print(f"\n{'='*80}")
    print(f"Q: {question}")
    print(f"{'='*80}\n")
    
    query_embedding = openai_service.get_embedding(question)
    similar_notes = embedding_storage.find_similar_notes(query_embedding, k=5)
    
    top_score = similar_notes[0]['score'] if similar_notes else 0
    
    print(f"Top Score: {top_score:.4f}")
    print(f"Confidence: {'HIGH' if top_score >= CONFIDENCE_THRESHOLD else 'LOW'}")
    print(f"Mode: {'full_answer' if top_score >= CONFIDENCE_THRESHOLD else 'redirect'}\n")
    
    context_parts = []
    for i, note in enumerate(similar_notes):
        print(f"{i+1}. {note['note_id']} ({note['score']:.4f})")
        context_parts.append(note['metadata'].get('content_preview', ''))
    
    context = "\n\n".join(context_parts)
    
    if top_score >= CONFIDENCE_THRESHOLD:
        print("\n--- FULL ANSWER ---")
        answer = openai_service.generate_chat_response(question, context)
    else:
        print("\n--- REDIRECT RESPONSE ---")
        answer = openai_service.generate_redirect_response(question, context)
    
    print(answer)
    
    return top_score

def main():
    print("Initializing services...")
    openai_service = OpenAIService()
    embedding_storage = LocalEmbeddingStorage(storage_path=str(EMBEDDINGS_FILE))
    
    print(f"\nLoaded {embedding_storage.count_notes()} notes")
    print(f"Confidence Threshold: {CONFIDENCE_THRESHOLD}\n")
    
    print("\n" + "="*80)
    print("TESTING WEAK QUESTIONS (Expected: Low Confidence)")
    print("="*80)
    
    weak_scores = []
    for q in WEAK_QUESTIONS:
        score = test_question(q, openai_service, embedding_storage)
        weak_scores.append(score)
    
    print("\n" + "="*80)
    print("TESTING STRONG QUESTIONS (Expected: High Confidence)")
    print("="*80)
    
    strong_scores = []
    for q in STRONG_QUESTIONS:
        score = test_question(q, openai_service, embedding_storage)
        strong_scores.append(score)
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    avg_weak = sum(weak_scores) / len(weak_scores) if weak_scores else 0
    avg_strong = sum(strong_scores) / len(strong_scores) if strong_scores else 0
    
    weak_below_threshold = sum(1 for s in weak_scores if s < CONFIDENCE_THRESHOLD)
    strong_above_threshold = sum(1 for s in strong_scores if s >= CONFIDENCE_THRESHOLD)
    
    print(f"\nWeak Questions:")
    print(f"  Average Score: {avg_weak:.4f}")
    print(f"  Below Threshold: {weak_below_threshold}/{len(weak_scores)}")
    
    print(f"\nStrong Questions:")
    print(f"  Average Score: {avg_strong:.4f}")
    print(f"  Above Threshold: {strong_above_threshold}/{len(strong_scores)}")
    
    print(f"\nThreshold Effectiveness:")
    weak_accuracy = (weak_below_threshold / len(weak_scores)) * 100
    strong_accuracy = (strong_above_threshold / len(strong_scores)) * 100
    print(f"  Correctly identified weak: {weak_accuracy:.1f}%")
    print(f"  Correctly identified strong: {strong_accuracy:.1f}%")
    
    print("\n✅ Test complete!")

if __name__ == "__main__":
    main()
```

### Step 4: Run Tests

```bash
cd backend
source venv/bin/activate
python scripts/test_confidence_threshold.py
```

Expected output:
- Weak questions should trigger redirect responses
- Strong questions should trigger full answers
- Redirect responses should suggest alternative questions
- Full answers should be detailed and personalized

## Tuning the Threshold

### How to Adjust

If test results show poor performance:

**Too many false positives (good questions getting redirects):**
- Lower the threshold (e.g., 0.35)
- More questions get full answers

**Too many false negatives (weak questions getting full answers):**
- Raise the threshold (e.g., 0.45)
- More questions get redirects

### Evaluation Criteria

A good threshold should:
1. Route 70-85% of questions to full answers (high coverage)
2. Catch genuinely weak questions (quality control)
3. Produce helpful redirects (not generic "I don't know")
4. Minimize false positives (don't redirect answerable questions)

### Testing Process

1. Run test script with current threshold
2. Manually review 10-15 responses near the threshold boundary
3. Identify misclassified questions
4. Adjust threshold in 0.05 increments
5. Re-run and evaluate

## Response Quality Guidelines

### Good Full Answers

✅ Uses specific information from notes
✅ Maintains first-person voice
✅ Connects information coherently
✅ Answers the question directly

### Good Redirect Responses

✅ Acknowledges what the question asks
✅ Mentions related topics that ARE covered
✅ Suggests 2-3 specific alternative questions
✅ Maintains friendly, helpful tone
✅ References ability to discuss in interview

### Bad Responses to Avoid

❌ Generic "I don't know" without alternatives
❌ Hallucinated information not in notes
❌ Vague answers that don't help user
❌ Overly apologetic tone
❌ Suggesting unrelated topics

## Cost Analysis

### Token Usage

**High Confidence (Full Answer):**
- System prompt: ~100 tokens
- User prompt + context: ~800 tokens
- Response: ~400 tokens
- **Total: ~1,300 tokens per request**

**Low Confidence (Redirect):**
- System prompt: ~100 tokens
- User prompt + context: ~400 tokens
- Response: ~150 tokens
- **Total: ~650 tokens per request**

**Savings: ~50% per low-confidence request**

### Cost Estimate

Assuming 1000 questions with 20% low confidence:

**Without threshold:**
- 1000 × 1,300 tokens = 1,300,000 tokens
- Cost: ~$0.26

**With threshold:**
- 800 high × 1,300 tokens = 1,040,000 tokens
- 200 low × 650 tokens = 130,000 tokens
- Total: 1,170,000 tokens
- Cost: ~$0.23
- **Savings: $0.03 (12%)** + improved quality

## Monitoring and Analytics

### Metrics to Track

1. **Confidence Distribution**
   - Percentage of high vs low confidence responses
   - Average scores for each category

2. **Response Quality**
   - User satisfaction ratings
   - Follow-up question patterns
   - Session duration

3. **Threshold Effectiveness**
   - False positive rate (good questions redirected)
   - False negative rate (weak questions answered)
   - Redirect suggestion relevance

### Logging

Add logging to track confidence routing:

```python
import logging

logger = logging.getLogger(__name__)

# In chat endpoint:
logger.info(f"Question: {question[:50]}... | Score: {top_score:.4f} | Mode: {mode}")
```

## Frontend Integration

### Response Format

```typescript
interface ChatResponse {
  answer: string;
  suggestions: string[];
  confidence: 'high' | 'low';
  top_score: number;
  mode: 'direct_answer' | 'redirect';
}
```

### UI Considerations

**High Confidence:**
- Display answer normally
- Standard suggestion chips

**Low Confidence:**
- Optional: Show subtle indicator (e.g., icon)
- Make suggestion chips more prominent
- Consider different styling for redirect responses

## Future Enhancements

### Graduated Confidence Tiers

Instead of binary high/low, implement multiple tiers:

```python
if top_score >= 0.70:
    mode = "excellent"      # Full answer, 500 tokens
elif top_score >= 0.50:
    mode = "good"           # Full answer, 400 tokens
elif top_score >= 0.35:
    mode = "adequate"       # Brief answer, 300 tokens
else:
    mode = "redirect"       # Redirect, 200 tokens
```

### Context-Aware Thresholding

Adjust threshold based on conversation context:

```python
if is_follow_up_question(conversation_history):
    threshold = 0.35  # Lower threshold for follow-ups
else:
    threshold = 0.40  # Standard threshold
```

### Dynamic Suggestions

Extract suggested questions from LLM redirect response:

```python
def parse_suggestions(redirect_response: str) -> List[str]:
    # Parse LLM response for suggested questions
    # Extract bullet points or numbered lists
    # Return as list of strings
    pass
```

## Troubleshooting

### Issue: Too many redirects

**Symptoms:** Most questions getting low confidence
**Causes:** Threshold too high, insufficient notes
**Solutions:**
- Lower threshold to 0.35
- Add more atomic notes
- Check note quality and coverage

### Issue: Poor redirect suggestions

**Symptoms:** Suggested questions aren't relevant
**Causes:** Weak context, poor prompt design
**Solutions:**
- Improve redirect prompt
- Include more context in prompt
- Add examples to prompt

### Issue: Hallucination in full answers

**Symptoms:** Answers contain false information
**Causes:** Threshold too low, poor note quality
**Solutions:**
- Raise threshold to 0.45
- Review and improve note content
- Add explicit "don't invent" instruction to prompt

### Issue: False positive profanity detection

**Symptoms:** Legitimate questions trigger boundary response
**Causes:** Standalone insult words in technical context
**Examples:**
- "How does garbage collection work?" (contains "garbage")
- "Are there stupid questions?" (contains "stupid")
- "When is a try-catch useless?" (contains "useless")

**Solutions:**
- Add context-aware patterns (e.g., whitelist "garbage collection")
- Remove standalone insult words, keep only contextual patterns
- Log false positives and refine patterns iteratively
- Consider ML-based toxicity detection for nuanced filtering

**Note:** In testing (220+ questions), no false positives were observed. The risk is theoretical but worth monitoring in production.

## Summary

The confidence threshold system provides:
- ✅ Quality control for RAG responses
- ✅ Honest handling of knowledge gaps
- ✅ Strategic redirection to strengths
- ✅ Cost optimization
- ✅ Better user experience

Key implementation points:
1. Add dual-mode generation to OpenAI service
2. Implement routing logic in chat endpoint
3. Test with known weak/strong questions
4. Tune threshold based on results
5. Monitor and iterate

For questions or issues, refer to the technical specification in `ATOMIC-NOTES-TECHNICAL.md`.

