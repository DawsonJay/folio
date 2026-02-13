# What technologies did you use for WhatNow?

Frontend: React with TypeScript, Redux Toolkit for state management, and mobile-first responsive design. Backend: Python with FastAPI, PostgreSQL database, and Render for deployment. AI/ML: sentence transformers (`all-MiniLM-L6-v2`) for semantic embeddings, custom contextual bandit implementation, two-layer learning architecture (Session AI + Base AI).

The technology choices were pragmatic. React + TypeScript provides type safety and scalability. Redux manages complex application state across recommendations, favorites, and learning feedback. FastAPI gives Python's ML ecosystem with fast API performance. PostgreSQL handles persistent storage for activities, embeddings, and training data.

For ML, I chose sentence transformers over LLMs for semantic matching because they're faster (milliseconds vs seconds), cheaper (no API costs), and more reliable (consistent embeddings vs variable text generation). The two-layer learning architecture balances responsiveness (Session AI learns quickly from current session) with stability (Base AI learns slowly from all historical data).

The architecture evolved through iterations. Started with vanilla JavaScript and basic linear contextual bandits, then migrated to React + TypeScript for better structure. Added Redux as state complexity grew. Pivoted from scikit-learn to custom lightweight implementations to reduce dependencies. The evolution shows pragmatic decision-making under real constraints.

WhatNow demonstrates full-stack AI/ML engineering - complete system from database to deployment, not just model training.

---

**emotion:** happy
**suggestions:**
- Tell me about the WhatNow project
- How did you learn React?
- What's your experience with FastAPI?
- How do you choose technologies for projects?
- What AI frameworks have you used?
- Tell me about your machine learning experience

**projectLinks:**
- WhatNow:
  - demo: https://whatnow.onrender.com/
  - github: https://github.com/yourusername/whatnow
