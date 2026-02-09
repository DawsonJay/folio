# Tell me about WhatNow

WhatNow is an AI-powered activity recommendation system that helps me decide what to do when I'm feeling stuck or unmotivated. It's a production-deployed application that I actually use in my daily life, which makes it particularly satisfying - it's not just a portfolio piece, it's a tool that provides real value.

The core concept is simple: I input my current context using sliders for mood, energy level, social preference, available time, and weather conditions. The AI then generates 50 personalized activity suggestions from a database of 1,249 activities with semantic embeddings. I pick my top 3 favorites, and if none are quite right, I can regenerate for more options while my favorites accumulate in a pool. Eventually I make a final selection from all the activities I've marked as favorites, and the AI learns from my choice to make better recommendations in future sessions.

What makes WhatNow special is that it's a complete end-to-end machine learning system in production, not just a model or proof of concept. It handles data acquisition through user interaction, implements continuous learning that improves over time, balances immediate responsiveness with long-term robustness, and provides genuine utility that keeps me engaged with it.

The motivation for building WhatNow came from a very practical problem. I had tried building computer vision projects - a fruit recognition system called Jam Hot and a weather prediction system called Cirrus - and both failed because of fundamental dataset quality issues. I realized that for personal portfolio projects, acquiring high-quality datasets is often the insurmountable barrier to completion.

WhatNow solves that problem by generating its own training data. Every time I use it, I'm providing labeled examples of what activities I prefer given specific contexts. The AI doesn't need a massive pre-existing dataset - it learns from my actual usage over time. This meant I could actually finish the project and deploy it, rather than getting stuck in the data acquisition phase indefinitely.

The technical implementation uses contextual bandits, which is a form of reinforcement learning. I built a two-layer learning architecture with a Session AI for fast session learning and a Base AI for slow base learning. The system uses semantic embeddings to match user context with activities. Embeddings are vector representations of text that capture meaning. The system continuously improves over time based on user feedback.

The most significant technical pivot happened when I realized the manual metadata approach wasn't scalable. I had started with 17 activities that required 15+ manual metadata fields each. This created 30MB+ of manual data that was tedious to maintain and didn't scale to hundreds of activities. I completely pivoted to an AI-powered system using embeddings, eliminating all manual metadata. The database transformed from 17 activities with complex metadata to 1,250 activities with just name and AI embedding.

WhatNow represents one of my most successful portfolio projects, not just in terms of technical achievement but in demonstrating complete end-to-end machine learning engineering. The project is fully deployed, genuinely useful, and continues to improve through real usage.

---

**emotion:** happy
**suggestions:**
- How do you approach AI system design?
- What challenges have you faced?
- Tell me about your LLM experience
- How do you ensure AI system quality?
- What AI technologies are you learning?
- What projects have you built?

