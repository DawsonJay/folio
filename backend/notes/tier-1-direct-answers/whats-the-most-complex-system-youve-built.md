# What's the most complex system you've built?

The Nexus Dashboard at Nurtur. It visualised a complex backend system — queues, virtual machines, job managers, multi-tenant structures — and when I joined it, the load time was 15+ seconds. Users were staring at a blank screen not knowing if the app had frozen.

The problem wasn't a bug — it was an architecture that didn't match usage patterns. The system was fetching full objects when it only needed counts, loading everything upfront when most data was never seen in a session, and making repeated API calls for data it had already fetched. I had to rethink how data moved through the system, not patch what was there.

The approach: show counts first (fast, lightweight), fetch full objects only when a user expands a section. React Query for caching to prevent redundant requests. Buffer systems to page large datasets into manageable chunks. Loading progress so users had feedback during the initial load rather than a blank screen. Load time dropped from 15+ seconds to under five.

The more lasting architectural decision was the foundation blocks system — a library of modular, composable components designed so the dashboard could absorb backend changes without requiring frontend rewrites. The backend structure was genuinely unstable during development; we both knew it would change. Building with that assumption meant designing for adaptability rather than treating the first schema as permanent. That decision meant features could be added and rearranged without structural rework.

The full-stack thinking required — understanding what the backend could efficiently serve, what the frontend could cache, and what the user actually needed to see first — is what made it complex. Each layer had constraints that shaped the others.

---

**emotion:** happy
**suggestions:**
- Why do you want to work at a startup?
- Tell me about the Nexus Dashboard
- Tell me about the Integrations Dashboard
- Tell me about WhatNow
- How do you ensure code quality?
- What project are you most proud of?
