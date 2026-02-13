# What's your experience with RAG systems?

I've built Folio, the RAG-powered chatbot you're using right now. RAG stands for retrieval-augmented generation - combining knowledge bases with language models. Using LangChain for orchestration, OpenAI's text-embedding-3-small for semantic search, and GPT-4o-mini for response generation.

The atomic notes approach is key to Folio's design. Instead of long documents, the knowledge base contains self-contained notes each covering a single topic, written in first person. Granular structure enables precise retrieval - queries pull exactly relevant information without unrelated content dragging in.

Embeddings convert text into 1536-dimensional vectors where semantically similar content points in similar directions. Searching by meaning, not keywords. A query about leadership retrieves notes mentioning team dad approach even though leadership doesn't appear in them - the embedding understands they're semantically related.

The technical implementation uses local JSON storage with NumPy similarity calculations for vector search, appropriate for my dataset size. For larger production systems, I'd use dedicated vector databases like Pinecone or Weaviate. Understanding when simpler solutions suffice is part of good engineering.

The meta aspect - Folio is an AI system presenting an AI/ML portfolio. Practical RAG implementation with real-world trade-offs, not theoretical knowledge.

---

**emotion:** happy
**suggestions:**
- Tell me about your AI/ML experience
- What is Folio?
- How do you approach system design?
- What technologies are you most excited about?
- What challenges have you faced?
- What AI technologies are you learning?

