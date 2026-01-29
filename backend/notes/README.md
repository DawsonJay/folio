# Atomic Notes for Folio RAG System

This directory contains 20 atomic notes designed to test the RAG (Retrieval Augmented Generation) system.

## Structure

- `skills/` - Technical skills and expertise (3 notes)
- `work/` - Work experience and achievements (2 notes)
- `values/` - Core values and motivation (2 notes)
- `background/` - Educational and career background (2 notes)
- `resources/` - Project links and resources (1 note)
- `projects/` - WhatNow project deep-dive (10 notes)

## Total: 20 Notes

### General Coverage (10 notes)
1. python-backend-experience
2. react-frontend-experience
3. ai-ml-experience
4. integrations-dashboard-achievement
5. team-dad-leadership
6. wonder-connection-values
7. canadian-immigration-journey
8. artist-to-tech-transition
9. ironhack-bootcamp-education
10. project-links-all

### WhatNow Deep Dive (10 notes)
11. whatnow-overview-and-motivation
12. whatnow-solving-dataset-problem
13. whatnow-deployment-and-links
14. whatnow-two-layer-learning-architecture
15. whatnow-contextual-bandits-implementation
16. whatnow-metadata-to-embeddings-evolution
17. whatnow-frontend-architecture-evolution
18. whatnow-platform-migration-railway-to-render
19. whatnow-technical-challenges-and-solutions
20. whatnow-project-outcomes-and-learnings

## Embedding Notes into Local Storage

To embed these notes into local storage (JSON file):

### 1. Set Environment Variables

Create a `.env` file in the `backend/` directory with:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

**Note:** We use local storage (JSON file) instead of Pinecone for simplicity. For datasets under 1000 notes, local storage is faster and simpler.

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Run the Embedding Script

```bash
cd backend
python scripts/embed_notes.py
```

The script will:
- Read all 20 markdown note files
- Generate embeddings using OpenAI's `text-embedding-3-small` model (1536 dimensions)
- Store embeddings in `backend/embeddings.json` (local file, ~30KB for 20 notes)
- Display progress and confirmation

### 4. Verify Storage

The script will show storage stats at the end to confirm all notes were stored successfully.

## Note Guidelines

All notes follow the guidelines in `backend/docs/ATOMIC-NOTES-GUIDE.md`:
- 200-500 tokens per note
- First-person voice
- Self-contained with complete context
- Natural language optimized for embedding retrieval
- Include relevant links and specific examples

## Testing Strategy

These 20 notes serve as a test set to validate:
1. **Retrieval precision**: Do WhatNow queries retrieve WhatNow notes?
2. **Answer depth**: Are answers about WhatNow richer than about other topics?
3. **Context bleed**: Do WhatNow notes inappropriately appear in unrelated queries?
4. **Note granularity**: Is 10 notes the right level of detail for a project?

See `backend/scripts/test_retrieval.py` for test queries and evaluation.

