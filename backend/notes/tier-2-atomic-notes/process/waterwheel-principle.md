# The Waterwheel Principle — Building Around Controllable Resources

## The Principle

When designing a project, identify what is genuinely foundational — what the whole system depends on — and investigate that first. If the foundation is outside your control, redesign so the foundation is something you can control.

The waterwheel is the metaphor: you don't fight the river, you build something the river powers. The constraint becomes the design.

## Where It Came From — Cirrus

Cirrus was a Canadian weather AI prediction system. The code was good, the architecture was solid, and the idea was strong. But the whole system depended on public meteorological data I didn't control: precipitation coverage at 31%, wind speed at 0%, humidity missing. The prediction system was useless without reliable inputs, and there was nothing I could do about the data because it came from an outside source.

I had to scrap the entire project.

What I should have done first: sketch out what's genuinely foundational to the project and validate that it's actually achievable before building anything around it. If I'd done real analysis on the Cirrus data at the start, I'd have either built something different or saved months of work.

## The Application — WhatNow

WhatNow needed a recommendation engine, and recommendation engines typically need large amounts of training data — user behaviour, ratings, interaction history. I didn't have that. Collecting it would have taken months.

The waterwheel move: instead of treating data acquisition as a problem to solve before building, I made data acquisition the design. WhatNow trains incrementally on user input — each interaction with the system generates the training signal for the next recommendation. The system generates its own data through usage.

The data problem became the product. No external dependency. No data acquisition phase. The foundation was something I controlled.

## The General Lesson

Before building anything substantial:
1. Identify what's genuinely foundational — what the entire system depends on to function
2. Validate that the foundation is achievable with the resources you actually have
3. If it isn't, redesign so the foundation is something you control

This applies beyond AI projects. Any system that depends on an external dependency — a data source, an API, a third-party service, a team's decisions — needs that dependency validated early. If it's not there when you need it, everything built on top of it is waste.

## Connection to Other Principles

This principle connects to how I approach project scoping generally: define the minimum viable foundation, then build up from there. The trellis has to be right from the start — everything else can be added later. But a wrong foundation can't be retrofitted; it shapes every decision made after it.
