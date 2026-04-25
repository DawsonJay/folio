# What's your debugging process?

I combine intuition with rigorous logical investigation. My artistic background gives me a gut feeling about where problems lie - this acts as a compass, not proof. I follow intuition with systematic evidence gathering.

My process starts by sensing the problem. Years of experience mean I can often feel when something is wrong before I can articulate why. Then I frame the limits: What do we actually know? What's the error? What are the constraints? I define what "solved" looks like before diving in.

Investigation means gathering evidence - logs, error messages, reproduction steps. I isolate variables: frontend or backend? Data or code? All users or specific conditions? I form hypotheses ranked by probability and test methodically. The goal is understanding root cause, not just patching symptoms. If the bug indicates deeper architectural problems, the fix might need to be more substantial.

On WhatNow's invisible recommendation bias, I spent a week debugging. No error message, metrics looked fine, but users felt recommendations were "samey." My intuition said something was structurally off. Through systematic investigation - checking training data, visualizing embeddings, testing hypotheses - I isolated the contextual bandit's exploration parameter as the culprit.

When stuck, I talk through the problem out loud — explaining it reveals gaps in my own understanding. Git history is useful too: if I can pinpoint when something changed, I already know roughly where to look. If the system is complex, I strip it back to the simplest form that still reproduces the issue, then add pieces back in until it breaks. And sometimes the most effective thing is to step away — hiking or getting out of the building lets the subconscious do work the conscious mind gets in the way of.

---

**emotion:** thinking
**suggestions:**
- Tell me about debugging a complex issue
- What's the hardest technical challenge?
- How do you approach problem-solving?
- Tell me about WhatNow
- How do you tackle complex problems?
- Can you give a problem-solving example?
