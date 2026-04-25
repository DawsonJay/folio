# Tell me about contextual bandits

I've built WhatNow, an AI-powered activity recommendation system using contextual bandits — a form of reinforcement learning that balances exploration (trying new things) with exploitation (doubling down on what's worked). The algorithm takes context as input — in WhatNow's case, mood, energy, social preference, available time, and weather — and learns from which recommendations I actually choose.

The trickiest design decision was balancing responsiveness with stability. A system that learns only from recent choices becomes erratic — it chases whatever you picked yesterday and loses the broader pattern. I built a two-layer architecture to handle this: a session layer that adapts quickly within a single use, and a base layer that updates slowly from all historical data. The base layer provides stability; the session layer makes the system feel like it's paying attention right now.

The most interesting bug I encountered was invisible: the exploration parameter was set too low (epsilon 0.05 — 5% exploration, 95% exploitation). The algorithm was technically correct and metrics showed acceptable engagement, but recommendations felt samey over time. Users never discovered genuinely new experiences. Fixing it meant understanding what the system was actually optimising for versus what I wanted it to do — increasing epsilon to 0.15 and adding a diversity metric shifted that balance. WhatNow is production-deployed and I use it in my daily life, so the quality of its recommendations is something I experience directly.

---

**emotion:** happy
**suggestions:**
- Tell me about WhatNow
- Tell me about an ML project you built?
- Have you worked with recommendation systems?
- What's your understanding of embeddings?
- How do you approach AI project scoping?
- What AI/ML experience do you have?
