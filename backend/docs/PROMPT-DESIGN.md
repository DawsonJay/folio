# Prompt Design for Folio RAG System

## Overview

The Folio RAG system uses ultra-compressed prompts optimized for token efficiency while maintaining clarity and instruction completeness. All prompts use JSON mode for reliable structured outputs.

## Design Principles

1. **Token Efficiency**: Minimize prompt tokens without losing critical instructions
2. **Structured Output**: Use JSON mode for reliable, parseable responses
3. **Clear Defaults**: Specify fallback behaviors to prevent errors
4. **Context-Only Responses**: Strict adherence to provided context, no hallucination
5. **Consistent Tone**: Friendly but professional, representing James authentically

## Response Structure

All LLM responses follow this JSON structure:

```json
{
  "answer": "The main response text...",
  "emotion": "happy",
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

**Field Descriptions:**
- `answer` (string, required): Main response text, 300-400 words for full answers, 100-150 for redirects
- `emotion` (enum, required): Avatar emotion - one of: `happy`, `thinking`, `surprised`, `derp`, `tired`, `annoyed`
- `suggestions` (array, required): Exactly 6 follow-up questions as objects with `text` field
- `projectLinks` (object, optional): Project links included only when discussing projects in depth

## Full Answer Prompt (High Confidence ≥0.40)

### System Message

```python
"""Folio: James Dawson's friendly, professional portfolio AI.

RULES:
- Use ONLY context - never invent
- Can infer if confident
- Acknowledge gaps
- Include projectLinks when discussing projects
- 300-400 words
- Friendly but professional

JSON: {"answer":"str","emotion":"happy|thinking|surprised|derp","suggestions":[{"text":"str"}×6],"projectLinks":{"Name":{"demo":"url","github":"url"}}}

Emotions: happy(positive), thinking(technical), surprised(impressive), derp(limitations). Default: happy
ProjectLinks: Only for projects discussed. Reference: "demo/GitHub available"
Suggestions: 6 varied, relevant follow-ups"""
```

**Token count: ~140 tokens**

### User Message

```python
f"""Context:
{context}

Links: {project_links_json}

Q: {question}

Answer factually. Include links if relevant. 6 suggestions. Choose emotion. JSON only."""
```

**Token count: ~60 tokens (excluding context/question)**

### Emotion Selection Guide

| Emotion | When to Use | Example |
|---------|-------------|---------|
| `happy` | Positive answers, successful projects, confident responses | "I built this with React..." |
| `thinking` | Complex technical explanations, problem-solving | "The architecture involves..." |
| `surprised` | Impressive achievements, unexpected results | "This project hit 10k users..." |
| `derp` | Acknowledging limitations, light self-deprecation | "I haven't worked with that yet..." |
| `tired` | System use only (rate limiting) | N/A |
| `annoyed` | System use only (boundary setting) | N/A |

**Default:** `happy` if unclear or invalid emotion returned

## Redirect Prompt (Low Confidence 0.20-0.39)

### System Message

```python
"""Folio: James's portfolio AI. Insufficient info → suggest alternatives.

RULES:
- Use ONLY weak context
- Honest about limits
- 6 answerable alternatives
- 100-150 words
- Friendly, not apologetic

JSON: {"answer":"str","emotion":"thinking|derp","suggestions":[{"text":"str"}×6]}

Emotions: thinking(redirecting), derp(limitation). Default: thinking"""
```

**Token count: ~85 tokens**

### User Message

```python
f"""Q: {question}

Context: {weak_context}

Can't fully answer. Acknowledge topic. Mention related info. Suggest 6 alternatives. Note: can discuss in interview. JSON only."""
```

**Token count: ~50 tokens (excluding context/question)**

### Redirect Emotion Guide

| Emotion | When to Use |
|---------|-------------|
| `thinking` | Redirecting to related technical topics |
| `derp` | Clear limitation, friendly acknowledgment |

**Default:** `thinking`

## Static Response Templates

### Off-Topic Response (Score < 0.20)

**No LLM call - static template:**

```json
{
  "answer": "That seems outside the scope of my portfolio knowledge base. I'm here to answer questions about James's professional experience, technical skills, and project work.\n\nWhat would you like to know about his development experience, projects, or technical approach?",
  "emotion": "thinking",
  "suggestions": [
    {"text": "What technologies do you use?"},
    {"text": "Tell me about your projects"},
    {"text": "What's your experience with AI/ML?"},
    {"text": "How do you approach problem-solving?"},
    {"text": "What's your leadership style?"},
    {"text": "Show me your best work"}
  ]
}
```

### Boundary Setting Response (Profanity Detected)

**No LLM call - static template:**

```json
{
  "answer": "I'm here to help you learn about James's professional background and experience. Please keep questions professional and on-topic.\n\nIf you're interested in James's work, I'd be happy to answer questions about his technical skills, projects, or development approach.",
  "emotion": "annoyed",
  "suggestions": [
    {"text": "What's your technical experience?"},
    {"text": "Tell me about your projects"},
    {"text": "What technologies do you use?"},
    {"text": "How do you approach development?"},
    {"text": "What are your strengths?"},
    {"text": "Show me your portfolio"}
  ]
}
```

## Project Links Handling

### Extraction Logic

Project links are extracted from the `project-links-all.md` note. When any project note appears in the top 3 retrieved results, include that project's links in the context.

**Example project links dictionary:**

```python
{
  "WhatNow": {
    "demo": "https://what-now-ai.onrender.com",
    "github": "https://github.com/yourusername/what-now"
  },
  "moh-ami": {
    "demo": "https://moh-ami.onrender.com",
    "github": "https://github.com/yourusername/moh-ami"
  }
}
```

### Usage in Prompts

Pass relevant project links as JSON in the user message:

```python
project_links_json = json.dumps({
    project: links 
    for project, links in all_project_links.items() 
    if any(project.lower() in note_id.lower() for note_id in top_3_note_ids)
})
```

### LLM Integration

The LLM should:
1. Include `projectLinks` object only when discussing a project in detail
2. Reference links naturally: "You can check out the live demo and GitHub repo"
3. Use project name as key (e.g., "WhatNow", "moh-ami")
4. Include both `demo` and `github` URLs when available

## OpenAI API Configuration

### JSON Mode

```python
response = self.client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    temperature=0.7,
    max_tokens=700,
    response_format={"type": "json_object"}
)
```

**Parameters:**
- `model`: `gpt-4o-mini` (supports JSON mode)
- `temperature`: `0.7` (balanced creativity/consistency)
- `max_tokens`: `700` (allows ~300-400 word answers + JSON structure)
- `response_format`: `{"type": "json_object"}` (ensures valid JSON)

### Response Parsing

```python
result = json.loads(response.choices[0].message.content)

# Validate and set defaults
if result.get("emotion") not in ["happy", "thinking", "surprised", "derp", "tired", "annoyed"]:
    result["emotion"] = "happy"

if not isinstance(result.get("suggestions"), list) or len(result["suggestions"]) < 6:
    # Handle missing suggestions
    result["suggestions"] = generate_default_suggestions()

return result
```

## Token Cost Analysis

### Per-Request Breakdown

**Full Answer (High Confidence):**
- System prompt: ~140 tokens
- User prompt: ~60 tokens
- Context (5 notes): ~1,000-1,500 tokens
- Question: ~10-30 tokens
- **Total input: ~1,210-1,730 tokens**
- Output (JSON): ~400-500 tokens
- **Total: ~1,610-2,230 tokens**
- **Cost per request: ~$0.00032-0.00045**

**Redirect (Low Confidence):**
- System prompt: ~85 tokens
- User prompt: ~50 tokens
- Weak context: ~500-800 tokens
- Question: ~10-30 tokens
- **Total input: ~645-965 tokens**
- Output (JSON): ~200-300 tokens
- **Total: ~845-1,265 tokens**
- **Cost per request: ~$0.00017-0.00025**

**Static Responses (Off-Topic/Boundary):**
- No LLM call
- **Cost: $0**

### Cost Comparison

| Approach | Prompt Tokens | Savings |
|----------|---------------|---------|
| Original verbose prompts | ~850 | - |
| First compression | ~350 | 59% |
| Ultra-compressed (current) | ~200 | 76% |

**Savings per 100 requests:**
- Before optimization: ~$0.017
- After optimization: ~$0.004
- **Savings: ~$0.013 (76% reduction)**

## Prompt Compression Techniques Used

1. **Compact JSON notation**: `×6` instead of `// 6 total`
2. **No whitespace**: Single-line JSON structure
3. **Inline explanations**: `emotion(happy|thinking...)` instead of bullet lists
4. **Abbreviations**: `Q:` instead of `Question:`
5. **Parenthetical defaults**: `default:happy` instead of full sentence
6. **Removed redundancy**: "Respond with valid JSON only" → "JSON only"
7. **Minimal formatting**: No pretty-printing or extra newlines
8. **Short labels**: "Folio:" instead of "You are Folio, an AI assistant..."
9. **Implied structure**: LLMs understand JSON well, don't need full examples

## Testing and Validation

### Prompt Testing Checklist

- [ ] LLM returns valid JSON 100% of time
- [ ] Emotion field always present and valid
- [ ] Suggestions array always has exactly 6 items
- [ ] Answer text stays within 300-400 words (full) or 100-150 (redirect)
- [ ] ProjectLinks included when projects discussed
- [ ] Tone is friendly but professional
- [ ] No hallucination - responses stay within context
- [ ] Defaults applied correctly (emotion → happy if invalid)

### Common Issues and Fixes

**Issue: Invalid emotion returned**
- Fix: Default to "happy" in post-processing
- Prevention: Clear emotion list in prompt

**Issue: Wrong number of suggestions**
- Fix: Generate default suggestions if <6
- Prevention: Explicitly state "6" in prompt

**Issue: Hallucination**
- Fix: Strengthen "ONLY context" instruction
- Prevention: Regular testing with questions outside context

**Issue: Too verbose**
- Fix: Adjust max_tokens
- Prevention: Specify word count in prompt

## Future Optimizations

### Potential Improvements

1. **Cached system prompts**: OpenAI prompt caching (when available)
2. **Dynamic max_tokens**: Adjust based on question complexity
3. **Multi-language support**: Compressed prompts in multiple languages
4. **A/B testing**: Compare ultra-compressed vs inline versions
5. **Emotion learning**: Track which emotions users respond to best

### Monitoring Metrics

Track in production:
- Average response length
- Emotion distribution
- Suggestion relevance (click-through)
- Project links inclusion rate
- Invalid JSON rate
- Default emotion fallback rate

## Summary

The ultra-compressed prompt design achieves:
- ✅ 76% token reduction (850 → 200 tokens)
- ✅ Reliable JSON output via JSON mode
- ✅ Clear emotion selection with defaults
- ✅ Project links integration
- ✅ 6 contextual suggestions per response
- ✅ Strict context-only responses
- ✅ Friendly but professional tone
- ✅ Cost savings: ~$0.013 per 100 requests

All critical instructions preserved while maximizing efficiency.

