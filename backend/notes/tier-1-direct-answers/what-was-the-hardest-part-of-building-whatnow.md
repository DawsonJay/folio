# What was the hardest part of building WhatNow?

The hardest challenge was debugging invisible bias in the recommendation algorithm. The system was working - no crashes, no errors - but recommendations felt "samey." Metrics showed acceptable click-through rates, so data didn't flag it as a problem. Users (me) couldn't articulate what was wrong, just that it was "okay but not exciting."

I spent a week investigating before finding the root cause. The contextual bandit's exploration parameter was too low at 0.05 (5% exploration, 95% exploitation). This meant the algorithm showed "safe" recommendations 95% of the time, which performed acceptably but prevented discovering genuinely new experiences. The bug was in my design choices, not my implementation. The code worked perfectly - it was doing exactly what I told it to do.

This was harder than any stack overflow or memory leak because there was no error message, metrics didn't show it, and feedback was subjective. I had to rely on intuition first (something feels off), then investigate rigorously through hypothesis testing. I checked training data balance, visualized embedding clusters, and eventually isolated the exploration rate.

The fix was simple once I understood the problem - increase epsilon from 0.05 to 0.15. Recommendations immediately became more diverse and engaging. The lesson: the hardest bugs aren't dramatic crashes - they're subtle issues where the system works but doesn't work well. Finding them requires intuition, deep understanding of algorithms, and systematic investigation beyond just reading error logs.

The other major challenge was the metadata-to-embeddings pivot in October 2025, but that was architectural rather than debugging.

---

**shortTitle:** What was hardest about building WhatNow?
**emotion:** thinking
**suggestions:**
- Tell me about debugging a complex issue
- What's the hardest technical challenge?
- How do you approach problem-solving?
- Tell me about WhatNow
- What's your debugging process?
- What did you learn from building WhatNow?

**projectLinks:**
- WhatNow:
  - demo: https://whatnow.onrender.com/
  - github: https://github.com/yourusername/whatnow
