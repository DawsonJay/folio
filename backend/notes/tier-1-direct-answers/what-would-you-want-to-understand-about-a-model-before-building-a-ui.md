# What would you want to understand about a model before building a UI for it?

Before designing an interface around a model I want to understand its limitations, its strengths, what it's for in the product, and what value it's supposed to deliver. Those four things shape almost every design decision.

The less obvious question I'd ask is about real-world vs validation performance — not just what the model achieves in tests but how it actually behaves on realistic inputs. Jam Hot, a computer vision project I built, hit 86% validation accuracy but dropped to 0% in real-world use. If I'd designed the interface against only the validation story, I'd have built something that confidently surfaced wrong results.

One thing that caught me off guard early on was how often AI models operate as black boxes. With conventional software you can usually explain the mechanics to users. With many neural approaches or complex RAG pipelines there's no clean step-by-step story to surface. On Folio I handle this by having the UI reflect the best way to use the AI — suggestion chips hint at the question formats it handles well — rather than trying to expose mechanics that aren't meaningful at the user level. Knowing this upfront changes how you design the whole interface.

---

**shortTitle:** What do you ask before building an AI UI?
**emotion:** thinking
**suggestions:**
- How would you build an AI detection UI?
- What AI/ML experience do you have?
- How do you handle unexpected AI output?
- How do you show AI uncertainty in a UI?
- What does good AI integration look like?
- What is Folio?

**variants:**
- What questions do you ask the ML team before building a UI?
- What do you need to know about a model before you can design around it?
- What would you want to understand about an AI system before building its interface?
