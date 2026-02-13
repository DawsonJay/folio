# Tell me about your testing practices

Before I consider a feature done, I go through four steps. I manually test common user actions to ensure stability. I get a teammate to check it in the browser because fresh eyes catch things you miss after working on something too long. I run the existing test suite to verify nothing broke. Then I write tests for the new feature once I know it works correctly.

I use Jest as the test runner, React Testing Library for component testing, and Wallaby as an intelligent test runner that shows results inline as you code. This combination encourages writing tests from a user's perspective rather than implementation details, making them maintainable as code evolves.

My testing philosophy is to mimic common user actions rather than aim for exhaustive coverage. The goal is ensuring critical paths work correctly, not achieving 100% code coverage. If users would never encounter a code path in normal usage, testing it exhaustively is lower priority than ensuring main flows work reliably.

The Nexus Dashboard taught me this lesson the hard way. I didn't write tests at the start, but as complexity grew, manually testing everything took longer than the coding. Adding automated tests meant I could run the suite in minutes instead of spending 30+ minutes clicking through workflows. I should have written tests from the start - retrofitting them onto a complex system was a trial.

Testing effort matches code criticality. Production systems get comprehensive testing. Personal experiments get selective testing or manual-only testing. The Integrations Dashboard's 3+ years without bugs came from thorough testing combined with simple architecture.

---

**emotion:** thinking
**suggestions:**
- How do you decide what to test?
- What was the Nexus Dashboard complexity?
- Tell me about your development workflow
- How do you ensure code quality?
- What testing tools do you use?
- How do you handle test failures?
