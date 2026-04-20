# AI in the Development Workflow: Discipline Under Pressure

## How AI Changed My Coding Habits

Working heavily with AI development tools hardened my solo coding discipline more than anything else. Not because AI is dangerous to use — because it's powerful and that power requires structure to manage well.

AI makes sweeping changes without full context. It'll refactor broadly without understanding the architectural intent behind what it's touching. It'll generate code that looks correct but silently breaks assumptions elsewhere. The first time you let it run without sufficient constraints, you learn quickly that the problem isn't the AI — it's that your codebase wasn't structured to make its behaviour safe and reversible.

## The Habits AI Forced Me to Build

To stay on top of AI assistance, I developed tight habits that turned out to be good general engineering practice:

Small, modular components where any change only affects one contained area. This is good practice regardless of AI — but working with AI made it non-negotiable. If a component is too large or tangled, an AI change to one part can ripple unpredictably.

Careful review of everything AI produced, treating its output like a PR from a new developer who doesn't fully know the codebase yet. Not accepting output blindly — understanding what changed and why.

Tests around core mechanics of the code so it doesn't quietly drift from what it was supposed to do. AI is particularly good at introducing drift: changes that look right in isolation but shift behaviour in subtle ways.

These habits began as a response to AI, but they're general now. AI was just the high-pressure force that made them non-negotiable. I'd worked toward clean modular code before — AI made the cost of not doing it concrete and immediate.

## Dev Logs as AI Memory Layer

The other change AI prompted was writing dev logs consistently. AI assistants don't retain knowledge between sessions — every time you start a new chat, you're working with a fresh context that knows nothing about your project's history, your architectural decisions, or the edge cases you've already solved.

Dev logs solve this. Before starting a session, I update the AI's context from the logs rather than from raw code. It reads a concise, purpose-built record of what's been built, why decisions were made, and what problems have been solved. That produces better, more accurate assistance — and makes the sessions cheaper, since the model doesn't need to derive context from first principles every time.

## Treating AI Like a Capable Colleague

The mental model I've settled on: AI is a capable but context-starved colleague. It needs clear briefs, contained tasks, and careful review of what it produces. It works best in well-structured codebases where changes are scoped and reversible. Used that way, it's genuinely fast and helpful. Used without discipline, it introduces debt that costs more to fix than the speed it saved.

This isn't a negative view of AI tools — it's a realistic one. The skill in working with AI well is less about prompting and more about maintaining the kind of codebase that makes AI safe and useful to work in.
