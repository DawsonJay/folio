# Direct Answer Gaps — To Do

Questions currently handled by RAG (non-deterministic) that need scripted Tier 1 direct answers.
Each one needs a genuine answer from James — 150–200 words, STANDALONE + CURIOSITY framework,
exactly 6 suggestions. See existing files in `backend/notes/tier-1-direct-answers/` for format.

After writing each file: run `python scripts/embed_direct_answers.py` then `python test_canadian_employer.py`.

---

## Technical

- [ ] **How do you approach technical debt?**
  - Currently: conf=high RAG, score=0.417
  - File: `how-do-you-approach-technical-debt.md`

- [ ] **How do you approach frontend performance optimization?**
  - Currently: conf=high RAG, score=0.570
  - File: `how-do-you-approach-performance-optimization.md`

- [ ] **How do you decide when to refactor versus rewrite?**
  - Currently: conf=medium RAG, score=0.392 — gets the "question is a little vague" opener
  - File: `how-do-you-decide-when-to-refactor-versus-rewrite.md`

- [ ] **Tell me about a technical decision you made that you'd do differently now**
  - Currently: conf=high RAG, score=0.459
  - File: `tell-me-about-a-technical-decision-youd-do-differently.md`

---

## Culture & Values

- [ ] **Why do you want to work at a startup rather than a large company?**
  - Currently: conf=high RAG, score=0.447
  - File: `why-do-you-want-to-work-at-a-startup.md`

- [ ] **Describe your ideal work environment**
  - Currently: conf=high RAG, score=0.555
  - File: `describe-your-ideal-work-environment.md`

- [ ] **What kind of problems do you find most interesting to solve?**
  - Currently: conf=high RAG, score=0.438
  - File: `what-kind-of-problems-do-you-find-most-interesting.md`

---

## Needs Rewrite (answer exists but is wrong)

- [ ] **What are your weaknesses as a developer?**
  - Currently: returns the "artistic intuition" answer — a reframe, not a real weakness
  - File: `what-are-your-weaknesses-as-a-developer.md` (rewrite existing)
  - Note: needs a genuine, specific weakness with evidence of self-awareness and steps taken to address it
