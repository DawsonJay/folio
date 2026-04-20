# How do you handle a legacy codebase?

The core principle is smallest possible change, smallest possible footprint.

Build at BriefYourMarket — my first employer — was the clearest example I've worked through. It had been built by contractors with no long-term stake: their incentive was to ship features fast, not to leave something maintainable. By the time I was working in it, it was hotfix on hotfix. Touching one area could cascade failures elsewhere, and nobody fully held the whole map in their head. Meaningful improvement wasn't on the table without something close to a rebuild.

So the work I did there was surgical: go in, fix the specific bug, get out. Not making it worse was roughly the best available outcome. Any wider change risked introducing failures in places that weren't obviously connected.

The lesson I took from that is about timing. The moment to address structural problems is before they compound — early signals like minor bugs that take longer to trace than they should, components that are harder to extend than expected, surprising load delays. On Nexus I addressed those signals as they appeared. It cost less effort spread across the project than one big remediation would have, and it kept the codebase flexible for years. Legacy debt is expensive precisely because it's invisible until it isn't — and by then the cost of fixing it has multiplied.

---

**emotion:** thinking
**suggestions:**
- When does maintenance become improvement?
- When do you refactor versus rewrite?
- What was your first development job?
- How do you think about frontend architecture?
- How do you approach technical debt?
- Tell me about debugging a complex issue

**variants:**
- How do you approach working with old or inherited code?
- What do you do when you inherit a poorly written codebase?
- How do you work in a codebase with a lot of technical debt?
