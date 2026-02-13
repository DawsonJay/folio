# Tell me about a mistake you made

The hardest bug I've fixed wasn't a crash - it was invisible bias in WhatNow's recommendation algorithm. The system worked, metrics looked fine, but user feedback suggested recommendations felt samey. Not obviously wrong, just not diverse enough.

I spent a week debugging before realizing my contextual bandit's exploration parameter was too low. Epsilon was 0.05, meaning 5 percent exploration and 95 percent exploitation. The algorithm showed safe recommendations that performed acceptably, so metrics didn't flag problems. But users weren't discovering genuinely new experiences.

What made this hard - no error messages, the system worked exactly as coded, metrics showed acceptable engagement, and users couldn't articulate what felt wrong. The bug was in my design choices, not implementation. I wasn't measuring the right things.

I changed epsilon from 0.05 to 0.15, implemented adaptive exploration, and added diversity metrics to track. Category diversity increased 40 percent, semantic distance between recommendations increased 25 percent, and users reported feeling like they were discovering things.

What I learned - trust intuition then prove it, metrics can lie by omission, sometimes the bug is the design, and user feedback matters even when vague. Deep understanding beats trial and error. This required seeing what wasn't there - recommendations users never got to experience.

---

**emotion:** thinking
**suggestions:**
- What did you learn from that mistake?
- How do you handle failure?
- Tell me about WhatNow project
- How do you approach debugging?
- What challenges have you faced?
- How do you ensure code quality?

