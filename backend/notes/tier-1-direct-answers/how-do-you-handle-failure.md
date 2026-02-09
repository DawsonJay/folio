# How do you handle failure?

Things fail all the time. That's not a problem - it's reality. The key is to make sure they don't fail in the same way twice. Failure is information. It tells you what doesn't work, what needs improvement, what assumptions were wrong. The question isn't whether things will fail. It's how you respond to failure and what you learn from it.

I like to think in terms of test-driven design and structure. If you've got a good structure, you don't get the same bugs twice and every bit of work you do makes everything else better. If you have a poor structure, you get the same problem over and over again but worse as the weight increases on a structure that can't support it.

Good architecture means that when something fails, you fix it in a way that prevents similar failures. The Integrations Dashboard's zero-maintenance record isn't because nothing ever went wrong during development - it's because when things did go wrong, I fixed them in ways that strengthened the overall system.

I think perfection is bad - it takes too long and is generally unwanted. I do things in broad brushstrokes and test it against the real world. Some things will fail, and those are the things I then improve as they're the parts that are actually needed.

When creating the Integrations and Nexus dashboards, I would take designs to the teams that would use the product and get feedback on them and make adjustments. Having frequent feedback means I got lots of small useful failures instead of large project-breaking ones.

This is the key insight: failure is inevitable, but the timing and scale matter enormously. Small failures early in development are valuable - they teach you what users actually need, what workflows make sense, what assumptions are wrong. Large failures late in development are expensive - they can break the project, waste months of work, or require complete rewrites.

The feedback loop strategy - showing work early and often, getting small failures frequently - prevents the catastrophic failures that can kill projects. It's better to have ten small course corrections than one massive failure that requires starting over.

Each failure taught something specific. Jam Hot taught me about validation vs. real-world accuracy. Cirrus taught me about data coverage and fundamental assumptions. Those lessons directly informed WhatNow's architecture.

Failure isn't something to avoid - it's something to manage. The goal isn't zero failures. The goal is failures that teach you something, failures that happen early and small, and failures that don't repeat because you've built better structure.

---

**emotion:** thinking
**suggestions:**
- Tell me about a project that failed
- Tell me about a mistake you made
- How do you approach problem-solving?
- What challenges have you faced?
- How do you ensure code quality?
- What did you learn from that project?

