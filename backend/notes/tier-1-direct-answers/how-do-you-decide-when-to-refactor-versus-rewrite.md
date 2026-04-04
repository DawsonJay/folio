# How do you decide when to refactor versus rewrite?

Code structure guides direction — it tells future developers where to go next, and the easiest path is working with the grain of it.

When I need to change something, the question I ask is: am I bending the structure slightly, or fighting it? Refactoring is the right call when the change fits the shape of the existing system — even if it's significant work. Rewriting is the right call when the structure is pushing in the wrong direction and anything short of starting over means working against the nature of the code. If you fight the structure long enough, you end up rewriting it anyway — just slowly and painfully and in pieces.

It's an instinct as much as an analysis, but it's an instinct built on knowing the system well. I keep one eye on the project as a whole, so I usually have a clear sense of whether what I'm trying to do fits the shape of what's there.

The clearest case where rewriting was obviously right was Build at BriefYourMarket — hotfixes on hotfixes over years, completely organic, impossible to maintain safely. That call wasn't mine to make at the time, but it was an obvious one.

---

**emotion:** thinking
**suggestions:**
- Tell me about your time at BriefYourMarket
- How do you approach technical debt?
- How do you approach frontend architecture?
- How do you ensure code quality long-term?
- Tell me about a technical decision you'd do differently
- How do you approach debugging?
