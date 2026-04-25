# Tell me about a project you learned from

Jam Hot — a computer vision project for fruit recognition that I stopped because the model didn't work in the real world. On the Fruit-360 dataset it achieved 86% validation accuracy. With actual photos taken in normal conditions, 0%. The dataset had been captured in a controlled environment: consistent lighting, clean backgrounds, perfect angles. Real fruit doesn't look like that.

The lesson wasn't technical — it was about data and scope. The dataset I was depending on was the wrong shape for the problem I was trying to solve, and I had no way to fix that without building a completely different dataset from scratch.

WhatNow came directly out of that failure. The key design decisions were all shaped by what went wrong with Jam Hot:

The data problem became the design. Instead of sourcing external datasets I couldn't control, WhatNow generates its own training data through usage — every interaction I have with it provides a labeled example. The system learns from me, not from a dataset someone else built.

Scope was defined by what I could actually finish. Jam Hot attempted comprehensive fruit recognition across many categories with no clear endpoint. WhatNow focused on one thing: activity recommendations using a specific algorithm. A constrained, completable scope.

Real-world performance replaced academic metrics. Jam Hot looked successful on paper right up until it didn't work. WhatNow validates against actual use — if recommendations feel right, the system is working. I use it in daily life, so the quality of its output is something I experience directly.

The result is a production-deployed AI system I use every day. The contrast with Jam Hot is the point.

---

**emotion:** thinking
**suggestions:**
- How do you handle failure?
- What AI/ML experience do you have?
- How do you approach adding LLM features?
- Tell me about WhatNow
- Tell me about Cirrus
- Tell me about a project that failed
