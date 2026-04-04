# BriefYourMarket — Junior Developer and the Build System

## The Role

My first professional development role was as a Junior Web Developer at BriefYourMarket.com, from October 2020 to February 2021 (5 months). BriefYourMarket was a marketing platform for estate agents — the company I later rejoined as Nurtur in 2022.

Joining as a junior, I was working in a production codebase for the first time. The main codebase was a mature system with real users and real consequences for breaking things.

## The Build System

My first significant task was debugging a system called Build. Build was a core piece of architecture — critical to the company's operation — that had been assembled by contractors years earlier.

The contractors had no long-term stake in the code. Their incentive was to deliver features quickly, not to leave something maintainable. Over time, as requirements changed and bugs appeared, the response was always the same: hotfix. A change here, a patch there. Then a hotfix on top of a hotfix. Over years, this layered until the system had become almost organic in its complexity — no single person fully understood it, everything was entangled with everything else, and touching any part of it tended to cause cascading bugs somewhere else.

By the time I worked on it, Build was in a state where no one wanted to go near it. It was confusing, unstable, and critical — the worst possible combination.

## What I Did

My job was not to refactor Build. It was to debug it: find the source of a specific bug, investigate it deeply, and make the most surgical change possible — the minimum intervention that fixed the problem without touching anything else. Any change that disturbed the surrounding code risked triggering something else entirely.

That constraint — make the smallest possible change — was a masterclass in understanding how tightly coupled code behaves. It forced me to understand the system deeply before touching it, to trace cause and effect through layers of accumulated decisions, and to be precise.

## What It Taught Me

Working on Build shaped how I think about code structure more than any other single experience.

The problems in Build weren't the result of bad developers. They were the result of good enough decisions made without consideration for the future — decisions that calcified over time into something immovable. The structural problems weren't fixable with hotfixes; they were the hotfixes.

What I took from it:
- Structure is what makes code safe to change. When modules are self-contained and well-defined, fixing one thing doesn't break ten others.
- Structural debt calcifies. Clutter can be cleaned up later. Bad architecture can't be — it shapes every decision made after it.
- The right fix to a system like Build is a rewrite, not a refactor. The structure itself was forcing the wrong direction.

This experience is directly why I care so much about architecture from the start, why I think about how code will behave and change years into the future, and why the Integrations Dashboard has run 3+ years without a single maintenance call. I knew what the alternative looked like.

## Connection to Nurtur

BriefYourMarket later rebranded as Nurtur. When I rejoined in July 2022 as a Full Stack Developer, I was working for the same underlying company in a more senior role. My junior role at BriefYourMarket gave me familiarity with the codebase and context that informed how I approached new projects — particularly the emphasis on getting structure right from the start.
