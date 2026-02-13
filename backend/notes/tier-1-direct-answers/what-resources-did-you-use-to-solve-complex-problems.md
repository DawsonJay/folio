# What resources did you use to solve complex problems?

Documentation first, community second, experimentation always. For the WhatNow contextual bandit implementation, I read academic papers on epsilon-greedy algorithms and reinforcement learning fundamentals, consulted scikit-learn documentation for existing implementations, and tested different parameter values systematically to understand behavior.

When the Nexus Dashboard performance issues arose, I used React Query documentation to understand caching strategies, searched Stack Overflow and GitHub issues for similar performance patterns, profiled the actual network requests using Chrome DevTools to see what was slow, and consulted with the backend engineer about API constraints and optimization possibilities.

I favor official documentation over tutorials because documentation is accurate and complete, while tutorials often skip edge cases or use outdated patterns. But community resources (Stack Overflow, GitHub issues, blog posts) are invaluable for seeing how others solved similar problems and learning about approaches I wouldn't have considered.

Experimentation is critical. Reading about solutions isn't the same as implementing them. For WhatNow's embeddings approach, I tested multiple sentence transformer models (`all-MiniLM-L6-v2`, `all-mpnet-base-v2`) to compare speed and quality. For Nexus loading optimization, I tried different buffer strategies and measured actual impact rather than assuming what would work.

The best resource is often teammates. When stuck on the Email Editor's Lexical framework integration, discussing the problem with backend developers (even though they weren't frontend experts) helped clarify my thinking. Rubber ducking works - explaining the problem reveals gaps in understanding.

---

**emotion:** thinking
**suggestions:**
- How do you approach problem-solving?
- Tell me about debugging a complex issue
- How do you learn new technologies?
- What's your debugging process?
- Tell me about the WhatNow project
- Tell me about the Nexus Dashboard
