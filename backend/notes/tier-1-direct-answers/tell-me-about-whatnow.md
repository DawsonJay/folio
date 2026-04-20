# Tell me about WhatNow

WhatNow is an AI-powered activity recommendation system using contextual bandits and reinforcement learning. It's production-deployed and I use it daily - it's not just a portfolio piece, it solves a real problem deciding what to do when I'm feeling stuck or unmotivated.

The system takes my current context through sliders for mood, energy, social preference, time available, and weather. It generates 50 personalized suggestions from 1,249 activities with semantic embeddings. I pick favorites, and the AI learns from my choices to improve future recommendations. It's complete end-to-end ML - data acquisition through user interaction, continuous learning, and genuine utility.

The motivation was practical. My earlier computer vision projects failed due to dataset quality issues. WhatNow solves this by generating its own training data - every time I use it, I'm providing labeled examples. The AI doesn't need pre-existing datasets, it learns from actual usage.

The technical implementation uses a two-layer architecture. Session AI learns quickly from current interactions. Base AI provides stability from historical data. This balances immediate responsiveness with long-term robustness. The system uses semantic embeddings so similar activities cluster together naturally without manual tagging.

The biggest pivot was abandoning manual metadata. I started with 17 activities requiring 15+ manual fields each, creating 30MB+ of tedious data that didn't scale. Pivoting to AI embeddings transformed it to 1,249 activities with just name and embedding. I recognized the approach wouldn't scale and adapted.

---

**emotion:** happy
**suggestions:**
- Tell me about contextual bandits
- What AI/ML experience do you have?
- Tell me about Atlantis
- What technologies did you use for WhatNow?
- How do you approach AI project scoping?
- What is Folio?
