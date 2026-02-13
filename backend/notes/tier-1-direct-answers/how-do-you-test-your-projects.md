# How do you test your projects?

I've tested production systems for 3.5 years at Nurtur using Jest, React Testing Library, and Wallaby. Testing approach depends on the project's criticality and longevity. Production systems that people depend on get comprehensive testing. Personal experiments get selective testing or manual-only testing.

For work projects at Nurtur, I followed a consistent approach. Manual testing of common user actions first to ensure stability. Get a teammate to check it in the browser - fresh eyes catch things you miss. Run the existing test suite to verify nothing broke. Then write tests for the new feature using Jest and React Testing Library. I used Wallaby for continuous feedback as I developed.

My philosophy is testing user workflows rather than aiming for exhaustive coverage. I write tests that mimic what users actually do - logging in, creating items, navigating between pages. If users would never encounter a code path in normal usage, testing it exhaustively is lower priority than ensuring critical paths work reliably.

For personal projects like WhatNow and moh-ami, I'm more pragmatic. They have tests for critical functionality but less comprehensive coverage because there's no team relying on the codebase and the cost of a bug is lower. I still test user actions, but I'm selective about which actions need automated tests versus manual verification.

The Nexus Dashboard taught me to write tests incrementally. I didn't write tests at the start, and as complexity grew, manual testing everything took longer than coding. Retrofitting tests onto a complex system was a trial. Now I write tests as I build features rather than all at once later.

Testing effort matches what's at stake. The Integrations Dashboard's 3+ years without bugs came from thorough testing combined with simple architecture that's resistant to errors.

---

**emotion:** thinking
**suggestions:**
- What testing tools do you use?
- Tell me about your testing strategy
- How do you ensure code quality?
- Tell me about the Nexus Dashboard
- What was the Integrations Dashboard?
- How do you balance speed and quality?
