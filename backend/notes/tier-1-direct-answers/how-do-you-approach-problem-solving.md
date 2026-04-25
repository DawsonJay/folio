# How do you approach problem-solving?

I start by framing limits before jumping to solutions. What do we actually know? What's fixed — the database schema, an external API, a performance constraint — and what's flexible? Getting that clear first stops me from solving the wrong version of the problem.

The other thing I rely on is pattern recognition from experience. I've worked across enough different systems — the Integrations Dashboard, Nexus, WhatNow, moh-ami — that new problems often match something I've seen before, even if the surface looks different. I'll follow that instinct but verify it: gather evidence, isolate variables (frontend or backend? all users or specific conditions?), and work through hypotheses in order of likelihood. On WhatNow I sensed the recommendation algorithm wasn't quite right before the metrics confirmed it. That kind of intuition is useful as a compass, not as proof.

I also try not to patch symptoms. If a bug is a sign of something structural, the fix needs to address the structure. The Integrations Dashboard running 3+ years without maintenance isn't because nothing went wrong during development — it's because when things did go wrong, I fixed them in ways that strengthened the system rather than working around it.

---

**emotion:** thinking
**suggestions:**
- Tell me about debugging a complex issue
- How do you handle failure?
- Tell me about the Integrations Dashboard
- Tell me about the Nexus Dashboard
- Tell me about moh-ami
- Tell me about WhatNow
