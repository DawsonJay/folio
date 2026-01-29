# Folio Backend Documentation

Complete documentation for the Folio RAG (Retrieval Augmented Generation) backend system.

## Documentation Index

### Core Documentation

**[PROMPT-DESIGN.md](PROMPT-DESIGN.md)** - Ultra-compressed prompts and JSON response structure
- Full answer and redirect prompts
- Emotion selection system
- Project links integration
- Token optimization (76% reduction)
- Cost analysis

**[ATOMIC-NOTES-GUIDE.md](ATOMIC-NOTES-GUIDE.md)** - Practical guide for writing atomic notes
- Principles for effective notes
- Structure and formatting
- Examples and best practices
- Size recommendations (200-500 tokens)

**[ATOMIC-NOTES-TECHNICAL.md](ATOMIC-NOTES-TECHNICAL.md)** - Technical specification for RAG system
- How embeddings work
- Semantic search explanation
- RAG architecture
- Confidence threshold strategy
- Performance considerations

### Implementation Guides

**[CONFIDENCE-THRESHOLD-GUIDE.md](CONFIDENCE-THRESHOLD-GUIDE.md)** - 4-tier response routing implementation
- Profanity detection
- Off-topic handling
- Weak coverage redirects
- Full answer routing
- Testing and tuning

**[PROFANITY-FILTER-NOTES.md](PROFANITY-FILTER-NOTES.md)** - Profanity filter design and analysis
- Text-based vs embedding-based approaches
- False positive analysis
- Pattern categories
- Testing results

**[CONFIDENCE-THRESHOLD-PLAN.md](CONFIDENCE-THRESHOLD-PLAN.md)** - Strategic plan for confidence thresholds
- Problem statement
- Solution design
- Implementation timeline
- Success criteria

### Backend Setup

**[BACKEND-TODOS.md](BACKEND-TODOS.md)** - Development task list
- Database models
- API endpoints
- Services implementation
- Testing requirements

**[../SETUP-INSTRUCTIONS.md](../SETUP-INSTRUCTIONS.md)** - Setup guide
- Environment configuration
- Dependencies
- Running locally

## Quick Start

### Understanding the System

1. **Start here:** [PROMPT-DESIGN.md](PROMPT-DESIGN.md) - Learn about the ultra-compressed prompts and JSON responses
2. **Then read:** [ATOMIC-NOTES-GUIDE.md](ATOMIC-NOTES-GUIDE.md) - Understand how to write effective notes
3. **Deep dive:** [ATOMIC-NOTES-TECHNICAL.md](ATOMIC-NOTES-TECHNICAL.md) - Technical details of embeddings and RAG

### Implementing Features

1. **Confidence thresholds:** [CONFIDENCE-THRESHOLD-GUIDE.md](CONFIDENCE-THRESHOLD-GUIDE.md)
2. **Profanity filtering:** [PROFANITY-FILTER-NOTES.md](PROFANITY-FILTER-NOTES.md)
3. **Testing:** See test results in `backend/TEST-RESULTS-*.md`

## System Overview

### RAG Architecture

```
Question → Profanity Check → Embed → Retrieve Notes → Route by Confidence
                ↓                                              ↓
         Boundary Response                    ┌───────────────┼───────────────┐
                                              ↓               ↓               ↓
                                        Off-Topic      Redirect        Full Answer
                                        (< 0.20)      (0.20-0.39)       (≥ 0.40)
                                              ↓               ↓               ↓
                                        Static         LLM (200)       LLM (700)
                                              ↓               ↓               ↓
                                        JSON Response with emotion, suggestions, links
```

### Key Features

- **Ultra-compressed prompts**: 76% token reduction (850 → 200 tokens)
- **JSON mode responses**: Reliable structured output
- **Emotion system**: 6 avatar emotions drive UI
- **Project links**: Auto-included when discussing projects
- **6 suggestions**: Contextual follow-up questions per response
- **4-tier routing**: Profanity, off-topic, redirect, full answer
- **Local storage**: JSON file with NumPy for similarity search
- **120 atomic notes**: Comprehensive knowledge base

### Response Structure

```json
{
  "answer": "Main response text (300-400 words)",
  "emotion": "happy|thinking|surprised|derp|tired|annoyed",
  "suggestions": [
    {"text": "Follow-up question 1"},
    {"text": "Follow-up question 2"},
    {"text": "Follow-up question 3"},
    {"text": "Follow-up question 4"},
    {"text": "Follow-up question 5"},
    {"text": "Follow-up question 6"}
  ],
  "projectLinks": {
    "ProjectName": {
      "demo": "https://...",
      "github": "https://..."
    }
  }
}
```

## Test Results

### Latest Performance

- **Overall System Accuracy:** 85% (enhanced tier routing)
- **Profanity Detection:** 100% (5/5 test cases)
- **Off-Topic Detection:** 80% (4/5 test cases)
- **Full Answer Routing:** 100% (5/5 test cases)
- **Note Coverage Score:** 3.77/5.0 (113 notes)
- **Cost per 100 queries:** ~$0.023

### Test Documentation

- `backend/TEST-RESULTS-ENHANCED-TIERS.md` - 4-tier routing validation
- `backend/TEST-RESULTS-100-ANALYSIS.md` - Comprehensive coverage test
- `backend/TEST-RESULTS-IMPROVEMENT-SUMMARY.md` - Before/after comparison
- `backend/TEST-RESULTS-FINAL.md` - Final gap-filling results

## Cost Analysis

### Per Request

**Full Answer (79% of requests):**
- Prompt: ~200 tokens
- Context: ~1,200 tokens
- Output: ~500 tokens
- **Cost: ~$0.00038 per request**

**Redirect (21% of requests):**
- Prompt: ~135 tokens
- Context: ~650 tokens
- Output: ~250 tokens
- **Cost: ~$0.00021 per request**

**Static Responses (Profanity/Off-topic):**
- **Cost: $0 (no LLM call)**

### Monthly Estimates

For 1,000 queries:
- ~$0.023/month (highly sustainable)

## Development Status

See [../../IMPLEMENTATION-STATUS.md](../../IMPLEMENTATION-STATUS.md) for current development status and next steps.

## Contributing

When adding notes:
1. Follow [ATOMIC-NOTES-GUIDE.md](ATOMIC-NOTES-GUIDE.md) principles
2. Keep notes 200-500 tokens
3. Use natural language with synonyms
4. Test retrieval with relevant questions
5. Re-embed after changes

When updating prompts:
1. Maintain token efficiency
2. Test with JSON mode
3. Validate emotion selection
4. Ensure 6 suggestions per response
5. Document changes

## Questions?

For detailed implementation questions, see the specific guides listed above. For system architecture questions, start with [ATOMIC-NOTES-TECHNICAL.md](ATOMIC-NOTES-TECHNICAL.md).

