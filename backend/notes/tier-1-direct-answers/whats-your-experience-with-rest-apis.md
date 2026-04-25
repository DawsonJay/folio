# What's your experience with REST APIs?

REST APIs run through all of my production work. On the backend I've built them in two stacks: C# at Nurtur for professional work, and Python with FastAPI for personal AI projects.

The Integrations Dashboard API was my first professional backend work. Under senior mentorship I designed and built the endpoints that the sales team's dashboard runs on — they're still serving requests three years later with no maintenance. The key decision there was designing the API around what the frontend actually needed to display, not what seemed like a complete data model. That thinking — build the API for the consumer, not in the abstract — is something I carry into every project.

FastAPI I've used as the backbone for WhatNow, moh-ami, and Folio. Each has different constraints: WhatNow's endpoints handle recommendation requests and write back learning data; moh-ami passes structured prompts to OpenAI and returns JSON translations; Folio's RAG pipeline retrieves embeddings, runs semantic search, and constructs responses before sending anything to the LLM. Building APIs that wrap AI systems has its own set of considerations — the response is non-deterministic, latency is higher, and error handling needs to account for the external service failing or returning something unexpected.

---

**emotion:** happy
**suggestions:**
- What's your backend development experience?
- Tell me about the Integrations Dashboard
- Tell me about moh-ami
- Tell me about WhatNow
- What is Folio?
- What databases have you worked with?
