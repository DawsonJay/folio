# What AI frameworks have you used?

I use the **OpenAI API** heavily (embeddings + chat with JSON outputs), **FastAPI** for Python service boundaries, and **custom Python/JS** where frameworks add noise — WhatNow's contextual bandits are hand-rolled because I needed the same ideas on both backend and frontend.

**Folio (this chatbot)** is intentionally not “framework-first” RAG: routing, Tier 1 vs Tier 2 retrieval, similarity search over a local embedding store, and structured responses are plain FastAPI + NumPy-style cosine similarity plus the OpenAI client. That's easier to tune and explain in interviews than a black-box chain wrapper.

For **moh-ami**, orchestration stays in Next.js/App Router routes and structured prompts validated in code rather than delegating semantics to an external orchestration toolkit.

I've used ecosystem patterns people associate with LangChain-style pipelines, but Folio shipped as readable application code rather than stacking another dependency layer.

---

**emotion:** thinking
**suggestions:**
- What AI/ML experience do you have?
- Tell me about WhatNow
- What is Folio?
- How do you approach adding LLM features?
- Tell me about moh-ami
- What's your understanding of embeddings?
