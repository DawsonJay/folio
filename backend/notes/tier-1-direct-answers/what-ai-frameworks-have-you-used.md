# What AI frameworks have you used?

I use LangChain for building LLM applications, OpenAI API for embeddings and language models, and I've implemented contextual bandits for recommendation systems. For Folio, I use LangChain with OpenAI embeddings for semantic search and RAG architecture. For moh-ami, I integrated OpenAI API for translation explanations and language learning assistance.

WhatNow uses a custom contextual bandits implementation for activity recommendations. The system learns from user choices to improve future suggestions, balancing immediate responsiveness with long-term learning. I built a two-layer learning architecture combining fast adaptation with stable long-term preferences.

I work with embeddings extensively - generating them, storing them, and retrieving them for semantic search. The Folio portfolio chatbot uses 137 atomic notes as embeddings retrieved based on query similarity. This RAG approach combines retrieval with generation for accurate, grounded responses.

For development, I use FastAPI for Python backends integrating AI capabilities, React for frontends consuming AI services, and Prisma ORM for database management including vector storage. I've worked with Vercel AI SDK for streaming responses and building AI-powered interfaces.

My approach is to use existing AI services rather than build infrastructure from scratch. OpenAI for embeddings and language models, LangChain for orchestration, FastAPI for the backend layer — the goal is shipping something that works and provides real value, not reinventing what already exists.

---

**emotion:** thinking
**suggestions:**
- What AI/ML experience do you have?
- Tell me about WhatNow
- What is Folio?
- How do you approach adding LLM features?
- Tell me about moh-ami
- What's your understanding of embeddings?
