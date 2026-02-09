# How do you approach problem-solving?

My problem-solving approach combines artistic intuition with rigorous logical investigation. My artistic background gives me intuition about code structure - a gut feeling about where problems lie. This intuition acts as a compass, not as proof. I follow intuition with rigorous logical investigation.

I approach problems by framing limits first, then finding creative solutions within those constraints. What do we actually know? What's the actual error or unexpected behavior? What are the constraints (performance, resources, time)? What can't be changed (external APIs, database schema, existing systems)? What's the scope of impact? Define success: What does "solved" look like? Sometimes the real problem isn't what it first appears to be.

My gut often points me to the right area of code or the right system boundary. On the WhatNow project, I could sense when the recommendation algorithm wasn't quite right, even before metrics confirmed it. Pattern recognition helps too - from projects like the Integrations Dashboard, Nexus, and moh-ami, I've seen many categories of problems. Often a new bug matches a pattern I've seen before, and intuition catches that similarity.

I gather evidence: logs, error messages, reproduction steps, affected users, timing of when it started. I isolate variables: Is it the frontend or backend? Is it data or code? Is it all users or specific conditions? Narrow down systematically. I form hypotheses based on evidence and intuition, ranking them by probability and ease of testing. Then I test methodically: verify each hypothesis. When one is confirmed, test the fix thoroughly before considering it solved.

I don't just patch symptoms. If the bug is a symptom of deeper architectural problems, the fix might need to be more substantial. I learn for next time: What caused this? How can we prevent similar issues? Should our architecture or testing change?

When debugging is hard, I take breaks. Sometimes hiking or stepping away lets my subconscious process the problem. I've solved many bugs while not actively working on them. I challenge assumptions: The hardest bugs hide in things we assume are working. Question everything. If all else fails, I start from first principles: What is this code supposed to do? Does it do that? If not, why not?

The goal isn't just to fix bugs - it's to understand systems deeply enough that problems become rare. The Integrations Dashboard working for 3+ years without maintenance proves that thoughtful development prevents most bugs before they happen.

My debugging process is about combining intuition (where to look), strategic thinking (how to approach it), and rigorous investigation (proving what's actually wrong). This combination of artistic intuition and logical rigor is what makes my problem-solving effective.

---

**emotion:** thinking
**suggestions:**
- Tell me about debugging a complex issue
- How do you handle failure?
- What challenges have you faced?
- How do you ensure code quality?
- Tell me about a mistake you made
- How do you approach learning new technologies?

