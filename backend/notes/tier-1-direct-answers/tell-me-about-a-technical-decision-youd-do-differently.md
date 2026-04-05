# Tell me about a technical decision you made that you'd do differently now

The decision I keep coming back to is Cirrus — a Canadian weather AI project I built that I eventually had to scrap entirely.

The code was good. The idea was strong. But I never properly validated the data it depended on. The source was public meteorological data, and it turned out to be patchy, inconsistent, and scattered — 31% precipitation coverage, 0% wind speed. The whole prediction system was useless without reliable inputs, and I couldn't fix the data because it came from an outside source. I had to dispose of the entire project.

What I should have done first was exactly what I did for WhatNow later: build around a data source I could control. WhatNow's recommendation engine trains incrementally on user input — like using a waterwheel to power the project. The data problem became the design, not the obstacle.

The general lesson: before building anything substantial, sketch out what's genuinely foundational and investigate that first. If I'd done real analysis on the Cirrus data early, I'd either have built something different or saved months of work.

---

**shortTitle:** What technical decision would you redo?
**emotion:** thinking
**suggestions:**
- Tell me about Cirrus
- Tell me about WhatNow
- Tell me about a project that failed
- How do you approach AI project scoping?
- How do you ensure code quality?
- Tell me about a mistake you made
