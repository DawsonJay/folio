# How do you approach adding a new LLM-powered feature to an existing web application?

The first question I ask is whether it's solving a real problem. A lot of AI features exist because companies want to say they use AI — not because AI was the right tool. moh-ami uses it because it genuinely solves something: learning a language in isolation from context is hard, and an LLM can analyse a real piece of text and explain exactly how specific phrases work, what's idiomatic, what sounds natural versus what a guidebook teaches. That problem doesn't have a simpler solution. AI earns its place there.

Once I'm clear on the problem, I think about structure. The biggest lesson from building Folio was that AI is non-deterministic and prone to hallucination — you can't fully test it the way you test normal code. My solution was to use AI only where it was genuinely needed and build layers around it. Folio handles common questions with scripted direct answers that bypass the model entirely — those are fully testable. The AI only gets called for edge cases, and even then it's working from a set of atomic notes I wrote and can verify. The notes are testable. The AI's job is stitching them together naturally, not inventing facts. That separation keeps the system reliable.

At a company, I'd be asking the same structural questions from the start: where is the AI actually required, where can something simpler do the job, and how do we test what can be tested? AI calls are expensive and the model can lie — the more you can constrain it to a specific, bounded task with controlled inputs, the more robust the feature becomes.

The key is treating AI as a tool with real limitations, not a wonder solution you point at a problem and walk away from.

---

**emotion:** thinking
**suggestions:**
- What is Folio and how does it work?
- Tell me about the moh-ami project
- What's your experience with RAG systems?
- Tell me about your AI/ML experience
- How do you approach system design?
- How do you ensure code quality?
