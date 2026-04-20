# How do you handle accessibility?

I build with it in mind from the start now, but that wasn't always the case — and the thing that changed it was a dev training day.

We split into pairs and the task was to add tests to an existing codebase. The code turned out to be my own, something I'd been working on for months. We wanted tests that behaved like a real user — finding a button by its label, its type, that kind of thing. The structure for that wasn't there, and when we tried to fall back on ARIA labels, I hadn't added those either. It was awkward. I made a joke about obviously knowing what I'd be working on when we went back to our desks, and people ran with it. But it genuinely landed.

The lesson that stuck: testing tools and accessibility tools read a UI in similar ways. They both depend on semantic structure, meaningful labels, and elements that make sense independent of visual context. If a test can't find a button without resorting to nth-child selectors, a screen reader is having the same problem. Building with semantic HTML, proper labels, and accessible interactive elements isn't a separate concern — it's the same foundation.

I wouldn't describe myself as a WCAG auditor, but I'm not treating accessibility as optional either.

---

**emotion:** happy
**suggestions:**
- How do you test your projects?
- How do you ensure code quality?
- How do you work with designers?
- Tell me about your frontend experience?
- What's your strongest React skill?
- How do you approach UI/UX design?

**variants:**
- How do you approach accessibility in your frontend work?
- Do you think about accessibility when building UIs?
- How accessible is the code you write?
