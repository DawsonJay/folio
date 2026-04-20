# AI as a Development Tool: How It Hardened My Coding Discipline

Working heavily with AI tools hardened my coding discipline more than anything else. Not because AI is dangerous — because it's powerful and that power requires structure to manage well.

AI makes sweeping changes without full context. It refactors broadly without understanding architectural intent. It generates code that looks correct but silently breaks assumptions elsewhere. The first time you let it run without sufficient constraints, you learn quickly that the problem isn't the AI — it's that the codebase wasn't structured to make its behaviour safe and reversible.

To stay on top of AI assistance, I developed habits that turned out to be good general engineering practice: small modular components where changes only affect one contained area; careful review of everything AI produced, treating its output like a PR from a new developer who doesn't fully know the codebase; and tests around core mechanics so the code doesn't quietly drift from what it's supposed to do. AI is particularly good at introducing drift — changes that look right in isolation but shift behaviour in subtle ways.

These habits began as a response to AI, but they're general now. AI was just the high-pressure force that made them non-negotiable.

The mental model I use: AI is a capable but context-starved colleague. It needs clear briefs, contained tasks, and careful review of what it produces. It works best in well-structured codebases where changes are scoped and reversible. Dev logs serve as AI memory — before starting a session I update the AI's context from the logs rather than from raw code, which produces better assistance and makes sessions cheaper. The skill in working with AI well is less about prompting and more about maintaining a codebase that makes AI safe and useful to work in.
