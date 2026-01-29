# The Hardest Bug I've Fixed: WhatNow's Invisible Recommendation Bias

## The Problem

The hardest bug I've fixed wasn't a crash or error message - it was **invisible bias in WhatNow's recommendation algorithm** that I had to discover, prove, and fix without any obvious symptoms.

## Context

WhatNow used a two-layer learning architecture: embeddings for semantic similarity + contextual bandits for personalization. The system was working, recommendations seemed reasonable, but something felt off.

## How I Noticed Something Was Wrong

**Intuition first**: User feedback suggested recommendations felt "samey" - not obviously wrong, just not as diverse as they should be. Metrics didn't show a problem (click-through rates were acceptable), but the qualitative feedback nagged at me.

**This is where my artistic background's intuition matters**: I could feel something was structurally weak even without data proving it.

## The Investigation

### 1. Initial Hypothesis: Training Data Imbalance
Checked activity distribution in the database. Some categories were more represented than others, which could bias recommendations. But correcting for this didn't fix the feeling of "samey" recommendations.

### 2. Second Hypothesis: Embedding Clustering
Maybe embeddings were clustering too tightly, making everything seem similar. Visualized the embedding space using dimensionality reduction (t-SNE). Found clusters, but they made sense semantically - not a problem.

### 3. The Breakthrough: Contextual Bandit Exploration Rate
Spent a week debugging before I realized: **the contextual bandit's exploration parameter was too low.**

**What this meant**: 
- Contextual bandits balance exploration (trying new things) vs. exploitation (doubling down on what works)
- My epsilon value (exploration rate) was 0.05 (5% exploration)
- This meant 95% of the time, the algorithm showed "safe" recommendations
- Safe recommendations performed acceptably, so metrics didn't flag it
- But users weren't discovering genuinely new experiences

## Why This Was Hard

### 1. No Error Message
The system worked exactly as coded. No crashes, no exceptions, no warnings. The bug was in my design choices, not my implementation.

### 2. Metrics Didn't Show It
Click-through rates and engagement were acceptable. Traditional A/B testing wouldn't catch this because both versions would perform "fine."

### 3. Subjective Feedback
Users couldn't articulate what was wrong. They just felt recommendations were "okay but not exciting." That's hard to debug.

### 4. Required Deep Understanding
To fix this, I needed to understand:
- How contextual bandits actually learn
- The exploration-exploitation trade-off
- Why low exploration creates invisible problems
- How to measure diversity, not just performance

### 5. Validation Was Difficult
How do you prove recommendations are "more diverse" and that matters? I had to:
- Define diversity metrics (category distribution, semantic distance between recommendations)
- Run longer-term tests (diversity benefits emerge over time, not immediately)
- Gather qualitative feedback systematically

## The Fix

Changed epsilon from 0.05 to 0.15 (5% → 15% exploration).

**But it wasn't that simple**:
- Also implemented adaptive exploration (higher epsilon for new users, lower for established preferences)
- Added diversity penalty to exploitation choices (don't show semantically identical activities)
- Created monitoring dashboard to track diversity metrics alongside performance metrics
- Added mechanism for users to explicitly request "something different"

## The Results

**Quantitative**:
- Category diversity increased by 40%
- Average semantic distance between recommendations increased by 25%
- Long-term engagement improved (users came back more)
- Short-term click-through dropped slightly (expected - exploring means some misses)

**Qualitative**:
- Users reported feeling like they were "discovering" things
- Feedback shifted from "okay" to "exciting"
- More stories of trying activities they wouldn't have chosen themselves

## What Made This My Hardest Bug

### Not Traditional Debugging
No stack traces, no error logs, no obvious failures. Had to rely on:
- Intuition that something was off
- Deep understanding of the algorithm
- Systematic investigation of multiple hypotheses
- Creating metrics to prove the problem existed

### Domain Knowledge Required
Needed to understand:
- Machine learning (contextual bandits)
- User psychology (what makes recommendations feel good)
- Product thinking (short-term metrics vs. long-term experience)
- Statistics (how to measure and validate improvement)

### High Stakes
WhatNow's entire value proposition was recommendations. If they weren't good, the project failed. No pressure.

### Self-Inflicted
I wrote the original code. Fixing this meant admitting my initial epsilon choice was wrong and understanding why I made that mistake.

## What I Learned

### 1. Trust Your Intuition, Then Prove It
My gut feeling that something was off drove the investigation. But I didn't act until I could prove and measure the problem.

### 2. Metrics Can Lie By Omission
Everything I was measuring said "fine." The problem was I wasn't measuring the right things (diversity, novelty, long-term engagement).

### 3. Sometimes The Bug Is The Design
The code worked perfectly. The algorithm was implemented correctly. The bug was in my design choices about how the algorithm should behave.

### 4. User Feedback Matters
Quantitative metrics matter, but qualitative feedback - even vague feedback like "it's okay but..." - can point to real problems.

### 5. Deep Understanding Beats Trial and Error
I could have randomly tweaked parameters until things improved. Instead, I investigated until I understood the root cause, then made informed changes.

## Why This Story Matters

**For technical interviews**: This demonstrates:
- Deep understanding of algorithms, not just implementation
- Ability to debug subtle, non-obvious problems
- Data-driven decision making
- Product thinking (user experience matters)
- Self-awareness (admitting and fixing my own design mistakes)

**For real work**: Most hard bugs aren't dramatic crashes. They're subtle issues where the system works but doesn't work well. Finding and fixing these requires intuition, deep understanding, and systematic investigation.

This was harder than any stack overflow or memory leak I've debugged because it required seeing what wasn't there: the recommendations users never got to experience.

