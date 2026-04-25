# Tell me about the Email Editor project

The Email Editor was a rebuild of Nurtur's core product — the drag-and-drop email template system clients used daily for campaign creation. A four-person team, genuine business criticality, shared ownership across frontend and backend.

The team composition shaped the work as much as the technical requirements. Three of the four were backend developers transitioning into full-stack roles, which meant the collaboration involved a lot of explanation — helping them understand component thinking, CSS patterns, and state management in React while they were contributing to production code in parallel. The code reviews were more educational than gatekeeping: I'd explain why a CSS pattern worked the way it did, connect it to concepts they already had from backend development. By the time I moved to the Nexus project, all three were contributing to the frontend independently.

My main technical contribution was a link editor component built on the Lexical framework — Lexical is a rich text editing library with a plugin architecture, and building a custom plugin required understanding its state management and extension points in some depth. State across the editor used Redux Toolkit, which made sense given multiple developers working on interconnected features: centralised state gave everyone a clear place to look when something behaved unexpectedly.

The project continued without me when I moved to Nexus. That's how it should work — I was contributing to a team effort, not creating something that depended on me staying.

---

**emotion:** happy
**suggestions:**
- Have you mentored other developers?
- How do you work in a team?
- What's your biggest weakness?
- Tell me about the Nexus Dashboard
- Tell me about the Integrations Dashboard
- How do you approach UI/UX design?
