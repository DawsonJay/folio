# How do you handle ambiguous requirements?

My approach is to frame the limits before jumping to solutions. Ambiguous requirements usually mean the stakeholder knows they have a problem but doesn't know what the solution looks like — so the first job is to understand the real problem, not to start building the imagined one.

The Integrations Dashboard started with "better access to backend data." That's not a requirement, it's a direction. Through conversations with both the backend team and the sales team who'd be using it, I learned what they actually needed: fast customer lookups, integration status checks, and troubleshooting tools — all without needing to understand backend database structure. That clarity completely shaped the architecture. Without it I'd have built the wrong thing.

Once I understand the problem, I make constraints explicit — what's fixed (the existing schema, the timeline, what the backend can serve) and what's flexible. That's usually where good solutions come from. When something is tightly constrained, you have to be clever rather than just building what's obvious. I'll also prototype early when requirements are genuinely unclear — stakeholders often can't articulate what they want until they can react to something concrete.

---

**emotion:** thinking
**suggestions:**
- Tell me about the Integrations Dashboard
- How do you approach problem-solving?
- Tell me about the Email Editor project
- Tell me about the Nexus Dashboard
- Tell me about moh-ami
- How do you handle scope creep?
