# How do you approach AI project scoping?

I've scoped and built multiple AI projects - some succeeded (WhatNow, moh-ami, Folio), some failed (Cirrus, Jam Hot). The difference was realistic scoping from day one. I think in terms of what I need and what resources I have. The intersection defines what's feasible. This isn't about what's theoretically interesting. It's about what I can actually complete given constraints of time, data, money, and expertise.

For WhatNow, I started with clear requirements. A project completable in about a month. Not reliant on data I don't control or have to collect myself. AI as a central mechanism, not peripheral. These constraints eliminated projects needing large datasets and focused scope on something achievable quickly. The recommendation system idea emerged from constraints - it could generate its own training data through usage, solving the data problem.

Before committing to an AI project, I check data availability first. What data do I need and how will I get it? Projects needing data I can't access are non-starters. I evaluate whether I can use existing AI services like LLMs and embeddings APIs or need to train models. Training adds complexity, requires data, takes much longer. Using APIs is almost always preferable for personal projects.

Cirrus and Jam Hot taught me what "too big" looks like. Cirrus failed because weather forecasting needs meteorological expertise I didn't have and serious data infrastructure. Jam Hot failed because music recommendation needs extensive listening history I couldn't obtain. Both persisted too long on unrealistic ambitions.

The question I ask before starting any AI project: what needs to be true for this to work, and can I actually make those things true? If the answer involves months of data collection or requires solving a problem that OpenAI hasn't solved, the project is mis-scoped. WhatNow, moh-ami, and Folio all passed that test. Cirrus and Jam Hot didn't.

---

**emotion:** thinking
**suggestions:**
- Tell me about WhatNow
- Tell me about Cirrus
- What AI/ML experience do you have?
- What is Folio?
- Tell me about moh-ami
- How do you approach adding LLM features?
