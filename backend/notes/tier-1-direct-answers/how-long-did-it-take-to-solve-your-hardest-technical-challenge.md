# How long did it take to solve your hardest technical challenge?

The invisible bias in WhatNow's recommendation algorithm took a week to debug. The system was working - no crashes, no errors - but recommendations felt "samey." Metrics looked acceptable, so data didn't flag it as a problem.

Day 1-2: I knew something was wrong but couldn't articulate what. The intuitive feeling that the system wasn't quite right, even though everything looked fine on paper. Day 3-4: Systematic investigation - checking training data balance, visualizing embedding clusters, testing different hypotheses. Everything looked structurally sound. Day 5-6: Deeper investigation into the algorithm itself. Reviewing the contextual bandit implementation, checking parameters, understanding why "safe" recommendations dominated. Day 7: Found it - the exploration parameter (epsilon) was too low at 0.05. This meant 95% exploitation (safe choices) and only 5% exploration (discovering new things). The code worked perfectly; the design choices were wrong.

The fix took 5 minutes once I understood the problem - change epsilon from 0.05 to 0.15. Recommendations immediately became more diverse and engaging.

A week sounds like a long time for a 5-minute fix, but the debugging process was crucial. Without understanding the root cause, I would have made random changes hoping something worked. The week of investigation meant I understood exactly why the fix worked and could make informed decisions about other algorithm parameters.

The lesson: hard problems require time to understand, not just time to fix.

---

**emotion:** thinking
**suggestions:**
- What's the hardest technical challenge you've solved?
- Tell me about debugging a complex issue
- What was the hardest part of building WhatNow?
- How do you approach problem-solving?
- What's your debugging process?
- Tell me about the WhatNow project
