# AI Project Scoping

## The Framework: Needs and Resources

When I approach an AI project, I think in terms of what I need and what resources I have. The intersection of needs and resources defines what's feasible.

This isn't about what would be theoretically interesting or technically impressive. It's about what I can actually complete given the constraints of time, data, money, and expertise.

## The WhatNow Example

For WhatNow, I started with clear requirements:

**What I needed**:
- A project I could complete in about a month
- Not reliant on online sources of data I don't control
- Not dependent on data I had to collect myself or pay for
- AI as a central mechanism, not just a peripheral feature

**These constraints shaped everything**: They eliminated projects that needed large existing datasets, ruled out anything requiring extensive data collection, and focused the scope on something achievable quickly.

**The idea came from the constraints**: Once I knew what was feasible, the idea for a recommendation system emerged. The system could generate its own training data through usage, solving the data problem. The recommendation system concept fit within a month of development time. The AI was central to the value proposition.

**Then I worked out the minimum version**: What's the simplest recommendation system that actually provides value? Context inputs (mood, energy, time available) + activity database + recommendation engine + feedback mechanism for learning. That became the MVP.

## What to Check First

Before committing to an AI project, I check:

**Data**: What data do I need and how will I get it? Can I generate it, use existing datasets, collect it myself, or do I need to pay for it? Projects that need data I can't access are non-starters.

**Feasibility**: Is this technically achievable with my current skills and the tools available? Am I trying to build something that requires a research lab and 10 PhD students, or is it realistic for one person?

**API vs training**: Can I use existing AI services (LLMs, embeddings APIs) or do I need to train my own models? Training adds complexity, requires data, and takes much longer. Using APIs is almost always preferable for personal projects.

**Timeline**: Can I build a working version in a reasonable time frame (weeks to a few months)? Projects that would take a year+ are too big for portfolio work.

**Clear metric**: How will I know if it's working? AI projects need some way to evaluate success. If I can't define what "working" means, the project is too vague.

## Rules of Thumb

**"This is too big" indicators**:
- Needs data I have to collect over months
- Requires training complex models from scratch
- Success depends on beating state-of-the-art systems
- Would take more than 3-4 months to get a working version
- Requires domain expertise I don't have and can't quickly learn

**"This is scoped right" indicators**:
- Can use existing AI services (OpenAI API, embeddings, etc.)
- Data can be generated through usage or obtained readily
- Can build an MVP in weeks, not months
- Success is about solving a specific problem, not competing with Google
- Fits within one or two key technical challenges, not ten

## Lessons from Failures: Cirrus and Jam Hot

**Cirrus** (weather prediction system) failed because:
- Domain complexity: Weather forecasting requires meteorological expertise I didn't have
- Data infrastructure: Needed ongoing data acquisition, storage, validation - serious infrastructure
- Unrealistic ambition: Trying to compete with professional weather services was hubris
- Scope creep: Each requirement expanded the project until it would have taken years

**Jam Hot** (music recommendation) failed because:
- Data bottleneck: Music recommendation needs extensive listening history and mood labels
- Domain complexity: Audio features, music theory, mood classification all required deep knowledge
- Overambition: Attempting a sophisticated system as a first AI project
- Persistence too long: Should have pivoted earlier when data challenges became apparent

**What I learned**: Scope AI projects around data I can access, use existing AI services rather than building from scratch, start small and expand rather than planning something comprehensive upfront, and pivot early when fundamental constraints appear.

## How This Shapes Current Projects

**WhatNow**: Scoped around generating its own data, realistic completion timeline, used existing ML approaches (contextual bandits) rather than novel research.

**moh-ami**: Used existing LLM services rather than training models, focused on one specific problem (translation learning), built in days not months.

**Folio**: Used existing embedding services, focused on one narrow use case (portfolio chatbot), designed for iterative improvement rather than trying to be perfect upfront.

These projects succeeded where Cirrus and Jam Hot failed because they were scoped realistically from the start, worked within resource constraints, and used existing AI capabilities rather than trying to build everything from scratch.

## The Key Question

Before starting an AI project, I ask: **"What needs to be true for this to work, and can I make those things true?"**

If the answer involves "need six months of data collection" or "need to train a model better than what OpenAI has" or "need a team of people," the project is mis-scoped. If the answer is "need to use embeddings API and build a retrieval system," that's achievable.

Realistic scoping is what separates finished AI projects from perpetually-in-progress experiments.

