# How I Approach UI/UX Design

## My Design Philosophy

I don't separate aesthetics from function. Good design looks good because it works well and communicates well. It's like any well-made tool - the beauty is in how well it does its function. This philosophy has guided my work on the Integrations Dashboard, Nexus Dashboard, and moh-ami.

## Process: Intent and Use First

I start by talking to people. I want to find out what the real intent is behind the task, what the data looks like, what people want to use it for. How it will be used should inform the design, not the other way around.

Understanding the actual use case prevents designing interfaces that look good but don't support real workflows. On the Integrations Dashboard, I talked at length with both the backend developers and the sales team to understand what they needed. The sales team knew what wasn't working for them but couldn't articulate it technically. The backend team had technical explanations but didn't understand the user workflow. Getting both perspectives revealed the real problem was mismatch between backend data model and sales workflow.

Then I make sketches and notes on paper. When I'm confident in the design, I make a loose Figma design to show to the team who'll use it and get their opinion. Usually they have useful feedback and I'll go back to paper to improve the design.

Each stage of the process takes more effort and is harder to change, so I try to get a really solid design in the early stages rather than diving straight into code and figuring the design out later. Paper is fast to change. Figma is slower. Code is slowest. Get the design right in paper before committing to implementation.

## Feeling and Communication

A lot of UX design is about feeling. Programmers tend to want to rationalise everything but to make a good experience flow you have to be sensitive to how it impulsively makes you feel. If a design makes you feel even the slightest twist of confusion or annoyance it has to be changed. Users might not consciously notice how it makes them feel, but it'll still influence their experience. As a designer I have to know exactly what impression the site makes.

This is exactly what you do with artwork. You draw or paint to create a feeling or message - it's all communication and you have to build an awareness of what it's communicating on an unconscious level. My art background gives me that sensitivity. Years of creating visual work trained me to notice subtle discomfort or confusion in interfaces. If something feels off, even slightly, it needs adjustment.

## Example: Integrations Dashboard Rebuild

There was an existing dashboard created by a couple of backend developers who were using React for the first time. It broke continuously, was overcrowded and hard to read, and wasn't pleasant or intuitive to use. I rebuilt it from scratch so it conveyed all the same information but in a much more intuitive way that didn't get in the way of user flow.

The original had too much information competing for attention. Every integration's full details were shown simultaneously, creating visual clutter that made it hard to find what you needed. I redesigned it with summary views that showed essential status at a glance, then allowed drilling down into details only when needed. This hierarchical information architecture reduced cognitive load.

The original navigation was unclear - users couldn't tell what was clickable or how to accomplish common tasks. I created clear visual hierarchy with obvious primary actions, consistent interaction patterns, and breadcrumbs showing where you were in the system. Simple things like making buttons look like buttons and organizing information logically made the interface self-explanatory.

I translated backend complexity into sales-team-friendly interfaces. The sales team didn't need to understand database schemas or API endpoints. They needed to see "Is this integration working?" and "How do I fix it if not?" The redesign focused on answering those questions clearly without requiring technical knowledge.

## Example: Nexus Dashboard - Blocks and Rapid Iteration

I chose to represent the graphs and other major components in blocks in a grid. This allowed me to standardise the process of making them and keep a library of graphs that could be rapidly swapped in and out. New graphs could be built in about 10 minutes, new pages in about 30 minutes. This rapid iteration capability was essential because requirements kept evolving as we understood the system better.

The design was incredibly flexible for future changes, which was one of the few concrete things I was told about the job managers - that they would go through major changes in the future. The foundation blocks architecture supported that. When backend data structures changed, I could update the relevant block without touching other parts of the dashboard.

The blocks approach also created consistency. Every graph used the same visual language, same interaction patterns, same loading states. Users didn't have to relearn how to interact with each new visualization. This consistency reduced training time and made the dashboard feel cohesive rather than like a collection of disparate tools.

## Example: moh-ami - Interactive Translation Interface

For moh-ami, I designed a synchronized side-by-side text comparison with interactive features that made learning intuitive. English text on the left, French translation on the right, with both divided into semantic chunks of 50-150 characters for meaningful units.

The hover highlighting creates visual connection between languages. When you hover over an English chunk, the corresponding French chunk highlights. This immediate visual feedback helps learners understand the mapping without clicking or reading instructions.

The expandable explanation panels let users dive deeper when curious. Click a chunk to expand detailed grammar explanations, word-by-word mappings, cultural context, and alternative translations. The collapsed-by-default design keeps the interface clean for quick reference while making deep learning available on demand.

The chunk selection system uses IDs rather than text matching, which handles special characters, punctuation, and LLM paraphrasing reliably. This technical decision made the interactive features robust - something that looks simple to users often requires careful technical implementation to work reliably.

## Tools and Techniques

Paper and pencil for early iteration. Drawing rough layouts and flows helps me think through interaction patterns quickly without committing to implementation details. Paper is infinitely flexible and encourages big changes.

Figma for collaborative design. Once the paper design feels solid, I create a Figma mockup to show stakeholders. Figma bridges paper (too rough) and code (too concrete), letting people give feedback on something that looks real but is still cheap to change.

User feedback loops throughout development. I don't wait until the end to get feedback. I show designs early and often, getting reactions from actual users. When creating the Integrations and Nexus dashboards, I would take designs to the teams that would use them and make adjustments based on their input. Frequent small feedback cycles prevent large project-breaking design failures.

Prototyping in code for complex interactions. Sometimes you can't know if an interaction works until you build it. For moh-ami's synchronized scrolling, I prototyped the interaction early to verify the pattern worked before building the full feature.

Iteration based on real usage. After deployment, I watch how people actually use the interface and adjust based on patterns I observe. The best design insights come from seeing what users struggle with or avoid.

## When Design Is Hard

Competing user needs create tension. On Integrations Dashboard, backend developers wanted technical details while sales team wanted simplicity. I resolved this through progressive disclosure - simple high-level view by default, with drill-down to technical details when needed. Both user groups got what they needed without compromising the other's experience.

Technical constraints limit design options. Performance requirements on Nexus meant I couldn't show all data simultaneously - I had to design around lazy loading and pagination. The blocks architecture made these constraints feel natural rather than limiting. Sometimes constraints lead to better design because they force creative solutions.

Time pressure requires prioritization. When building Folio under tight deadline, I couldn't perfect every interaction. I focused on core user flow first - ask question, get answer, see suggestions. Polish and refinements came after the essential experience worked. The trellis approach: build structure that supports future growth, ship viable version, then iterate.

## Learning from Design

Simple and clear beats clever and complex. The Integrations Dashboard's longevity comes partly from straightforward design that doesn't try to be too clever. Clear labels, obvious actions, minimal abstraction. Users understand it immediately and it doesn't break.

Flexibility requires structure. The Nexus blocks architecture wasn't just about making things swappable - it was about creating structure that enabled flexibility. Paradoxically, having clear rules and patterns makes it easier to adapt to change than having no structure at all.

User feedback is essential, not optional. Both the Integrations Dashboard and Nexus Dashboard succeeded because I gathered continuous feedback from actual users. Designing in isolation creates interfaces that satisfy the designer but frustrate users. Frequent feedback loops catch problems early when they're cheap to fix.

Art background as advantage. Developers who only think logically miss the feeling aspect of interfaces. My art background lets me sense when something feels wrong even if I can't immediately articulate why. That intuition catches subtle UX problems that pure logic misses.

## What This Demonstrates

My UI/UX approach demonstrates: user-first design process starting with real needs, ability to translate complex technical systems into intuitive interfaces, iteration and feedback loops throughout development, artistic intuition combined with technical implementation, and design decisions that support both immediate usability and long-term flexibility.

For mid to senior roles, this shows: cross-functional collaboration capability (technical and non-technical stakeholders), architectural thinking applied to UI (blocks, progressive disclosure, consistency), and understanding that good design requires both feeling and function working together.
