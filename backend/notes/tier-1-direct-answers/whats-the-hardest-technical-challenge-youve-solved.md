# What's the hardest technical challenge you've solved?

The hardest bug I've fixed was invisible bias in WhatNow's recommendation algorithm. The system was working - no crashes, no errors - but recommendations felt "samey." Metrics showed acceptable click-through rates, so data didn't flag it as a problem. Users couldn't articulate what was wrong, just that it was "okay but not exciting."

I spent a week debugging before I realized the problem. The contextual bandit's exploration parameter was too low at 0.05 (5% exploration, 95% exploitation). This meant the algorithm showed "safe" recommendations 95% of the time, which performed acceptably but prevented users from discovering genuinely new experiences. The bug was in my design choices, not my implementation. The code worked perfectly - it was doing exactly what I told it to do.

This was harder than any stack overflow or memory leak because there was no error message, metrics didn't show it, and feedback was subjective. I had to rely on intuition first (something feels off), then investigate rigorously through hypothesis testing. I checked training data balance, visualized embedding clusters, and eventually isolated the exploration rate as the culprit.

The fix was simple once I understood the root cause - increase epsilon from 0.05 to 0.15. Recommendations immediately became more diverse and engaging. The lesson was that the hardest bugs aren't dramatic crashes - they're subtle issues where the system works but doesn't work well. Finding them requires intuition, deep understanding of algorithms, and systematic investigation beyond just reading error logs.

---

**shortTitle:** What's the hardest technical challenge?
**emotion:** thinking
**suggestions:**
- Tell me about debugging a complex issue
- Tell me about WhatNow
- How do you approach problem-solving?
- What's your debugging process?
- Tell me about a challenging project
- What did you learn from building WhatNow?
