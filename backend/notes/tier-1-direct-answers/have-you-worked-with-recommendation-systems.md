# Have you worked with recommendation systems?

Yes — WhatNow is a production-deployed activity recommendation system built on contextual bandits, a form of reinforcement learning. I built it from scratch and use it in my daily life, which is the most honest form of quality control.

The core mechanic: I enter my context through sliders — mood, energy, social preference, available time, weather — and the system surfaces 50 personalized suggestions from a database of 1,249 activities matched using semantic embeddings. I mark favourites, the AI learns from my eventual choice, and recommendations improve over time.

One design challenge was balancing responsiveness with stability. A recommendation system that learns only from recent choices becomes erratic — it'll chase whatever you picked yesterday and miss the broader pattern. I built a two-layer architecture to handle this: a session layer that adapts quickly within a single use, and a base layer that updates slowly from all historical data. The base layer provides stability; the session layer provides the feeling that the system is paying attention right now.

I also had to debug an invisible bias: the exploration parameter was too low, which meant the system kept recommending safe choices and never surfaced genuinely new experiences. The algorithm was technically working but behaviourally wrong. Fixing it required understanding what the system was actually optimising for versus what I wanted it to do — a distinction that matters a lot with reinforcement learning.

---

**emotion:** happy
**suggestions:**
- Tell me about WhatNow
- Tell me about contextual bandits
- What's your understanding of embeddings?
- How do you approach AI project scoping?
- How do you approach adding LLM features?
- What is Folio?
