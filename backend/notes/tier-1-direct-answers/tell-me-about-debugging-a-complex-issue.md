# Tell me about debugging a complex issue

The hardest bug I've fixed wasn't a crash or error message - it was invisible bias in WhatNow's recommendation algorithm that I had to discover, prove, and fix without any obvious symptoms.

WhatNow used a two-layer learning architecture: embeddings for semantic similarity plus contextual bandits for personalization. The system was working, recommendations seemed reasonable, but something felt off. User feedback suggested recommendations felt samey - not obviously wrong, just not as diverse as they should be. Metrics didn't show a problem, but the qualitative feedback nagged at me.

I spent a week debugging before I realized: the contextual bandit's exploration parameter was too low. Contextual bandits balance exploration (trying new things) vs. exploitation (doubling down on what works). My epsilon value was 0.05, which meant 5% exploration. The algorithm showed safe recommendations 95% of the time. Safe recommendations performed acceptably, so metrics didn't flag it. But users weren't discovering genuinely new experiences.

Why this was hard: No error message. The system worked exactly as coded. The bug was in my design choices, not my implementation. Metrics didn't show it - click-through rates and engagement were acceptable. Users couldn't articulate what was wrong. They just felt recommendations were okay but not exciting.

I changed epsilon from 0.05 to 0.15, implemented adaptive exploration, and added diversity metrics to track. Category diversity increased by 40%, average semantic distance between recommendations increased by 25%, and users reported feeling like they were discovering things.

What I learned: Trust your intuition, then prove it. Metrics can lie by omission - everything I was measuring said fine, but I wasn't measuring the right things. Sometimes the bug is the design. User feedback matters - even vague feedback can point to real problems. Deep understanding beats trial and error.

This was harder than any stack overflow or memory leak I've debugged because it required seeing what wasn't there: the recommendations users never got to experience.

---

**emotion:** thinking
**suggestions:**
- Tell me about a mistake you made
- How do you approach problem-solving?
- How do you ensure code quality?
- Tell me about WhatNow
- How do you handle failure?
- What's your debugging process?

