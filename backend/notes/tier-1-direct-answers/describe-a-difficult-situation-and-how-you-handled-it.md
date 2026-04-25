# Describe a difficult situation and how you handled it

Building Folio, the RAG-powered portfolio chatbot you're talking to right now, was a genuine pressure situation: I needed it working and deployed before I could start job applications. Not a theoretical deadline. The challenge was that cutting corners on the architecture would mean rebuilding it later, but spending too long on it meant not being able to apply.

The approach I used: build a structure capable of supporting the full product, but define the absolute minimum scope that actually works. I think of it like a trellis for a seedling — not so small it snaps under first load, not over-engineered for a plant that hasn't grown yet. The RAG system, embedding storage, and API structure had to be right from day one — those are too expensive to redo. But I didn't need every feature immediately.

The result is live, still growing, and the architecture is holding. I iterate on it regularly without structural rework — which is the test of whether the trellis was the right size.

Another difficult situation was optimizing the Nexus Dashboard performance from 15+ seconds to under 5 seconds. The initial implementation had severe performance problems that made the dashboard essentially unusable. Users waited staring at loading spinners wondering if the app was frozen. I handled it by thinking across the entire stack from database queries through API design to frontend rendering, implementing strategic loading, intelligent caching, and careful data management.

---

**shortTitle:** Tell me about a difficult situation?
**emotion:** thinking
**suggestions:**
- How do you handle tight deadlines?
- How do you handle stress and pressure?
- How do you approach problem-solving?
- Tell me about the Nexus Dashboard
- Tell me about a challenging project
- What is Folio?
