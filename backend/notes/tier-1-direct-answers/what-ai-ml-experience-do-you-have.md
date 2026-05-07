# What AI/ML experience do you have?

I've built three production AI systems: WhatNow (recommendation engine using contextual bandits and reinforcement learning), moh-ami (LLM-powered language learning tool with structured prompt engineering), and Folio (the RAG chatbot you're using right now). The focus across all three is practical AI integration into web applications — not research or prototype work, but production systems with real users and real constraints.

WhatNow is end-to-end machine learning engineering. Two-layer learning architecture where Session AI learns quickly from current interactions while Base AI provides stability from historical data. The system uses semantic embeddings to match user context with 1,249 activities and continuously improves through real usage. Deployed in production and generates its own training data through user interactions - solving the dataset acquisition problem that killed my earlier computer vision projects.

moh-ami is LLM integration. Designed structured prompts requesting specific JSON schemas. Built validation logic catching common LLM errors before they reach users. The system handles word-by-word translations, grammar explanations, and cultural context through careful prompt engineering. Costs minimal - about £1-2 monthly for OpenAI API.

Folio is RAG architecture I shipped in FastAPI: Tier 1 embeddings over curated Q&A, Tier 2 embeddings over atomic markdown notes, confidence-style routing, OpenAI `text-embedding-3-small` plus `gpt-4o-mini`, everything stored in a local embedding file rather than a hosted vector DB — appropriate for this corpus size.

My AI experience focuses on integration. I'm creating AI-powered user interfaces, handling streaming responses, designing loading states, and building complete systems. AI as a capability to integrate into frontend applications.

---

**emotion:** happy
**suggestions:**
- Tell me about WhatNow
- Tell me about moh-ami
- What is Folio?
- Tell me about contextual bandits
- How do you approach adding LLM features?
- What's your experience with RAG systems?

**variants:**
- Have you built interfaces that display AI or ML output before?
