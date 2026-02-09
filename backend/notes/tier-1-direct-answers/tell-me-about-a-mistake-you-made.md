# Tell me about a mistake you made

The hardest bug I've fixed wasn't a crash or error message - it was invisible bias in WhatNow's recommendation algorithm that I had to discover, prove, and fix without any obvious symptoms. This was a mistake in my design choices, not my implementation.

WhatNow used a two-layer learning architecture: embeddings for semantic similarity plus contextual bandits for personalization. The system was working, recommendations seemed reasonable, but something felt off. User feedback suggested recommendations felt samey - not obviously wrong, just not as diverse as they should be. Metrics didn't show a problem, but the qualitative feedback nagged at me.

I spent a week debugging before I realized: the contextual bandit's exploration parameter was too low. Contextual bandits balance exploration (trying new things) vs. exploitation (doubling down on what works). My epsilon value (exploration rate) was 0.05, which meant 5% exploration. This meant 95% of the time, the algorithm showed safe recommendations. Safe recommendations performed acceptably, so metrics didn't flag it. But users weren't discovering genuinely new experiences.

Why this was hard: There was no error message. The system worked exactly as coded. No crashes, no exceptions, no warnings. The bug was in my design choices, not my implementation. Metrics didn't show it - click-through rates and engagement were acceptable. Traditional A/B testing wouldn't catch this because both versions would perform fine. Users couldn't articulate what was wrong. They just felt recommendations were okay but not exciting. That's hard to debug.

To fix this, I needed to understand how contextual bandits actually learn, the exploration-exploitation trade-off, why low exploration creates invisible problems, and how to measure diversity, not just performance. I changed epsilon from 0.05 to 0.15, implemented adaptive exploration, added diversity penalty to exploitation choices, created monitoring dashboard to track diversity metrics, and added mechanism for users to explicitly request something different.

The results: Category diversity increased by 40%, average semantic distance between recommendations increased by 25%, long-term engagement improved, and users reported feeling like they were discovering things.

What I learned: Trust your intuition, then prove it. Metrics can lie by omission - everything I was measuring said fine, but I wasn't measuring the right things. Sometimes the bug is the design - the code worked perfectly, the algorithm was implemented correctly, the bug was in my design choices. User feedback matters - even vague feedback can point to real problems. Deep understanding beats trial and error.

This was harder than any stack overflow or memory leak I've debugged because it required seeing what wasn't there: the recommendations users never got to experience.

---

**emotion:** thinking
**suggestions:**
- What did you learn from that mistake?
- How do you handle failure?
- Tell me about WhatNow project
- How do you approach debugging?
- What challenges have you faced?
- How do you ensure code quality?

