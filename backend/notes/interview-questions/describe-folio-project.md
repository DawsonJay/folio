## Question

Can you describe the Folio project?

## Answer

Folio is a conversational, AI‑powered portfolio I built to solve a problem I kept seeing in my own job search. Traditional portfolios are static: everyone sees the same content in the same order, and you can’t ask follow‑up questions. With Folio, hiring managers can ask questions like “What’s your React experience?” or “Tell me about a hard problem you solved,” and get answers in my voice that are tailored to their interests.

Under the hood it uses a retrieval‑augmented pattern: I wrote a set of small, focused notes about my background and projects, the system finds the most relevant notes for each question, and an LLM answers strictly from that information so it stays accurate and consistent. I built a simple full‑stack setup for this—a React chat interface on the front‑end and a Python API on the back‑end that handles retrieval and model calls. I started with a small dataset, measured how well it was pulling the right notes across different projects, fixed hallucinated project details, and only then scaled it up.

I made a few deliberate trade‑offs along the way: for my scale I kept the vector store local rather than adding extra infrastructure, and I focused on accuracy, cost, and maintainability instead of chasing the fanciest models. For me it’s a good example of how I like to work: start from a real user problem, learn whatever AI tools I need, design the simplest architecture that will hold up, and iterate until it’s something I’m comfortable putting in front of real users.

Optionally, when speaking to frontend- or UX-focused interviewers, I sometimes add that on top of the core AI flow, I added a lightweight event system between the backend and the React client so the assistant avatar’s expressions stay in sync with the conversation, making the experience feel more alive without adding much complexity.

## Concepts to memorise (aligned to the answer)

1. **Problem and value**
   - Traditional portfolios are static and one‑size‑fits‑all; they don’t allow follow‑up questions.
   - In your job search you wanted something conversational and tailored.
   - Folio is a conversational, AI‑powered portfolio that lets hiring managers ask what they care about and get answers in your voice.

2. **RAG idea, implementation, and iteration**
   - You wrote small, focused notes about your background and projects.
   - For each question the system retrieves the most relevant notes, and an LLM answers only from those so it stays accurate and consistent.
   - Implementation: React chat frontend and Python API backend handling retrieval and model calls.
   - You started with a small dataset, measured whether the right notes were being pulled for different projects, fixed hallucinations, and then scaled up.

3. **Trade‑offs and working style**
   - You kept the vector store local instead of adding external infrastructure and focused on accuracy, cost, and maintainability rather than chasing the fanciest models.
   - Folio shows how you like to work: start from a real user problem, learn the AI tools you need, design the simplest architecture that will hold up, and iterate until you’re happy putting it in front of real users.

4. **Optional UX detail**
   - For frontend/UX‑focused audiences: you also added a small event system so the assistant avatar’s expressions stay in sync with the conversation for extra polish without much complexity.
