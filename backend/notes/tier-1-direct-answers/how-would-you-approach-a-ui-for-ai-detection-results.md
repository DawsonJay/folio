# How would you approach building a UI that displays AI detection results?

The first question is who the UI is for. If the goal is giving users insight into the model's reasoning, I'd have the source image with bounding boxes overlaid on one side, and on the other a breakdown: object classes with confidence scores, and the final determination separated with its own confidence. The aim is making the model's reasoning legible without overwhelming the user.

Before designing anything I'd want to know the real-world performance picture, not just validation numbers. My closest experience is Jam Hot — a computer vision project that hit 86% validation accuracy then dropped to 0% accuracy when pointed at actual photos. That gap taught me something critical for UI: if the model's real-world failure modes aren't surfaced honestly, users have no way to compensate. An interface showing "detected: apple, 91% confidence" when the model is unreliable on real images does more damage than one that says "low confidence — try better lighting."

For edge cases: multiple overlapping detections get layered in different colours on the source image so the conflict is visible. Low confidence at the final stage gets flagged explicitly. Complete misses still show the logic steps taken — the worst UX is when something has clearly gone wrong with no explanation of why.

---

**shortTitle:** How would you build an AI detection UI?
**emotion:** thinking
**suggestions:**
- What do you ask before building an AI UI?
- What AI/ML experience do you have?
- How do you handle unexpected AI output?
- Where does UI add value on top of AI?
- How do you show AI uncertainty in a UI?
- What does good AI integration look like?

**variants:**
- How would you design a UI to show object detection results?
- How would you display AI model output to a user?
- How do you think about building interfaces for AI systems?
