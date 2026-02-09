# Prompt Engineering Experience

## moh-ami: LLM-Powered Legal Assistance

My primary prompt engineering experience comes from the moh-ami project, where I integrated OpenAI's GPT-4o-mini to provide legal document assistance and guidance.

## Core Implementation

**OpenAI API Integration**: Used OpenAI Node.js SDK v6.16.0 for API integration with GPT-4o-mini model.

**Structured JSON Prompts**: Designed prompts that returned structured data rather than free-form text, enabling:
- Consistent parsing and display
- Validation of responses
- Integration with TypeScript type system
- Error handling for malformed outputs

## Prompt Design Strategies

### System Context and Role Definition

Defined clear system messages that established:
- The AI's role (legal assistant, not legal advice)
- Tone and approach (helpful, clear, non-intimidating)
- Output format requirements (JSON structure)
- Safety boundaries (what not to do)

### Context Management

**Compact context building**: Provided relevant legal document context to the LLM without overwhelming token limits:
- Extracted relevant sections from documents
- Summarized user's situation concisely
- Included only pertinent case details

### Output Structure

**Enforced structured responses**: Rather than asking for general explanations, prompts specified exact JSON formats:
```
{
  "explanation": "...",
  "next_steps": [...],
  "resources": [...],
  "confidence": "high/medium/low"
}
```

This made responses predictable and integrable with the UI.

## Error Handling and Validation

**Graceful degradation**: When LLM responses didn't match expected format:
- Attempted to parse and salvage useful parts
- Provided fallback responses
- Logged issues for prompt refinement

**Prompt iteration**: Refined prompts based on failure cases to reduce malformed responses.

## Key Learnings

### 1. Specificity Over Generality

Vague prompts like "explain this document" produced verbose, unfocused responses. Specific prompts like "identify the 3 most important deadlines in this document and explain consequences of missing each" produced useful, actionable information.

### 2. Format Enforcement

Requesting "JSON format" wasn't enough. Providing exact schema examples in the prompt dramatically improved output consistency.

### 3. Temperature Tuning

**Lower temperature (0.3-0.5)** for factual, structured responses (document analysis, step identification).

**Higher temperature (0.7-0.8)** for creative explanations or analogies (making legal concepts accessible).

### 4. Token Economics

**Balance detail vs. cost**: More context isn't always better. I learned to identify minimal sufficient context that produced good responses without unnecessary token usage.

**Streaming for UX**: Used streaming responses where appropriate so users saw incremental results rather than waiting for complete responses.

## Integration Challenges

**Type Safety**: Ensured LLM responses matched TypeScript types by:
- Runtime validation of responses
- Type guards for parsed JSON
- Fallback types for malformed responses

**GraphQL Integration**: Passed LLM results through GraphQL resolvers, requiring careful error handling and type alignment.

**User Experience**: Made LLM interactions feel natural:
- Loading states during API calls
- Progressive disclosure of complex information
- Clear indication when AI is uncertain

## Ethical Considerations

**Not Legal Advice**: Carefully crafted prompts to assist understanding without crossing into legal advice:
- Always recommend consulting actual lawyers
- Focus on explaining process and documents
- Avoid making specific recommendations about user's case

**Hallucination Risk**: Implemented confidence indicators and always cited sources where possible to help users evaluate AI output critically.

## Technical Outcomes

**Successful production deployment**: The LLM integration worked reliably in production, helping users understand legal documents they found intimidating.

**Performance**: Response times typically under 3 seconds, acceptably fast for the use case.

**Cost management**: Token usage optimization kept API costs sustainable for the project scope.

## Relevance to RAG Systems

The moh-ami prompt engineering experience directly informed building the Folio RAG system:
- Understanding how to structure context for LLMs
- Knowing when to use higher vs. lower temperature
- Experience with JSON-structured outputs
- Token management strategies
- Error handling for LLM responses

Prompt engineering isn't just about writing prompts - it's about designing systems that integrate LLMs reliably and usefully. The moh-ami project taught me how to do this in production contexts.

