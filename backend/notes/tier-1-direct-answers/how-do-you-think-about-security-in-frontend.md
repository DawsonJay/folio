# How do you think about security in frontend?

I start from the perspective of someone who wants to cause damage and ask: what areas of this system are most exposed? Exposed complexity is usually where vulnerabilities live. For user input, for instance, you could maintain an extensive blacklist of code-like strings — but that's a moving target. Simpler is to only allow alphanumeric input and ensure the data is always treated as a string, never executed. Simplicity is a better defence than cleverness.

At Nurtur I built auth systems for several dashboards that gave users direct control of company databases. A malicious action — or just an accidental one — could cause real damage. Part of the security was standard: role-based access controls, different permission levels per user. But a surprisingly large part was awareness. I built multi-stage confirmation flows for destructive actions, so if someone triggered something serious they did it with full knowledge of what they were doing. I also added audit logging so every action was traceable back to a user. Security often meant thinking about human error as much as technical attack surfaces.

---

**emotion:** thinking
**suggestions:**
- How do you approach problem-solving?
- How do you ensure code quality?
- How do you make technical decisions?
- Tell me about the Nexus Dashboard
- What's your backend development experience?
- How do you handle production bugs?

**variants:**
- What do you think about when it comes to frontend security?
- How do you approach security in web development?
- What security considerations do you keep in mind as a frontend developer?
