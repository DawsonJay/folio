# Debugging and Problem-Solving Process

## Intuition as Compass, Logic as Proof

My artistic background gives me intuition about code structure - a gut feeling about where problems lie. This intuition acts as a compass, not as proof. I follow intuition with rigorous logical investigation.

## The Process

### 1. Sense the Problem

**Intuitive awareness**: Years of experience mean I can often feel when something is wrong before I can articulate why. The code structure feels weak, the architecture feels unstable, something about the implementation feels off.

**Trust but verify**: I don't act on intuition alone, but I don't ignore it either. If something feels wrong, that's a signal to investigate more carefully.

### 2. Frame the Limits

**Strategic thinking**: I approach problems by framing limits first, then finding creative solutions within those constraints.

**What do we actually know?**:
- What's the actual error or unexpected behavior?
- What are the constraints (performance, resources, time)?
- What can't be changed (external APIs, database schema, existing systems)?
- What's the scope of impact?

**Define success**: What does "solved" look like? Sometimes the real problem isn't what it first appears to be.

### 3. Follow the Intuition

**Where does it feel wrong?**: My gut often points me to the right area of code or the right system boundary. On the WhatNow project, I could sense when the recommendation algorithm wasn't quite right, even before metrics confirmed it.

**Pattern recognition**: From projects like the Integrations Dashboard, Nexus, and moh-ami, I've seen many categories of problems. Often a new bug matches a pattern I've seen before, and intuition catches that similarity.

### 4. Investigate Rigorously

**Gather evidence**: Logs, error messages, reproduction steps, affected users, timing of when it started.

**Isolate variables**: Is it the frontend or backend? Is it data or code? Is it all users or specific conditions? Narrow down systematically.

**Form hypotheses**: Based on evidence and intuition, what are the most likely causes? Rank them by probability and ease of testing.

**Test methodically**: Verify each hypothesis. When one is confirmed, test the fix thoroughly before considering it solved.

### 5. Understand the Root Cause

**Don't just patch symptoms**: If the bug is a symptom of deeper architectural problems, the fix might need to be more substantial.

**Learn for next time**: What caused this? How can we prevent similar issues? Should our architecture or testing change?

## Examples

### Integrations Dashboard

Building the bridge between backend and sales teams required understanding problems from both perspectives. The sales team knew what wasn't working for them, but couldn't articulate it technically. The backend team had technical explanations but didn't understand the user workflow.

**My process**:
- Listened to both teams to understand their perspectives
- Identified that the real problem was mismatch between backend data model and sales workflow
- Framed the constraints (can't change backend schema, need simple UI)
- Created solutions that translated backend complexity into sales-team-friendly interfaces
- Gathered continuous feedback to verify solutions worked in practice

### WhatNow Dataset Problem

I needed collaborative filtering recommendations but had no dataset of user interactions.

**My process**:
- Intuition said manual metadata wouldn't scale or work well
- Framed the constraint: Can't collect millions of interactions, need recommendations now
- Researched solutions for cold-start recommendation problems
- Evolved from manual metadata → embeddings → contextual bandits
- Tested each iteration against actual use cases
- Built two-layer learning architecture to optimize over time

## Tools and Techniques

**Rubber ducking**: Explaining the problem out loud (even to myself) often reveals what I'm missing.

**Simplify and rebuild**: Sometimes the fastest path is stripping code to its simplest form and rebuilding, watching where it breaks.

**Version control archaeology**: Git history often shows when problems were introduced and what changed.

**Team collaboration**: Sharing the problem with teammates brings fresh perspectives. I'm not too proud to ask for help when I'm stuck.

## When Debugging Is Hard

**Take breaks**: Sometimes hiking or stepping away lets my subconscious process the problem. I've solved many bugs while not actively working on them.

**Challenge assumptions**: The hardest bugs hide in things we assume are working. Question everything.

**Start from first principles**: If all else fails, go back to basics. What is this code supposed to do? Does it do that? If not, why not?

## The Goal

The goal isn't just to fix bugs - it's to understand systems deeply enough that problems become rare. The Integrations Dashboard working for 3+ years without maintenance proves that thoughtful development prevents most bugs before they happen.

My debugging process is about combining intuition (where to look), strategic thinking (how to approach it), and rigorous investigation (proving what's actually wrong).

