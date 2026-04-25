# Do you have experience with LLMs?

Yes — production experience integrating LLMs into web applications. moh-ami uses GPT-4o-mini to provide detailed educational explanations for French language learners. Folio is the RAG-powered chatbot you're using right now. In both cases the focus is on prompt engineering that produces reliable, cost-effective results rather than impressive demos that don't hold up in practice.

In moh-ami, I designed structured prompts requesting specific JSON schemas, making responses consistent and parseable. The system handles word-by-word translations, grammar explanations, and cultural context. I built validation logic catching common LLM errors before they reach users. LLMs are powerful but unpredictable - production systems need careful error handling.

Cost is minimal. moh-ami costs about £1-2 monthly for OpenAI API usage. I self-host all my projects on a Raspberry Pi I set up as a home server, so hosting costs are effectively zero. I build efficient systems - batching requests, caching responses, choosing appropriate models for each task.

In Folio, I'm using LLMs as part of a RAG system - retrieval-augmented generation combining knowledge bases with language models. The system uses embeddings for semantic search to find relevant information, then LLMs generate responses based on that context. More accurate answers than using LLMs alone.

My LLM experience is primarily about integration — building the full user experience around the model: handling streaming responses, designing loading states, managing errors gracefully, and creating interfaces that work reliably when the AI is inherently non-deterministic.

---

**emotion:** happy
**suggestions:**
- Tell me about moh-ami
- Tell me about prompt engineering experience
- What is Folio?
- How do you approach adding LLM features?
- What AI/ML experience do you have?
- What's your experience with RAG systems?
