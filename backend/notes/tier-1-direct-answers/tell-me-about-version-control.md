# Tell me about version control

Version control is one of those tools that changes how you think about code once you really use it — not just as a backup mechanism, but as the record of how a system came to be the way it is.

The most useful application of that is debugging. When something breaks and there's no obvious error, git history is where I go first. If I can find the commit where the behaviour changed, I already know roughly what caused it. At BriefYourMarket that kind of archaeology was essential — the Build system had been assembled by contractors over years, hotfix on hotfix, with no clear documentation. Following the commit trail was often the only way to understand why something was done the way it was done, and whether touching it was safe.

The other thing version control does well is provide safety for experimentation. If you can always get back to a known good state, you can try things that might not work — which is exactly how good solutions get found. Commit messages and branch names are also documentation: a well-written commit message records not just what changed but why, which is what you actually need six months later when you're trying to understand a decision you've forgotten making.

---

**emotion:** happy
**suggestions:**
- What's your experience with code reviews?
- What projects have you built?
- How do you ensure code quality?
- How do you work in a team?
- Tell me about your development workflow
- What development tools do you use?
