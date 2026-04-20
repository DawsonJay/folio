# How do you design for users with very different levels of technical knowledge?

The Integrations Dashboard was exactly this problem. One side was backend developers working with data normalisation code; the other was a sales team who needed to work with that data without seeing or understanding the underlying system. The challenge isn't usually the data itself — it's communicating the context around it intuitively for both.

The first move was hierarchy. The dashboard dealt with clients (large real estate companies), branches (individual offices within those companies), and sessions (millions of granular records per branch). Layering those as nested screens made it immediately clear what was a subset of what — without that structure it was just overwhelming flat data.

Simplification mattered as much as organisation. Traffic-light colours for statuses meant a failed processing job showed as red and was instantly visible without reading anything. All the raw data was still accessible by drilling down, but the default view showed only what a user actually needed at a glance.

I validated by releasing early, talking to both teams, and shipping frequently based on what they asked for. The original structure was designed to grow — adding new pages and controls was straightforward because the foundation anticipated it. Building in flexibility from the start is what makes that kind of iterative validation work.

---

**shortTitle:** How do you design for mixed audiences?
**emotion:** thinking
**suggestions:**
- Tell me about the Integrations Dashboard
- How do you work with non-technical people?
- How do you communicate technical concepts?
- How do you explain a technical decision?
- How do you work with designers?
- How would you build an AI detection UI?

**variants:**
- How do you design for both technical and non-technical users?
- How do you handle UX when your users have very different backgrounds?
- How do you build something that works for both engineers and non-engineers?
