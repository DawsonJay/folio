# How do you test your projects?

My philosophy is testing user workflows rather than chasing coverage numbers. I write tests that mimic what users actually do — the paths they follow, the actions they take — rather than testing every possible code path. If a user would never encounter a particular path in normal usage, testing it exhaustively is lower priority than ensuring the critical flows work reliably.

At Nurtur I used Jest and React Testing Library with Wallaby running in the background as a continuous runner. My process on any new feature was: manual stability check first, get a teammate to take a fresh look in the browser, run the existing test suite, then write tests for the new feature. That order matters — I'd rather know the feature works before I write tests to document that it works.

The Nexus Dashboard taught me an expensive lesson: I didn't write tests at the start, and as the system grew in complexity, manually verifying everything after each change took longer than the coding itself. Retrofitting tests onto a complex codebase is genuinely painful. Now I write them incrementally as features land. For personal projects like WhatNow and moh-ami, I'm more selective — critical functionality is covered, but the test suite is lighter because the cost of a bug is lower and there's no team depending on the codebase.

---

**emotion:** thinking
**suggestions:**
- Tell me about the Nexus Dashboard
- Tell me about moh-ami
- Tell me about the Integrations Dashboard
- Tell me about WhatNow
- How do you ensure code quality?
- Tell me about your testing practices
