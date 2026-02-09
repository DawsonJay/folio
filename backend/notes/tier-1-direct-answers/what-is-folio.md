# What is Folio?

Folio is the RAG-powered portfolio chatbot you're talking to right now. It's an AI-powered portfolio chatbot that uses Retrieval Augmented Generation (RAG) to answer questions about my background, skills, and projects. The system represents the cutting edge of my AI/ML capabilities combined with full-stack development expertise, demonstrating modern AI application architecture in a production-ready system.

The core motivation for building Folio came from recognizing that traditional portfolios are passive documents. Employers read what you write in the order you wrote it. They can't ask follow-up questions. They can't drill into specific projects that interest them. They get the same generic information everyone sees. This mismatch between how employers want to evaluate candidates (through conversation and questions) and how portfolios present information (through static content) creates friction.

Folio solves this by making my portfolio conversational and interactive. Employers can ask natural language questions like "Tell me about your React experience" or "What was the biggest technical challenge in WhatNow?" The system retrieves relevant information from my knowledge base and generates personalized answers maintaining my authentic first-person voice. Follow-up questions drill deeper. Different employers get different information based on what they care about. The portfolio adapts to the conversation rather than forcing everyone through the same linear narrative.

The technical architecture combines several modern AI technologies. LangChain orchestrates the RAG workflow, handling retrieval, prompt construction, and response generation. OpenAI's text-embedding-3-small model (1536 dimensions) generates semantic embeddings from text, enabling similarity-based search. Local JSON file storage with NumPy similarity calculations handles vector search for my dataset size. OpenAI's GPT-4o-mini generates the actual chat responses using retrieved context. The frontend uses React with TypeScript for the chat interface. The backend uses FastAPI providing API endpoints for chat and suggestions.

The atomic notes approach is central to Folio's design. Instead of long articles or documents, the knowledge base consists of self-contained notes each covering a single coherent topic. Notes are written in first person as if I'm speaking directly to the interviewer. Each note includes enough context to stand alone so it makes sense when retrieved individually. This granular approach enables precise retrieval - the system can pull exactly the relevant notes for a query without dragging in unrelated information.

The meta aspect of using an AI chatbot to present an AI/ML portfolio is deliberate. Folio doesn't just claim I can build AI systems - it proves it by being an AI system. The transparency of the implementation with comprehensive documentation, test results, and technical decisions documented provides evidence of real engineering work. Employers interested in AI/ML capabilities can examine Folio's architecture and understand exactly how modern RAG systems work in practice.

What makes Folio particularly valuable is solving a real problem I personally experienced. Traditional portfolios don't support the conversational evaluation process employers want. Folio fixes this by making portfolio information conversationally accessible through natural language questions. This demonstrates I don't just build technology for technology's sake - I identify genuine problems and build appropriate solutions.

---

**emotion:** happy
**suggestions:**
- Tell me about your AI/ML experience
- What projects have you built?
- How do you approach system design?
- What technologies are you most excited about?
- Tell me about your RAG systems experience
- What challenges have you faced?

