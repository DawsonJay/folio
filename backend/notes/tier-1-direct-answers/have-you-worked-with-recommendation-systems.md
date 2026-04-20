# Have you worked with recommendation systems?

Yes, I've built WhatNow, an AI-powered activity recommendation system using contextual bandits, which is a form of reinforcement learning. The system uses semantic embeddings to match user context with activities and continuously improves over time based on user feedback.

WhatNow is a production-deployed application that I actually use in my daily life. The core concept is simple: I input my current context using sliders for mood, energy level, social preference, available time, and weather conditions. The AI then generates 50 personalized activity suggestions from a database of 1,249 activities with semantic embeddings. I pick my top 3 favorites, and if none are quite right, I can regenerate for more options while my favorites accumulate in a pool. Eventually I make a final selection from all the activities I've marked as favorites, and the AI learns from my choice to make better recommendations in future sessions.

The system uses a two-layer learning architecture with a Session AI for fast session learning and a Base AI for slow base learning. Session AI learns quickly from the current session, adapting recommendations in real-time as I make choices. Base AI learns slowly from all historical data, providing stability and preventing the system from overfitting to recent choices. Balances responsiveness and robustness - system that feels intelligent without being chaotic.

The semantic embeddings approach replaced manual metadata tagging. Instead of trying to manually categorize 1,249 activities with tags like outdoor, social, active, I used AI embeddings to capture the semantic meaning of each activity. The system understands that "hiking" and "walking in nature" are similar, even if they're described differently.

The contextual bandits algorithm balances exploration (trying new things) vs. exploitation (doubling down on what works). I had to debug an invisible bias where the exploration parameter was too low, which meant the system was showing safe recommendations but not discovering genuinely new experiences. I fixed this by adjusting the exploration rate and implementing adaptive exploration.

WhatNow is one of my most successful portfolio projects. Complete end-to-end machine learning engineering. The project is fully deployed, genuinely useful, and continues to improve through real usage.

---

**emotion:** happy
**suggestions:**
- Tell me about WhatNow
- Tell me about contextual bandits
- What's your understanding of embeddings?
- How do you approach AI project scoping?
- How do you approach adding LLM features?
- What is Folio?
