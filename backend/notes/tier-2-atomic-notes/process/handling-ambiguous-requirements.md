# Handling Ambiguous Requirements

## Frame the Limits First

When requirements are unclear, my approach is to **frame the limits first, then find creative solutions** within those constraints.

## The Process

### 1. Understand the Real Problem

Ambiguous requirements often mean the stakeholder knows they have a problem but doesn't know what the solution looks like.

**Ask why, not just what**:
- What problem are you trying to solve?
- What does success look like?
- Who are the users and what do they actually need?
- What have you tried before? What worked and what didn't?

**Example - Integrations Dashboard**: The sales team knew they needed "better access to backend data," but that wasn't a clear requirement. Through conversations, I learned they needed to quickly look up customer information, check integration status, and troubleshoot common issues - all without understanding the backend database structure.

### 2. Define the Constraints

What's actually fixed and what's flexible?

**Technical constraints**:
- What systems can't be changed?
- What's the performance requirement?
- What's the budget (time, money, infrastructure)?

**Business constraints**:
- Who needs this and when?
- What's the minimum viable solution?
- What can be added later vs. what's essential now?

**"When resources are scarce, you have to turn to cleverness and creativity"**: Often ambiguity comes from competing priorities or limited resources. Naming these constraints explicitly helps find elegant solutions.

### 3. Create Clarity Through Prototypes

**Show, don't just discuss**: Often stakeholders can't articulate requirements until they see something concrete. Build quick prototypes or mockups to make the abstract concrete.

**Iterate fast**: On moh-ami, the UI/UX went through rapid iteration because legal assistance requirements were complex. Each iteration clarified what users actually needed vs. what we thought they needed.

**Gather real feedback**: Like building the Integrations Dashboard, I talked at length with both backend and sales teams as I worked. Real feedback revealed what was valuable and what wasn't.

### 4. Focus on First Principles

**What are we really trying to accomplish?**: Strip away assumptions and get to the core goal.

**Example - WhatNow**: The ambiguous requirement was "recommend activities to users." But why? The real goal was helping people discover new experiences they'd enjoy. This clarity led to contextual bandits (learning from user responses) rather than just collaborative filtering.

### 5. Propose Options with Tradeoffs

Don't wait for perfect requirements. Propose solutions with clear tradeoffs:

**"We could build X which does A, B, C and takes 2 weeks, or Y which does A, B and takes 1 week. Here's what we'd gain and lose with each."**

This gives stakeholders something concrete to evaluate and often clarifies what they actually care about most.

## Examples

### Nexus Dashboard Foundation Blocks

The requirement was vague: "Create a scalable architecture for dashboard building." Through discussion and framing constraints, we established:
- Need to support multiple dashboard types
- Developers should be able to create new dashboards quickly
- Need safety layers to prevent breaking existing dashboards
- Must be performant even with complex visualizations

This clarity led to the foundation blocks architecture where developers compose dashboards from tested, reusable components.

### Atlantis Hardware Pivot

Early requirements for Atlantis were exploratory: "Build an underwater drone." Through framing constraints (budget, environment, mission profile) and understanding the real goal (lake bed mapping), requirements clarified into specific hardware and software needs.

When initial hardware choices didn't fit constraints, we pivoted based on what we learned. Ambiguity became clarity through iterative testing and honest assessment.

## Handling Resistance to Clarity

Sometimes stakeholders resist defining requirements because they don't want to commit or limit options.

**My approach**:
- Explain that ambiguity is expensive (wasted work, missed targets)
- Start with what we CAN define, even if some things remain unclear
- Build in phases so we can adjust as we learn
- Make ambiguity explicit: "We're assuming X. If that assumption is wrong, we'll need to adjust."

## Communication Strategies

**Active listening**: Focus on understanding their perspective before presenting mine. Often the real requirement is underneath what they first say.

**Translate between domains**: Like bridging backend and sales teams, translate business needs into technical requirements and technical constraints into business implications.

**Visual aids**: Diagrams, mockups, and flowcharts make ambiguous concepts concrete and discussable.

## Knowing When to Proceed

You can't always eliminate all ambiguity before starting. Sometimes you need to start building to learn what you don't know.

**Proceed when**:
- Core goals are clear even if details aren't
- Constraints are defined well enough to make meaningful progress
- Stakeholders understand we may need to adjust as we learn
- Early work provides value even if later work changes direction

**Wait when**:
- Fundamental decisions (tech stack, architecture) depend on unclear requirements
- Stakeholders have contradictory goals they haven't reconciled
- No one can define what success looks like

## The Goal

Turn ambiguity into clarity through strategic questioning, rapid prototyping, and iterative feedback. Frame the limits, focus on real problems, and propose concrete solutions with clear tradeoffs.

The Integrations Dashboard succeeded because I didn't wait for perfect requirements - I clarified through collaboration and iteration. That's how you handle ambiguity: make it explicit, test assumptions, and learn by doing.

