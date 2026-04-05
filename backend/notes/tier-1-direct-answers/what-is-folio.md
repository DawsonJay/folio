# What is Folio?

Folio is the RAG-powered portfolio chatbot you're talking to right now. It uses Retrieval Augmented Generation to answer questions about my background, skills, and projects. Modern AI application architecture in a production system.

Traditional portfolios are passive. Employers read what you write in the order you wrote it. No follow-up questions, no drilling into specific interests, same generic information for everyone. This mismatch between how employers evaluate candidates through conversation versus how portfolios present static content creates friction.

Folio solves this by making my portfolio conversational. Ask natural language questions like Tell me about your React experience or What was the biggest challenge in WhatNow? The system retrieves relevant information and generates personalized answers maintaining my authentic first-person voice. Different employers get different information based on what they care about. The portfolio adapts to conversation rather than forcing everyone through the same linear narrative.

The technical architecture combines several modern AI technologies. LangChain orchestrates the RAG workflow. OpenAI's text-embedding-3-small generates 1536-dimension semantic embeddings enabling similarity search. Local JSON storage with NumPy similarity calculations handles vector search for my dataset size. GPT-4o-mini generates chat responses using retrieved context. Frontend uses React/TypeScript, backend uses FastAPI.

The atomic notes approach is central. Instead of long documents, the knowledge base contains self-contained notes each covering a single topic, written in first person as if I'm speaking directly. This granular approach enables precise retrieval - the system pulls exactly relevant information without unrelated content.

The meta aspect is deliberate. Folio is an AI system presenting an AI/ML portfolio.

---

**emotion:** happy
**suggestions:**
- What AI/ML experience do you have?
- What projects have you built?
- What technologies are you most excited about?
- What's your experience with RAG systems?
- Tell me about WhatNow
- What's your understanding of embeddings?

