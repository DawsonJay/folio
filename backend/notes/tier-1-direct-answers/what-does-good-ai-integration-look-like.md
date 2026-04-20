# What does good AI integration look like?

Good AI integration solves a problem that nothing else solves as well. AI has severe limitations — expensive, non-deterministic, prone to hallucination, difficult to test — and those limitations are acceptable only if the thing you're getting in return isn't achievable any other way.

Folio is a clear example of that boundary drawn correctly. The LLM does one thing: it stitches together structured notes to produce answers that sound human and genuine rather than copy-pasted. That's a task only a language model can do, and it's genuinely invaluable for a chatbot. Everything else in the system is deterministic — retrieval, routing, fallback logic. The AI is contained to exactly the part that requires it.

The opposite failure mode is what I saw being proposed on the Email Editor at Nurtur. Management were excited about an AI feature that would draft emails for users — not because anyone was being obstructive, but because AI was generating huge enthusiasm and it sounded like a quick win. The lead developer's real frustration wasn't fighting management, it was how hard it was to explain to stakeholders that shipping something genuinely useful at that quality bar would require enormous complexity in a core product — and the end result still wouldn't beat what a user could do with ChatGPT in another tab for free. The problem wasn't the intention, it was the gap between expectation and what was actually achievable.

---

**emotion:** thinking
**suggestions:**
- What is Folio?
- What AI/ML experience do you have?
- How do you approach adding AI features?
- Tell me about the Email Editor project
- Do you have experience with LLMs?
- How do you approach AI project scoping?

**variants:**
- What makes AI integration feel native in a product?
- How do you know when to use AI in a frontend?
- What does well-integrated AI look like versus bolted-on AI?
