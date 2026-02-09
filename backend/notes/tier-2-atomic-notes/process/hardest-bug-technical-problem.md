# Hardest Bug and Technical Problem

## The WhatNow Dataset Problem

The hardest technical problem I've solved wasn't a single bug - it was the fundamental challenge of building a recommendation system without the data recommendation systems require.

## The Problem

**WhatNow needed collaborative filtering recommendations**, which traditionally require millions of user interactions. I didn't have:
- Existing users
- Historical interaction data
- Resources to collect that data over months/years
- Time to wait for enough data to train models

This was a **cold-start problem at system level**, not just new-user level. Most recommendation systems assume you already have data. I had to build something that worked from day one.

## Why This Was Hard

**Circular dependency**: To attract users, I needed good recommendations. To have good recommendations, I needed user data. To get user data, I needed users.

**Technical complexity**: Recommendation systems are genuinely hard. They involve:
- Understanding user preferences
- Predicting what someone will enjoy
- Learning from implicit feedback (views, time spent) not just explicit ratings
- Balancing exploration (showing new things) with exploitation (showing known good things)

**No obvious solution**: This wasn't a bug where the problem is finding what's broken. This was architectural - the traditional approach fundamentally didn't fit my constraints.

## The Solution Evolution

### Attempt 1: Manual Metadata

Initially tried manually tagging activities with metadata (categories, difficulty, indoor/outdoor) and matching based on past selections.

**Why it failed**: Manual metadata is subjective, incomplete, and doesn't capture what makes one kayaking trip different from another. Users didn't just want "outdoor activities" - they wanted experiences that matched their specific vibe.

### Attempt 2: Embeddings

Switched to generating embeddings from activity descriptions using OpenAI's models. This captured semantic similarity far better than manual tags.

**Improvement**: Now recommendations could find "similar vibes" even across different activity types. A poetry reading and intimate concert might be semantically similar even though they're different categories.

**Limitation**: Still wasn't learning from user behavior. Static similarity without adaptation to individual preferences.

### Attempt 3: Contextual Bandits (The Solution)

Built a two-layer learning architecture:
1. **Content layer**: Embeddings for semantic similarity
2. **Learning layer**: Contextual bandits that learn from user responses

**Why this worked**:
- Starts with reasonable recommendations (embeddings) on day one
- Learns from each user interaction (clicks, time spent, explicit feedback)
- Balances exploration (trying new things) with exploitation (doubling down on what works)
- Adapts to individual users without needing millions of historical interactions
- Gets better over time automatically

## The Debugging Process

**Frame the limits**:
- Can't wait months for data
- Can't force users to rate everything explicitly
- Need recommendations that work immediately but improve over time
- Need to work with small datasets and cold starts

**Creative solution within constraints**: "When resources are scarce, you have to turn to cleverness and creativity." Contextual bandits were the clever solution - they're designed exactly for this scenario (learning with limited data in real-time).

**Iterate through versions**: I didn't solve this in one step. Each attempt taught me something:
- Manual metadata: taught me metadata alone isn't enough
- Embeddings: taught me semantic similarity works but isn't dynamic
- Contextual bandits: combined both insights into adaptive system

## What Made It Hard

**No clear path**: Traditional recommendation systems have well-trodden paths. My constraints made those paths unavailable, forcing novel approaches.

**Multiple disciplines**: This required understanding:
- Machine learning (contextual bandits, embeddings)
- User experience (what makes good recommendations)
- System architecture (how to structure learning layers)
- Data engineering (how to capture and use feedback)

**Self-teaching**: I had to teach myself contextual bandits specifically for this project. No one at Nurtur or in my network had experience with them.

**High stakes**: WhatNow's core value proposition was recommendations. If they didn't work, the entire project failed.

## What I Learned

**Innovation and practicality can be the same thing**: The contextual bandit solution wasn't just novel - it was the practical answer to my constraints.

**Intuition + research**: My intuition told me embeddings alone weren't enough. Research led me to contextual bandits as the solution.

**Frame problems correctly**: Initially I saw this as "I need more data." Reframing it as "I need recommendations that work with minimal data" opened up different solutions.

**Iterate boldly**: Each version was substantially different. I wasn't afraid to throw away approaches that didn't work and try something fundamentally different.

## The Result

WhatNow's two-layer learning architecture:
- Works from day one with zero historical data
- Gets better with each user interaction
- Balances exploration and exploitation automatically
- Scales to new users and activities gracefully
- Demonstrates strong AI/ML understanding beyond basic implementations

This problem taught me that the hardest technical challenges aren't usually bugs - they're architectural problems that require creative solutions within real-world constraints. That's where the interesting work lives.

