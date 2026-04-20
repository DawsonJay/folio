# How do you think about frontend architecture on a larger project?

Three things matter most upfront: consistency, containment, and purpose.

Consistency means one clear structure everyone follows. On the Email Editor at Nurtur the layout was strong — separate components for pages, hooks for API and drag-and-drop — but reuse had drifted. People built their own components without checking if something already existed, leaving a disorganised pool of similar pieces that should have been one. That makes bugs harder to reason about and duplicates effort.

Containment means wrapping third-party libraries behind clear boundaries. On Nexus I wrapped every Recharts component immediately — if surrounding code changed, only the wrapper was affected. If Recharts became a liability, I could swap another graphing library without detangling it from everywhere.

Purpose means designing structure around what the product actually needs to do. On Nexus the design wasn't fixed early and the backend might change significantly, so I prioritised adaptability above all else. That shaped every tool and structural decision.

Integrations aged well because the UI model matched what the product needed to do — hierarchy mirrors the backend, content grew outward without forcing rewrites. Build at BriefYourMarket — my first employer — built by contractors with no long-term stake, aged into something where only surgical fixes were possible: touch one area and failures cascade elsewhere. That experience is a lot of why I care upfront about these principles.

---

**shortTitle:** How do you think about frontend architecture?
**emotion:** thinking
**suggestions:**
- Tell me about the Nexus Dashboard
- Tell me about the Integrations Dashboard
- When do you refactor versus rewrite?
- How do you maintain a codebase solo?
- When does maintenance become improvement?
- What was your first development job?

**variants:**
- How do you approach frontend architecture on a large project?
- What structural decisions matter most to you at the start of a frontend project?
- How do you think about component organisation and scalability on the frontend?
