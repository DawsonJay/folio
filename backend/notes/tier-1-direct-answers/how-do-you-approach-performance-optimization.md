# How do you approach frontend performance optimization?

Performance problems are usually a symptom of structure, not just a specific bit of slow code. When something's slow, my first instinct is to get a high-level view of what's being fetched and why — not to dive straight into optimization.

The Nexus Dashboard is a good example. The page took so long you'd go and make a cup of tea while it loaded. It was immediately obvious we were fetching far more data than the screen needed. But the interesting problem wasn't just reducing the volume — it was thinking about *when* the user needs what. I structured the page into sections and layers so each part only fetches data when the user actually reaches it. The result was under 5 seconds from over 15.

What I find genuinely interesting about performance is how it reveals the shape of the code underneath. A well-structured system — modular, layered, designed with the future in mind — doesn't tend to develop these problems at scale. The bottlenecks that really hurt are the ones baked into the architecture, not the ones you can patch with a caching layer. That's what I focus on: getting the structure right so the performance follows.

---

**emotion:** thinking
**suggestions:**
- Tell me about the Nexus Dashboard
- How do you approach frontend architecture?
- Tell me about a technically challenging problem you've solved
- How do you ensure code quality?
- What's your experience with React?
- How do you approach technical debt?
