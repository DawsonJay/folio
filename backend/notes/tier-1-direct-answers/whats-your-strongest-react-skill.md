# What's your strongest React skill?

State management. Race conditions and multiple sources of truth are among the most common problems in large React codebases, and many developers find them hard to manage when state is scattered throughout a project. I'm good at building a structure that enforces a single clear state and exposes it in a way that avoids prop drilling — using hooks and context to give components what they need without tightly coupling them.

On the Nexus Dashboard, that strength mattered directly. The dashboard handled complex filter logic, accepted data from multiple asynchronous API calls, and combined those into larger data structures that needed to stay consistent under constant updates. The state layer I built kept all of that stable and bug-free through the full development cycle.

Folio pushed it further. I built a custom event system using hooks and context to coordinate multiple independent concerns: when the API responds to a question, the suggestions list updates, the answer renders, and the animated avatar cycles through emotion states. Each of those concerns is compartmentalised and can change independently without triggering cascades. The architecture stayed clean as Folio grew in complexity.

---

**emotion:** thinking
**suggestions:**
- Tell me about the Nexus Dashboard
- What is Folio?
- Tell me about your experience with React
- What state management libraries do you know?
- How do you approach problem-solving?
- What's your experience with TypeScript?

**variants:**
- What area of React are you strongest in?
- What's your best React skill?
- Where in React do you have the most depth?
