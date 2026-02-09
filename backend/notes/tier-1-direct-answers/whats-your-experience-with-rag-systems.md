# What's your experience with RAG systems?

I have experience with RAG systems through Folio, the RAG-powered portfolio chatbot you're talking to right now. RAG stands for retrieval-augmented generation, which combines knowledge bases with language models. The system uses LangChain for RAG orchestration, handling retrieval, prompt construction, and response generation.

The technical architecture combines several modern AI technologies. LangChain orchestrates the RAG workflow, handling retrieval, prompt construction, and response generation. OpenAI's text-embedding-3-small model (1536 dimensions) generates semantic embeddings from text, enabling similarity-based search. Local JSON file storage with NumPy similarity calculations handles vector search for my dataset size. OpenAI's GPT-4o-mini generates the actual chat responses using retrieved context.

The atomic notes approach is central to Folio's design. Instead of long articles or documents, the knowledge base consists of self-contained notes each covering a single coherent topic. Notes are written in first person as if I'm speaking directly to the interviewer. Each note includes enough context to stand alone so it makes sense when retrieved individually. This granular approach enables precise retrieval - the system can pull exactly the relevant notes for a query without dragging in unrelated information.

The embeddings themselves are fascinating pieces of technology. They convert text into 1536-dimensional numerical vectors where semantically similar text has vectors that point in similar directions in this high-dimensional space. This enables searching by meaning rather than keyword matching. A query about "leadership" retrieves notes mentioning "team dad" approach even though "leadership" doesn't appear in those notes - the embedding understands they're semantically related concepts.

The first-person voice in answers is carefully maintained through the atomic notes and LLM prompt design. Notes are written as if I'm speaking directly, using "I" and describing experiences personally. The LLM system prompt instructs it to answer in first person as if it is me. This creates answers that feel authentic and personal rather than clinical third-person descriptions.

The meta aspect of using an RAG system to present an AI/ML portfolio is deliberate. Folio doesn't just claim I can build AI systems - it proves it by being an AI system. The transparency of the implementation with comprehensive documentation, test results, and technical decisions documented provides evidence of real engineering work.

---

**emotion:** happy
**suggestions:**
- Tell me about your AI/ML experience
- What is Folio?
- How do you approach system design?
- What technologies are you most excited about?
- What challenges have you faced?
- What AI technologies are you learning?

