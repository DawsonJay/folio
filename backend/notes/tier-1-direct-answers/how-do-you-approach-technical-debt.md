# How do you approach technical debt?

I think of it like housekeeping. If you try to keep everything absolutely immaculate you never get anything done — but there's a real difference between clutter on the table and a broken window.

My code structure is designed around that distinction. I keep things modular so when debt needs cleaning up, it's a self-contained section — safe to fix without risk. The structure itself I get right from the start, because structure is genuinely hard to retrofit. Variable names, minor inefficiencies, small shortcuts — that's clutter I can sweep up during a slower week. Structural problems calcify.

I learned this at BriefYourMarket. My first job was debugging a system called Build — assembled by contractors who had no incentive to care about maintainability. Over years, hotfix had been layered on hotfix until the whole thing was so entangled that touching anything caused cascades of bugs somewhere else. My job was surgical: find the cause, make the minimum change that affected nothing else. It showed me exactly what I never want to build — and why I'm careful about structure from the start.

I've shipped imperfect code — clutter I knew I'd clean up later. I've never shipped a broken window. I have to live in the codebase.

---

**emotion:** thinking
**suggestions:**
- Tell me about your time at BriefYourMarket
- How do you decide when to refactor versus rewrite?
- How do you approach frontend architecture?
- How do you ensure code quality?
- Tell me about the Integrations Dashboard
- How do you approach performance optimization?
