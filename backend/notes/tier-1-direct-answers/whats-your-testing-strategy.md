# What's your testing strategy?

I've tested production systems for 3.5 years at Nurtur using Jest, React Testing Library, and Wallaby. My strategy is to test the critical paths users actually follow, not every possible edge case. I write tests that mimic common user actions - logging in, creating items, navigating workflows - rather than aiming for 100% code coverage. The goal is confidence that the application works for real usage, not satisfying an arbitrary coverage metric.

I use Jest for test infrastructure, React Testing Library for component testing that focuses on user behavior, and Wallaby for continuous testing feedback. Tests verify what the application should do from a user's perspective, not internal implementation details. This makes tests resilient to refactoring and valuable as behavior documentation.

My process is to write tests after I know the feature works. I manually test it, get teammate feedback, verify existing tests pass, then add tests for the new functionality. Writing tests once behavior is correct means the tests encode actual requirements rather than initial assumptions that might be wrong.

The Nexus Dashboard experience shaped this strategy. Starting without tests meant every new feature required 30+ minutes of manual regression testing. Adding automated tests for user workflows meant running the suite in minutes with high confidence. The lesson was clear - write tests incrementally as you build, not all at once later.

Testing effort scales with criticality. The Integrations Dashboard serving the sales team daily got thorough testing. Personal experiments get selective testing. Production systems that people depend on need comprehensive user-flow coverage. Throwaway prototypes need much less.

---

**emotion:** thinking
**suggestions:**
- Tell me about the Nexus Dashboard
- Tell me about balancing quality and speed
- Tell me about the Integrations Dashboard
- How do you ensure code quality?
- Tell me about your testing practices
- How do you test your projects?
