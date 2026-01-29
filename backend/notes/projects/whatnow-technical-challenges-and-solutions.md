# WhatNow: Technical Challenges and Solutions

Building WhatNow involved solving numerous technical challenges across machine learning, full-stack development, and production deployment. The solutions I developed demonstrate problem-solving abilities, technical depth, and the practical engineering skills needed to take projects from concept to working systems.

**Challenge: Balancing Learning Speed with Robustness**

The core AI challenge was needing recommendations that adapt quickly to current context while remaining stable over time. Too fast and the system becomes chaotic, over-responding to outliers. Too slow and it feels unresponsive, not adapting to my current mood.

Solution: The two-layer learning architecture with Session AI (rate=0.8, resets each session) for immediate adaptation and Base AI (rate=0.02, persists forever) for long-term stability. This provides both responsiveness and robustness without compromising either.

**Challenge: Data Acquisition for Training**

Traditional ML projects require massive pre-existing datasets, which for personal projects often means relying on inadequate public datasets. This killed my previous CV projects (Jam Hot, Cirrus).

Solution: Build a system that generates its own training data through usage. Every interaction provides labeled examples, eliminating the dataset acquisition problem entirely. The system is useful from day one and improves continuously through real usage.

**Challenge: Representing Activities Meaningfully**

Hand-coding metadata for 1,249 activities across 15+ dimensions was time-consuming, subjective, and incomplete. No matter how many dimensions I added, I couldn't capture nuanced similarities between activities.

Solution: Semantic embeddings using sentence transformers. Each activity description becomes a 384-dimensional vector that automatically captures semantic relationships. Similar activities cluster together without manual categorization, and the representation is more expressive than hand-coded features.

**Challenge: Frontend Responsiveness for Learning**

If Session AI learning required API calls to the backend after each selection, the latency would hurt user experience. Waiting 200-500ms for API responses between each interaction makes the interface feel sluggish.

Solution: Implement Session AI entirely in the frontend JavaScript. The contextual bandit logic runs client-side, updating weights immediately after selections with zero latency. Only Base AI updates require backend communication, and those happen after session completion when latency doesn't impact interaction flow.

**Challenge: Deployment Constraints**

Initial implementation used scikit-learn and TensorFlow, but deploying those heavy libraries to free-tier hosting was problematic. Build times were long, cold starts were slow, and memory constraints were tight.

Solution: Custom lightweight implementations of the contextual bandit logic in Python and JavaScript. No heavy ML libraries needed - just numpy on the backend and plain JavaScript math on the frontend. This reduced deployment complexity, improved cold start times, and made the code easier to understand and modify.

**Challenge: Cold Start Problem**

How do you make reasonable recommendations before the AI has learned anything about the user? Random suggestions would feel useless and might discourage continued use.

Solution: Initialize with sensible priors based on general activity characteristics. High-energy activities start with small positive weights for high-energy contexts, social activities associate with social contexts, etc. This makes first-session recommendations reasonable while the AI learns actual preferences through usage.

**Challenge: Database Migration Between Platforms**

Moving from Railway to Render required migrating the PostgreSQL database without losing user data, preference histories, or Base AI model weights accumulated through real usage.

Solution: Careful migration procedure with database dump, import to new instance, integrity verification, and thorough testing before switching. Having clear rollback plans meant executing the migration confidently. Using environment variables for configuration made switching database connections manageable.

**Challenge: Maintaining State Across Multiple Interaction Cycles**

Users generate activities, mark favorites, regenerate for more options, accumulate favorites from multiple generations, and finally make a selection. Managing this complex state flow cleanly was tricky with vanilla JavaScript.

Solution: React + Redux Toolkit for centralized state management. State slices for sessionState, activities, and learning made the flow clear and maintainable. Components could focus on rendering and user interaction while Redux handled state coordination.

**Challenge: TypeScript Equivalence Between Python and JavaScript**

Session AI logic needed to work identically in Python (for testing and Base AI) and JavaScript (for frontend Session AI). Implementation differences could cause divergence in behavior.

Solution: Careful translation of the contextual bandit math from Python to JavaScript, with verification that both implementations produce identical results for the same inputs. Unit tests in both languages confirm mathematical equivalence. The clean separation of learning logic from framework code made this testable.

**Challenge: Activity Feature Engineering**

The contextual bandit needs features that combine context (mood, energy, etc.) and activity characteristics in ways that predict my preferences. Poor feature design means the AI can't learn effectively.

Solution: Iterative experimentation with feature representations. Started with simple concatenation, tried polynomial features for interactions, settled on combinations that actually predict my choices. The flexibility of embeddings meant the AI could discover useful patterns rather than relying solely on my feature engineering.

Each of these challenges represents a point where the project could have stalled or failed if I couldn't find workable solutions. The fact that WhatNow is deployed and functional means I successfully navigated all these technical obstacles. But more importantly, I did it in ways that are maintainable, understandable, and adaptable to future changes.

For employers, these challenge-solution pairs demonstrate that I don't just copy tutorial code - I face real technical problems and develop pragmatic solutions. I think about tradeoffs, make engineering decisions based on actual constraints, and build systems that work reliably in production. That problem-solving ability across the full stack (ML algorithms, backend APIs, frontend UI, deployment infrastructure) is what enables taking projects from idea to shipped product.

