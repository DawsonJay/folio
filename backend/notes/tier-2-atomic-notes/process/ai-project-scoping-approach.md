# AI Project Scoping Approach

I've scoped and built multiple AI projects - some succeeded (WhatNow, moh-ami, Folio), some failed (Cirrus, Jam Hot). The difference was realistic scoping from day one.

## Core Approach

I think in terms of what I need and what resources I have. The intersection defines what's feasible. This isn't about what's theoretically interesting or technically impressive. It's about what I can actually complete given constraints of time, data, money, and expertise.

## Before Committing to an AI Project

**Check data availability first**: What data do I need and how will I get it? Projects needing data I can't access are non-starters.

**Evaluate AI services vs training models**: Can I use existing AI services like LLMs and embeddings APIs, or do I need to train models? Training adds complexity, requires data, takes much longer. Using APIs is almost always preferable for personal projects.

**Define clear requirements upfront**: For WhatNow, I started with clear requirements - completable in about a month, not reliant on data I don't control, AI as a central mechanism. These constraints eliminated projects needing large datasets and focused scope on something achievable quickly.

## Rules of Thumb

**"Too big" looks like**: Cirrus failed because weather forecasting needs meteorological expertise I didn't have and serious data infrastructure. Jam Hot failed because music recommendation needs extensive listening history I couldn't obtain. Both persisted too long on unrealistic ambitions.

**"Scoped right" looks like**: WhatNow, moh-ami, and Folio succeeded because they were scoped around data I could access, used existing AI services rather than building from scratch, and had clear success metrics.

## The Critical Question

Before starting: what needs to be true for this to work, and can I make those things true? If the answer involves months of data collection or beating OpenAI, the project is mis-scoped.

My approach favors using existing AI services rather than training models from scratch. OpenAI API, embedding services, and established frameworks let me build production applications quickly. I focus effort on product design, user experience, and integration rather than reinventing AI infrastructure.
