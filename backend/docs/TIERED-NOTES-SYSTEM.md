# Tiered Notes System - Architecture and Implementation

**Created:** 2026-02-07  
**Purpose:** Document the new cascading fallback system for note retrieval and answer generation

## Problem Statement

### Current Issues

1. **Update Difficulty**: When employment status changes, dates must be updated across 40+ notes
2. **Retrieval Degradation**: Adding information (e.g., C# and Java to languages note) can hurt retrieval for common questions
3. **Quality Inconsistency**: All notes treated equally, but common questions need higher quality than edge cases
4. **Cost**: Every query uses LLM, even for simple questions that could be answered directly

### Core Insight

**Pareto Principle for RAG**: 20% of questions (common recruiter questions) account for 80% of queries. Focus quality and reliability on these, accept "good enough" for edge cases.

## System Architecture

### Cascading Fallback System

The system tries each tier in order, falling back only if confidence is too low:

```
Query → Tier 1 (Direct Answers) → Tier 2 (Current Atomic Notes System)
```

**Key Integration Point**: The existing atomic notes system becomes Tier 2 (fallback). This allows incremental implementation - add direct answers first, existing system handles everything else.

Each tier has a confidence threshold. If similarity score meets threshold, return answer. Otherwise, try next tier.

## Tier 1: Direct Answer Notes

### Purpose

Pre-written, polished answers to common recruiter questions. If query matches closely enough (similarity ≥ 0.75), return answer directly without LLM.

### Benefits

- **Zero cost**: No LLM call needed
- **Instant response**: No generation time
- **High quality**: Hand-crafted, polished answers
- **Reliable**: Consistent answers every time
- **Easy updates**: Update one note per question

### Note Format

```markdown
# What languages do you know?

I know TypeScript, React, C#, Python, Java, and Lua. 

My strongest languages are **TypeScript and React**, which I've used daily for 3.5 years at Nurtur (July 2022 - February 2026). These are where I have the most production experience and can deliver the most value.

I have significant professional experience with **C#** - I used it as my primary backend language for 3 years at Nurtur, working with C# APIs, Azure Functions, and backend systems.

I use **Python** extensively for AI/ML projects, including WhatNow (recommendation system), moh-ami (LLM integration), and Folio (this RAG chatbot). I've been familiar with Python for around 7 years, with focused use in the past year.

**Java** was my first programming language, learned during my Higher Education course and at Heriot Watt University. While I haven't used it professionally in recent years, I have a solid foundational understanding.

**Lua** I'm familiar with through personal projects, used for scripting and automation.

When people ask about my programming languages, I typically emphasize TypeScript and React as my core strengths, with C# and Python as significant professional experience.
```

**Key points:**
- Title is the question it answers
- No metadata needed
- Complete, polished answer
- Handles common variations naturally

### Directory Structure

```
/notes
  /direct-answers/
    - what-languages-do-you-know.md
    - tell-me-about-yourself.md
    - why-did-you-leave-nurtur.md
    - what-is-your-current-employment-status.md
    - do-you-know-csharp.md
    - do-you-know-java.md
    - what-is-your-experience-with-react.md
    - what-is-your-experience-with-python.md
    - what-are-your-strongest-skills.md
    - are-you-open-to-remote-work.md
    - tell-me-about-whatnow.md
    - tell-me-about-moh-ami.md
    - tell-me-about-atlantis.md
    - [20-30 total common questions]
```

### Retrieval Logic

```python
def find_direct_answer(query):
    # Embed the query
    query_embedding = embed(query)
    
    # Search only direct answer notes
    direct_answers = vector_search(
        query_embedding, 
        filter={"type": "direct_answer"},
        k=1
    )
    
    if direct_answers and direct_answers[0].similarity >= 0.75:
        return {
            "answer": direct_answers[0].content,
            "confidence": direct_answers[0].similarity,
            "system": "direct_answers",
            "cost": 0  # No LLM call!
        }
    
    return None  # Fall back to next system
```

### Quality Checklist

For each direct answer note:
- [ ] Answers the question completely
- [ ] Includes relevant context (dates, years, projects)
- [ ] Professional tone
- [ ] Appropriate length (not too brief, not too verbose)
- [ ] Handles common variations ("languages" vs "programming languages")
- [ ] Tested with embedding similarity (should match at 0.75+ for target question)

### Common Questions to Cover

**High Priority (must have direct answers):**
1. "What languages do you know?"
2. "Tell me about yourself"
3. "Why did you leave your last job?"
4. "What's your current employment status?"
5. "Do you know C#?" / "Do you know Java?"
6. "What's your experience with React?"
7. "What's your experience with Python?"
8. "Tell me about WhatNow"
9. "Tell me about moh-ami"
10. "Tell me about Atlantis"
11. "What are your strongest skills?"
12. "Are you open to remote work?"
13. "What's your backend experience?"
14. "What's your frontend experience?"
15. "How long have you been developing?"

**Medium Priority:**
- Project-specific questions
- Technology-specific questions
- Work experience questions

## Tier 2: Current Atomic Notes System (Fallback)

### Purpose

The existing atomic notes system serves as the fallback when direct answers don't match well enough. This is the current system that's already working - no changes needed initially.

### Benefits

- **Already working**: Existing system continues to handle edge cases
- **No migration needed**: Can implement incrementally
- **Comprehensive coverage**: All existing notes remain available
- **Proven reliability**: System already handles complex queries

### Current System Structure

The existing notes in `/notes/` directory:
- `/skills/` - Technical skills and expertise
- `/work/` - Work experience and achievements
- `/values/` - Core values and motivation
- `/background/` - Educational and career background
- `/projects/` - Project deep-dives
- `/career/` - Career goals and preferences
- `/process/` - Problem-solving and work processes
- `/soft-skills/` - Communication and collaboration

### Retrieval Logic

```python
def retrieve_current_system(query):
    """
    Uses existing retrieval system - no changes needed.
    This is the current RAG implementation.
    """
    query_embedding = embed(query)
    
    # Use existing embedding storage and retrieval
    results = embedding_storage.query_similar(
        query_embedding,
        top_k=5  # Current system uses top 5
    )
    
    # Use existing confidence threshold logic
    if results and results[0]['score'] >= 0.40:  # Current threshold
        return {
            "notes": results,
            "confidence": results[0]['score'],
            "system": "current_atomic_notes"
        }
    
    return None
```

### Integration Point

**No changes to existing system required.** The current atomic notes system continues to work exactly as it does now. Direct answers are simply checked first, then fall back to current system if no match.

## Complete Query Flow

```python
def answer_query(query):
    # Tier 1: Direct answers (new system)
    direct_answer = find_direct_answer(query)
    if direct_answer:
        return {
            "answer": direct_answer["answer"],
            "confidence": direct_answer["confidence"],
            "system": "direct_answers",
            "cost": 0  # No LLM call
        }
    
    # Tier 2: Current atomic notes system (existing fallback)
    current_system = retrieve_current_system(query)
    if current_system:
        # Use existing RAG synthesis logic
        return {
            "answer": existing_rag_synthesize(query, current_system["notes"]),
            "confidence": current_system["confidence"],
            "system": "current_atomic_notes"
        }
    
    # Final fallback: Use current system anyway (low confidence)
    return {
        "answer": existing_rag_synthesize(query, current_system["notes"]),
        "confidence": "low",
        "system": "current_atomic_notes_fallback"
    }
```

**Key Integration**: The existing `existing_rag_synthesize()` function continues to work. We just add a check before it runs.

## Embedding Metadata

When embedding notes, include type metadata to distinguish direct answers from existing notes:

```python
# Direct answer notes (new)
metadata = {
    "type": "direct_answer",
    "question": note_title  # "What languages do you know?"
}

# Existing atomic notes (no change needed)
# Current notes already have metadata structure
# They'll be retrieved by existing system if direct answers don't match
```

## Quality Strategy

### Focus Quality on Common Questions

- **Tier 1 (Direct Answers)**: Polish these heavily - they handle 80% of queries
- **Tier 2 (Current System)**: Existing quality maintained - handles edge cases and complex queries

### Update Strategy

**When employment status changes:**
1. Update direct answer: `what-is-your-current-employment-status.md`
2. Update direct answer: `why-did-you-leave-nurtur.md` (if needed)
3. Update fact notes: `nurtur-dates.md`, `nurtur-role.md` (small, easy)
4. Narrative notes: Usually unchanged (tell the story, not current status)

**When adding a language:**
1. Update direct answer: `what-languages-do-you-know.md`
2. Add fact note: `new-language.md` (if needed for synthesis)
3. Narrative notes: Usually unchanged

**Result**: Update 2-3 notes instead of 40+.

## Implementation Plan

### Phase 1: Direct Answer System (New Layer)
1. Create `/notes/direct-answers/` directory
2. Identify top 20-30 common questions
3. Write polished direct answer notes
4. Embed direct answer notes with `type: "direct_answer"` metadata
5. Implement retrieval check before existing system
6. Test similarity scores for target questions
7. Deploy and monitor

### Phase 2: Integration with Current System
1. Modify query handler to check direct answers first
2. If no direct answer match (similarity < 0.75), fall back to existing system
3. Add system tracking (which tier answered)
4. Monitor confidence scores and hit rates
5. Adjust direct answer threshold based on results

### Future Enhancements (Optional)
- Consider granular fact notes if needed
- Consider narrative notes if needed
- But current system works fine as fallback for now

## Success Metrics

- **Direct answer hit rate**: Target 70-80% of queries
- **Cost reduction**: 70-80% reduction (direct answers = $0)
- **Response time**: Direct answers = instant, others = normal
- **Quality**: Direct answers = excellent, others = good enough
- **Update burden**: 2-3 notes per change instead of 40+

## Example Flows

### Example 1: Common Question
**Query:** "What languages do you know?"

1. System 1: Direct answer → similarity=0.92 → Return answer ✓
2. **Result**: Instant, $0 cost, perfect answer

### Example 2: Variation of Common Question
**Query:** "What programming languages are you familiar with?"

1. System 1: Direct answer → similarity=0.78 → Return answer ✓
2. **Result**: Instant, $0 cost, perfect answer (handles variation)

### Example 3: Specific Follow-up
**Query:** "How did you learn TypeScript?"

1. Tier 1: Direct answer → similarity=0.45 → Too low
2. Tier 2: Current system → similarity=0.68 → Use existing RAG synthesis ✓
3. **Result**: Normal cost, good answer from existing atomic notes

### Example 4: Complex Question
**Query:** "Tell me about your journey from art to tech"

1. Tier 1: Direct answer → similarity=0.30 → Too low
2. Tier 2: Current system → similarity=0.71 → Use existing RAG synthesis ✓
3. **Result**: Normal cost, answer from existing notes (artist-to-tech-transition, etc.)

## Integration with Current System

### Key Points

1. **No breaking changes**: Current system continues to work exactly as before
2. **Additive only**: Direct answers are checked first, then fall back to existing system
3. **Incremental**: Can implement and test direct answers without affecting current system
4. **Backward compatible**: If direct answers fail, existing system handles it

### Code Integration Point

The integration happens in the query handler:

```python
# Current flow (no changes needed for existing system)
def chat(request: ChatRequest):
    # NEW: Check direct answers first
    direct_answer = find_direct_answer(request.question)
    if direct_answer and direct_answer.similarity >= 0.75:
        return {
            "answer": direct_answer.content,
            "confidence": direct_answer.similarity,
            "system": "direct_answers"
        }
    
    # EXISTING: Current RAG system (no changes)
    query_embedding = openai_service.get_embedding(request.question)
    similar_notes = embedding_storage.query_similar(query_embedding, top_k=5)
    
    # Existing synthesis logic continues unchanged
    context = format_notes(similar_notes)
    answer = openai_service.generate_chat_response(request.question, context)
    
    return {
        "answer": answer,
        "confidence": similar_notes[0]['score'] if similar_notes else 0,
        "system": "current_atomic_notes"
    }
```

## Next Steps

1. Review this document
2. Create `/notes/direct-answers/` directory
3. Identify top 20-30 common questions for direct answers
4. Start writing direct answer notes
5. Implement Tier 1 retrieval check in query handler
6. Test direct answer matching
7. Monitor hit rates and adjust threshold

