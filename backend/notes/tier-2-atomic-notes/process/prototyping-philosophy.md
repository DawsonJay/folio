# Prototyping vs Production-Ready Work: Stage Props and Communication

A prototype has a purpose: testing a theory, showing a stakeholder what something could look like, exploring a direction without committing to full implementation. That's legitimate and sometimes exactly right. The problem isn't building prototypes — it's when stakeholders see a polished surface and assume it's finished.

I think of it like a stage prop. It looks real from the front. Behind it is cardboard and duct tape. Stakeholders can't see the internals. If you've built something exploratory, being explicit upfront — "this is a prototype to validate the idea, not production-ready software" — is what makes the pattern work without creating debt everyone's surprised by later.

When I do build something disposable, I build it modular where possible — so you can swap out internals and replace them with something robust later rather than discarding everything. This pattern works, but it's harder to pull off than building it right from the start, and it only holds up if both sides are clear on what's being built.

The instinct I work against is building the stage prop permanently. Solid internals and a quickly iterable visible layer aren't mutually exclusive. On Nexus I laid the right structural foundation early — adaptable components, a sensible API call system — while still being able to iterate quickly on the visible dashboard. The foundation paid dividends from the first time the backend changed. That's the ideal: prototype speed with structural discipline underneath.

The critical thing is communication. Stakeholders tend to evaluate based on what they can see. If the visible layer looks complete, they often conclude the product is complete. Managing that expectation explicitly — "this explores the idea; the internals will need proper engineering before it's production-ready" — is as important as the technical work.
