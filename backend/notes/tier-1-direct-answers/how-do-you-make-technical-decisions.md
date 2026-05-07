# How do you make technical decisions?

The question I anchor every decision to is: what does this system actually need to do, and what will make it hardest to change later? Everything else follows from that.

On the Nexus Dashboard, I knew the backend was complex and unstable — it was likely to change significantly before we shipped. So the architectural priority was adaptability over polish. I chose a foundation blocks approach: a library of composable, tested components that could be rearranged as requirements shifted without requiring frontend rewrites. That decision shaped every tool and structural choice that followed. I also brought in React Query early for caching because 15+ seconds load time was making the system unusable — that was a user impact decision, not a code preference.

On personal projects I make technology decisions based on fit rather than familiarity. WhatNow needed contextual bandits, so I used Python and FastAPI. moh-ami needed flexible data fetching across a complex translation schema, so GraphQL with Apollo made sense. Folio needed inspectable RAG routing and tight cost control, so I kept orchestration inside FastAPI with OpenAI embeddings, local cosine search, and explicit Tier 1 / Tier 2 logic. The point is that the problem defines the tool — I don't apply the same stack to every project and adjust later.

---

**emotion:** thinking
**suggestions:**
- Tell me about the Integrations Dashboard
- Tell me about moh-ami
- Tell me about WhatNow
- Tell me about the Nexus Dashboard
- What is Folio?
- When do you refactor versus rewrite?
