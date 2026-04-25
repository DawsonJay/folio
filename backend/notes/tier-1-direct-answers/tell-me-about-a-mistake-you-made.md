# Tell me about a mistake you made

Building WhatNow's recommendation system, I set the exploration parameter too low — epsilon at 0.05, meaning the algorithm favoured exploiting what it already knew over exploring new options 95% of the time. The system worked correctly. The code did exactly what I wrote it to do. That was the problem.

The mistake was a design assumption I didn't question. I tuned the parameter conservatively to avoid erratic recommendations, but didn't think hard enough about what "safe" recommendations would feel like over time — samey, predictable, not exciting. Users couldn't articulate what was wrong, and my metrics didn't flag it because engagement looked acceptable. I was measuring the wrong things.

I caught it because something felt off, spent a week investigating until I understood it, then adjusted epsilon to 0.15 and added diversity metrics to track. Category diversity increased 40%, average semantic distance between recommendations increased 25%, and the system started feeling genuinely exploratory. An algorithm doing exactly what you told it to do can still be wrong if you didn't think carefully enough about what you were actually asking for.

---

**emotion:** thinking
**suggestions:**
- Tell me about a project you learned from
- How do you handle failure?
- Tell me about WhatNow
- What's your debugging process?
- How do you ensure code quality?
- Tell me about a project that failed
