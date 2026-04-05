# Tell me about contextual bandits

I've built WhatNow, an AI-powered activity recommendation system using contextual bandits, which is a form of reinforcement learning. Contextual bandits balance exploration (trying new things) vs. exploitation (doubling down on what works), making them ideal for recommendation systems that need to learn from user feedback.

The system uses a two-layer learning architecture with a Session AI for fast session learning and a Base AI for slow base learning. Session AI learns quickly from the current session, adapting recommendations in real-time as I make choices. Base AI learns slowly from all historical data, providing stability and preventing the system from overfitting to recent choices. Balances responsiveness and robustness - system that feels intelligent without being chaotic.

Contextual bandits work by using context (in WhatNow's case, mood, energy level, social preference, available time, weather conditions) to make recommendations, then learning from the user's choice. The algorithm balances showing recommendations it thinks will work (exploitation) with trying new things to learn more (exploration).

I had to debug an invisible bias where the exploration parameter (epsilon) was too low. The epsilon value was 0.05, which meant only 5% exploration. This meant 95% of the time, the algorithm showed safe recommendations. Safe recommendations performed acceptably, so metrics didn't flag it. But users weren't discovering genuinely new experiences. I fixed this by changing epsilon from 0.05 to 0.15, implementing adaptive exploration, and adding diversity penalty to exploitation choices.

The hardest part was discovering this bug - there was no error message, the system worked exactly as coded, and metrics didn't show the problem. It required deep understanding of how contextual bandits actually learn, the exploration-exploitation trade-off, and how to measure diversity, not just performance.

WhatNow is a production-deployed application that I actually use in my daily life. The contextual bandits system is continuously learning from real usage. The system has learned my preferences through months of real usage. Algorithm works in practice, not just theory.

---

**emotion:** happy
**suggestions:**
- Tell me about WhatNow
- Tell me about an ML project you built?
- Have you worked with recommendation systems?
- What's your understanding of embeddings?
- How do you approach AI project scoping?
- What AI/ML experience do you have?

