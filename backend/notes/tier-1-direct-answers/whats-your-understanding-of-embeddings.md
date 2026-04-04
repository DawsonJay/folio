# What's your understanding of embeddings?

I understand embeddings through building WhatNow, an AI-powered activity recommendation system, and Folio, the RAG-powered portfolio chatbot you're talking to right now. Embeddings are vector representations of text that capture semantic meaning, enabling similarity-based search and semantic understanding.

In WhatNow, I used semantic embeddings to match user context with activities. Instead of trying to manually categorize 1,249 activities with tags like outdoor, social, active, I used AI embeddings to capture the semantic meaning of each activity. The system understands that "hiking" and "walking in nature" are similar, even if they're described differently. The embeddings capture relationships I couldn't have anticipated or manually encoded.

The embeddings convert text into high-dimensional numerical vectors (1536 dimensions in Folio's case) where semantically similar text has vectors that point in similar directions in this high-dimensional space. Searching by meaning rather than keyword matching. A query about "leadership" retrieves notes mentioning "team dad" approach even though "leadership" doesn't appear in those notes - the embedding understands they're semantically related concepts.

In WhatNow, the most significant technical pivot happened when I realized the manual metadata approach wasn't scalable. I had started with 17 activities that required 15+ manual metadata fields each. This created 30MB+ of manual data that was tedious to maintain and didn't scale to hundreds of activities. I completely pivoted to an AI-powered system using embeddings, eliminating all manual metadata. The database transformed from 17 activities with complex metadata to 1,250 activities with just name and AI embedding.

The decision to use sentence transformers (all-MiniLM-L6-v2 in WhatNow, text-embedding-3-small in Folio) over LLMs was driven by performance, cost, and reliability considerations - embeddings are faster, cheaper, and more reliable for semantic matching than generating text with LLMs.

I understand how to generate embeddings, store them, and use them for semantic search. I've worked with embeddings in production systems, understanding the challenges of embedding quality, similarity thresholds, and how to structure knowledge bases for effective retrieval.

---

**emotion:** happy
**suggestions:**
- Tell me about your AI/ML experience
- Tell me about WhatNow project
- What's your experience with RAG systems?
- What technologies are you most excited about?
- How do you stay current with technology?
- What is Folio and how does it work?

