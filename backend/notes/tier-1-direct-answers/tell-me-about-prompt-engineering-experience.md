# Tell me about prompt engineering experience

My most hands-on prompt engineering work has been in moh-ami and Folio.

In moh-ami, the challenge was getting the model to produce consistent, structured JSON outputs: word-by-word translation mappings, grammar explanations, and cultural context — all in a format the application could parse reliably. LLMs are flexible but not predictable by default, so I iterated on the prompt structure until the model understood exactly what schema I needed, and added validation logic to catch the cases where it didn't. Getting a model to consistently produce a specific output format requires treating the prompt like a specification — precise, unambiguous, and explicit about edge cases.

In Folio (what you're talking to right now), the critical prompt engineering decision was accuracy. The system prompt includes explicit rules: use only facts from the retrieved context, never invent project descriptions or technical details. For a portfolio chatbot that an employer might ask factual questions to, hallucination isn't just an inconvenience — it's a trust problem. That constraint shaped both the prompt and the retrieval design: the more specific and accurate the retrieved context, the less the model has to improvise.

---

**emotion:** happy
**suggestions:**
- Do you have experience with LLMs?
- Tell me about moh-ami
- What technical decision would you redo?
- What is Folio?
- How do you approach adding LLM features?
- What's your experience with RAG systems?
