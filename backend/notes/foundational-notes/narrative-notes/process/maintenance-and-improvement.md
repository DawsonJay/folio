# Maintenance vs Improvement: Getting the Timing Right

## The Core Distinction

Maintenance keeps something stable — no bugs, no structural drift that will unravel later. Improvement moves it toward a better state. The line between them is real, but it's often about what's actually at risk.

The trap is treating visible improvement as the only kind that matters. I think of neglected internals like a stage prop: it looks real from the front but behind it is cardboard and duct tape that'll fall over with the slightest change. A product has to hold up over time, not just in a demo. Strong internals — smart structure, readable code, a modular build that adapts — project forward well. A stage prop doesn't.

## Reading Early Stress Signals

Structural problems rarely announce themselves clearly. They show up early as small signals: a minor bug that took longer than expected to trace, a component that's harder to extend than it should be, a surprising loading delay, an area of code that feels muddled when you return to it. Individually, each is minor. Together they point to a weakness before it becomes obvious.

The difficulty is that it's easy to ignore these signals. There's no reward for fixing a problem that doesn't exist yet, and structural work produces almost no visible progress in the short term. But the cost of addressing those signals early is a fraction of what it costs once the problem is established.

My instinct is to treat those signals as priority work disguised as cosmetic upkeep. If the structure is showing early strain, addressing it now is critical work — even though it looks like nothing to someone watching from the outside.

## Two Contrasting Examples

On Nexus I owned the frontend entirely. I kept a close eye on the structure as it evolved and addressed problems when they first appeared — before they grew into actual work items. That meant spending time on things that produced no visible feature progress but that kept the codebase flexible. Features expanded quickly when they came because the structure anticipated them. Nothing broke in ways that required significant rework.

Build at BriefYourMarket — my first employer — showed the other side. It had been built by contractors with no long-term stake, and by the time I was working in it, it was hotfix on hotfix. Touching one area caused failures elsewhere. Nobody held the full map. Meaningful improvement wasn't possible without something close to a rebuild. The work I did there was surgical: smallest possible change, smallest possible footprint. Not making it worse was roughly the best available outcome.

The contrast between them is why I prioritise structural work early. The time investment at the start is modest. The time investment once a codebase is entangled is massive, and even then the return is limited.

## When Stage Props Are Deliberate

Sometimes stage props are the right call. A rapid prototype to test a theory or show a stakeholder what something could look like is legitimate — especially if it's built in a modular way so you can swap internals for something robust later. The problem isn't the prop; the problem is when nobody communicates clearly what it is. Stakeholders often only see the visible layer and mistake "looks finished" for "is finished". If you're building a prototype deliberately, that framing has to be explicit from the start.
