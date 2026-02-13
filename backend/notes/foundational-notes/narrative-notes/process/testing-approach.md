# Testing Approach and Philosophy

## What "Done" Means

Before I consider a feature or PR done, I go through several steps to ensure it's stable and reliable:

1. **Manual stability testing**: I make sure the feature is stable and doesn't break easily by going through common user actions. I test the typical workflows a user would follow to ensure the happy path works and edge cases are handled.

2. **Teammate review**: I get a team member to spend a couple of minutes checking it in the browser. Sometimes you work on something for so long you miss the obvious, and a fresh pair of eyes catches things I've overlooked.

3. **Regression testing**: I run the existing test suite to see if the rest of the site still works. This ensures my new feature hasn't broken existing functionality.

4. **Write new tests**: Once I know the feature is functional in its current state, I write tests to cover the new feature. I write tests knowing the feature currently works, which makes it easier to write accurate tests that verify the correct behavior.

## Testing Philosophy: Mimic User Actions

I don't write exhaustive tests that cover every possible edge case. Instead, I write tests that mimic common user actions. The goal is to ensure the critical paths through the application work correctly, not to achieve 100% code coverage.

This approach focuses testing effort where it matters most: the workflows users actually follow. If a user would never encounter a particular code path in normal usage, testing it exhaustively is lower priority than ensuring the main flows work reliably.

## The Nexus Dashboard Lesson

Testing helped a lot with the Nexus Dashboard project. I didn't bother writing tests at the start, but as the site expanded in complexity, every new feature required me to manually test everything on the site. To test properly would take longer than the coding itself.

Writing automated tests to cover the mimicked user actions meant I could just run the test suite after every major change. Instead of spending 30+ minutes clicking through every page and workflow, I could run the test suite in minutes and have confidence that everything still worked.

**The lesson**: I should have just written tests from the start. Having to write them all at once later was a trial. It's much easier to write tests incrementally as you build features than to retrofit them onto a complex system.

## Testing at Nurtur vs Side Projects

At Nurtur, I followed the approach described above: manual testing, teammate review, run existing tests, write new tests. The team environment made the teammate review step natural and valuable.

For side projects, I'm more pragmatic. Projects like WhatNow and moh-ami have tests for critical functionality, but the testing is less comprehensive because there's no team relying on the codebase and the cost of a bug is lower. I still follow the principle of testing user actions, but I'm more selective about which actions need automated tests.

## Tools and Frameworks

At Nurtur, we used **Jest** as the test runner and **React Testing Library** for component testing. I also used **Wallaby** as an intelligent test runner that provides continuous testing - it runs tests automatically as you code and shows results inline in the editor.

The combination works well: Jest provides the testing infrastructure, React Testing Library encourages testing from a user's perspective rather than implementation details, and Wallaby gives immediate feedback as you develop. This setup makes it easy to write tests that are maintainable as the codebase evolves.

The key is writing tests that describe what the application should do from a user's perspective, not tests that verify internal implementation. This makes tests more resilient to refactoring and more valuable as documentation of expected behavior. React Testing Library's philosophy aligns perfectly with this approach.

## When to Skip Testing

I don't test everything exhaustively. I skip or minimize testing for:

- One-off scripts or throwaway prototypes
- Simple display components with no logic
- Code that's clearly temporary or exploratory

The testing effort should match the criticality and longevity of the code. Production systems that other people depend on get comprehensive testing. Personal experiments get selective testing or manual-only testing.

