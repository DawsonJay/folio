# WhatNow: Two-Layer Learning Architecture

The most innovative aspect of WhatNow is its two-layer learning architecture, which solves a fundamental tradeoff in machine learning: you want systems that adapt quickly to new information (good user experience), but you also want systems that are robust and don't overreact to outliers (good AI design). I solved this by implementing two separate AI models that learn at different rates and serve different purposes.

**Session AI** is the fast learner. It starts fresh at the beginning of each session with a learning rate of 0.8, which means it updates its weights dramatically based on each choice I make. If I'm in a low-energy mood and keep selecting quiet, restful activities, Session AI picks up on that pattern immediately and starts heavily favoring similar activities. This provides instant responsiveness - within 2-3 selections, the recommendations feel tailored to my current state.

**Base AI** is the slow learner. It persists across all sessions and learns with a rate of 0.02, meaning it takes many, many examples before significantly changing its model. Base AI is building a long-term understanding of my general preferences - the kinds of activities I tend to enjoy regardless of current mood, the categories I consistently avoid, the features that matter most to me. One bad session where I'm cranky and reject everything doesn't meaningfully affect Base AI's understanding.

The system combines both models for each recommendation. Base AI provides the foundation - "based on everything I know about you over months, these activities generally match your preferences." Session AI adds refinement - "but right now, based on your current mood and recent selections, here's how we should adjust those recommendations." The mathematical combination weights both models' predictions to generate the final activity scores.

Why does this two-layer approach work so well? Consider what happens in different scenarios:

If I'm in a familiar mood state, Session AI quickly converges toward activities that match that mood, while Base AI confirms those are generally good choices for me. Both models agree, so recommendations feel very confident and accurate.

If I'm in an unusual mood state, Session AI picks up the new pattern and pushes toward activities that match my current feeling, while Base AI provides stability by still knowing my general preferences. I get recommendations that feel responsive to my current state but aren't completely divorced from what I normally enjoy.

If I have one weird session - maybe I'm sick and just want to sleep, or I'm selecting random things because I'm distracted - Session AI will reflect that session, but Base AI remains unaffected. Next session, when Session AI resets to neutral, Base AI ensures the recommendations still reflect my actual long-term preferences.

This architecture emerged from thinking carefully about the user experience failure modes. Pure fast learning (only Session AI) would be super responsive but also chaotic - one bad session ruins the model. Pure slow learning (only Base AI) would be stable but frustratingly unresponsive - it wouldn't adapt to my current mood quickly enough to feel useful. The two-layer approach gives me both immediate responsiveness and long-term stability.

The implementation is interesting because Session AI runs entirely in the browser JavaScript (no API calls needed for within-session learning), while Base AI learning happens on the backend after session completion. This keeps the frontend responsive while ensuring the long-term model updates are persisted properly to the database.

From a machine learning perspective, this is inspired by but distinct from techniques like transfer learning or ensemble methods. It's closer to multi-timescale learning in neuroscience, where biological systems have both fast-adapting and slow-adapting mechanisms for different aspects of learning. I didn't copy this from a textbook - it emerged from thinking about what would actually provide good UX while remaining robust.

What I'm particularly proud of is that this wasn't the first design. I tried single-model approaches first, experienced the problems firsthand (too rigid or too chaotic), and iterated toward this solution. The two-layer architecture represents learning from failure and building something that actually works well in practice, not just in theory.

For employers, this demonstrates several important capabilities: I can design novel ML architectures to solve specific problems, I understand the tradeoffs in learning systems and can balance them intentionally, I think about user experience implications of AI decisions, and I iterate based on real-world performance rather than sticking with initial designs that don't work. The two-layer architecture isn't just technically interesting - it's the reason WhatNow is actually useful to me rather than a toy I tried once and abandoned.

