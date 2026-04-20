# What happens in your interface when the model returns an unexpected result?

Folio is a good example because it has to handle any question and it's a professional showcase — getting things wrong would be worse than not answering. The design is built in three layers.

First, for the most common questions I prepare scripted answers. If a question matches closely enough, the LLM is bypassed entirely — scripted answers are cheaper, faster, and far easier to test and improve. Second, if no scripted answer matches, the system finds notes from a pool of atomic records about my experience and sends the closest ones with the prompt. The LLM stitches them into a natural-sounding answer from vetted material rather than inventing facts. Third, if nothing matches well enough, Folio returns a clear message: not enough material to answer this, try a different question. I'd rather acknowledge a gap honestly than serve a confident wrong answer.

Suggestion chips sit across all three layers — pre-written questions Folio has strong coverage for — so users who hit a gap have a clear path to useful territory rather than a dead end.

The right recovery from an AI failure is always a clear next step for the user, not just an error message.

---

**shortTitle:** How do you handle unexpected AI output?
**emotion:** thinking
**suggestions:**
- How do you show AI uncertainty in a UI?
- Where does UI add value on top of AI?
- What do you ask before building an AI UI?
- What is Folio?
- What does good AI integration look like?
- How do you approach adding AI features?

**variants:**
- What defensive design have you built into AI-facing interfaces?
- What do you do when an AI model returns something unexpected?
- How do you handle AI failures in a user interface?
