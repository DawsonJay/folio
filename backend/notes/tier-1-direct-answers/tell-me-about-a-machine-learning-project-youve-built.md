# Tell me about a machine learning project you've built

WhatNow is an AI-powered activity recommendation system that I built using contextual bandits, which is a form of reinforcement learning. It's a production-deployed application that I actually use in my daily life - it's not just a portfolio piece, it's a tool that provides real value.

I input my current context using sliders for mood, energy level, social preference, available time, and weather conditions. The AI then generates 50 personalized activity suggestions from a database of 1,249 activities with semantic embeddings. I pick my top 3 favorites, and if none are quite right, I can regenerate for more options while my favorites accumulate in a pool. Eventually I make a final selection from all the activities I've marked as favorites, and the AI learns from my choice to make better recommendations in future sessions.

WhatNow is a complete end-to-end machine learning system in production, not just a model or proof of concept. It handles data acquisition through user interaction, implements continuous learning that improves over time, and provides genuine utility.

The motivation for building WhatNow came from a practical problem. I had tried building computer vision projects - a fruit recognition system called Jam Hot and a weather prediction system called Cirrus - and both failed because of fundamental dataset quality issues. For personal portfolio projects, acquiring high-quality datasets is often the insurmountable barrier to completion.

WhatNow solves that problem by generating its own training data. Every time I use it, I'm providing labeled examples of what activities I prefer given specific contexts. The AI doesn't need a massive pre-existing dataset - it learns from my actual usage over time.

The technical implementation evolved significantly. I started with vanilla JavaScript and basic linear contextual bandits. As the project grew, I migrated to React and TypeScript for better structure. The recommendation algorithm evolved from simple linear models to semantic embeddings that capture the meaning of activities, and eventually to a two-layer learning architecture with Session AI and Base AI.

The two-layer learning architecture was a key innovation. Session AI learns quickly from the current session, adapting recommendations in real-time. Base AI learns slowly from all historical data, providing stability and preventing the system from overfitting to recent choices.

The semantic embeddings approach replaced manual metadata tagging. Instead of trying to manually categorize 1,249 activities with tags like outdoor, social, active, I used AI embeddings to capture the semantic meaning of each activity. The system understands that hiking and walking in nature are similar, even if they're described differently.

---

**shortTitle:** Tell me about an ML project you built?
**emotion:** happy
**suggestions:**
- Tell me about WhatNow
- How do you approach AI project scoping?
- Tell me about Cirrus
- What is Folio?
- Tell me about contextual bandits
- What AI/ML experience do you have?

