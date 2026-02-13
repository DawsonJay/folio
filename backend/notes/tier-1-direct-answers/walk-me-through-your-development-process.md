# Walk me through your development process

I start by understanding the real problem, not just the stated requirements. Often stakeholders know they have a problem but can't articulate the solution. I ask why they need this, what success looks like, and who the users are. The Integrations Dashboard started with "better access to backend data" but conversations revealed they needed quick customer lookups and troubleshooting tools without understanding database structure.

Once I understand the problem, I define constraints. What's fixed versus flexible? What systems can't change? What's the timeline and budget? This frames what's possible. Then I define the MVP - the minimum that delivers core value with structure to expand later. I use a backlog for everything else so nothing is forgotten but nothing derails the initial build.

For implementation, I create a branch, build with React/TypeScript, write tests for critical paths, and do manual testing before creating a PR. Code review is central - I review teammates' PRs with educational feedback explaining why patterns work, and I treat feedback on my code as learning opportunities. Git provides safety nets for experimentation and documents decision-making through commit messages.

I work in small iterations, gathering feedback throughout rather than waiting until something is "done." On the Integrations Dashboard, talking at length with both backend and sales teams as I worked revealed what was valuable and what wasn't. Real feedback makes real value.

Testing matches criticality. Production systems get comprehensive user-flow testing with Jest and React Testing Library. I use Wallaby for continuous feedback. The Nexus Dashboard taught me to write tests incrementally rather than retrofitting them later.

I prioritize based on value versus effort and user impact. What moves the needle most? What unblocks other work? I protect deep focus time for complex problems and batch similar tasks to minimize context switching.

---

**emotion:** thinking
**suggestions:**
- How do you handle ambiguous requirements?
- Tell me about the Integrations Dashboard
- What testing approach do you use?
- How do you prioritize tasks?
- Tell me about your development workflow
- How do you gather user feedback?
