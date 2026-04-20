# Prototyping Philosophy: Stage Props, When They Work, and When They Don't

## Stage Props Are a Legitimate Tool

A prototype has a purpose: testing a theory, showing a stakeholder what something could look like, exploring a direction quickly without committing to full implementation. That's legitimate and sometimes exactly what a project needs. Companies that want to iterate rapidly or validate ideas before investing often need this pattern.

The key is to be clear — to yourself and to everyone else — about what you're building.

## The Stage Prop Problem

A stage prop looks real from the front. Behind it is cardboard and duct tape. The problem isn't building the prop; it's when stakeholders see a polished surface and assume it's finished. They can't see the internals. If you've built something exploratory, being explicit upfront — "this is a prototype to validate the idea, not production-ready software" — is what makes the pattern work without creating debt everyone's surprised by later.

Too often, companies mistake speed-of-visible-progress for real progress. A rapid prototype thrown up in a week looks more complete than a week of solid architectural foundation work. The foundation week produces almost nothing visible. The prototype week produces something that looks like a product. Stakeholders who only see the surface don't always understand why the foundation week was more valuable.

## Building Prototypes That Can Grow

When I build something disposable I build it modular where I can. The goal is to be able to swap out internals and replace them with something robust later rather than discarding everything. If a prototype is structured so each part is reasonably isolated, you can replace the cardboard-and-duct-tape internals piece by piece with something solid.

This pattern works — it's just harder to pull off than building it right from the start, and it only holds up if both sides understand what's being built. Modular prototypes that grow into real products need clear communication about what's been replaced and what hasn't.

## The Better Path Where Possible

The instinct I work against is building the stage prop permanently. Solid internals and a quick visible layer aren't mutually exclusive. Often you can lay the right structural foundation early — which costs relatively little if done at the start — and still iterate quickly on the visible layer above it.

The Nexus Dashboard is an example of this done well. The backend situation was uncertain and might change a lot. Rather than building a fragile UI tightly coupled to specific backend assumptions, I prioritised adaptability early: modular components, a system for handling API calls that could be updated without rewriting everything around it. The visible layer was still iterable. But the foundation didn't need to be thrown away when things changed.

That's the ideal: prototype speed with structural discipline. The foundation pays dividends from the moment something changes — which, in active development, is always.
