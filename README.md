# Folio

A portfolio website with an AI assistant that answers questions about skills, experience, and projects. Retrieval uses embeddings and cosine similarity stored locally; common questions can be answered from **Tier 1** hand-written notes before falling back to **Tier 2** RAG generation.

## Overview

Users chat with Folio through a React frontend. The backend (FastAPI) routes questions through profanity/off-topic checks, **direct-answer** matching, then RAG over embedded markdown notes, using OpenAI for embeddings and chat.

## Features

- **AI chat**: Direct-answer routing plus RAG with structured JSON replies (emotion, suggestions, optional project links)
- **Portfolio UI**: Landing chat experience, avatar state, contextual suggestions
- **Contact flow**: EmailJS-powered form (validation, success route)
- **Analytics** (when DB configured): Question logging via PostgreSQL (or SQLite in dev via `DATABASE_URL`)

## Tech stack

### Backend

- FastAPI (Python), Uvicorn  
- OpenAI (`text-embedding-3-small`, `gpt-4o-mini`)  
- Embeddings persisted in **`backend/embeddings.json`** via `LocalEmbeddingStorage`  
- PostgreSQL or SQLite (`DATABASE_URL`; defaults to `sqlite:///./folio.db`), SQLAlchemy, Alembic  

### Frontend

- React + TypeScript, Vite, SCSS  
- EmailJS for contact  

### Deployment

- Backend documented for **Railway** ([`backend/docs/RAILWAY_DEPLOYMENT.md`](backend/docs/RAILWAY_DEPLOYMENT.md)); frontend commonly Vercel/Netlify or a second Railway service.

## Repository layout

```
folio/
├── backend/           # FastAPI app, scripts, docs (backend/docs/)
├── frontend/          # React + Vite app
├── CHAT-RECORDS.md    # Project record conventions
└── README.md          # This file
```

Authoritative developer docs live under **`backend/docs/`** (indexed by [`backend/docs/README.md`](backend/docs/README.md)).

## Prerequisites

- Python 3.11+  
- Node.js 18+  
- Optional: PostgreSQL locally (Docker Compose in `backend/`) for analytics parity with production  

## Getting started

### Backend

Install into a **venv** under `backend/venv` (required for `npm run dev:all` on the frontend):

```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\python.exe -m pip install -r requirements.txt
# macOS/Linux: ./venv/bin/python -m pip install -r requirements.txt
```

Copy **`backend/.env.example`** to **`backend/.env`** and set at least:

```env
OPENAI_API_KEY=your_key_here
```

Optional (defaults to SQLite file `folio.db` in cwd when absent):

```env
DATABASE_URL=sqlite:///./folio.db
```

For analytics and PostgreSQL-specific workflows, see [`backend/docs/SETUP-INSTRUCTIONS.md`](backend/docs/SETUP-INSTRUCTIONS.md).

Build embeddings after changing notes:

```bash
cd backend
python scripts/embed_direct_answers.py   # Tier 1: notes/tier-1-direct-answers/
python scripts/embed_notes.py            # Tier 2 + other markdown under backend/notes/
```

Run API:

```bash
cd backend
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
```

Create **`frontend/.env`**:

```env
VITE_EMAILJS_SERVICE_ID=...
VITE_EMAILJS_TEMPLATE_ID=...
VITE_EMAILJS_PUBLIC_KEY=...
```

Optional: **`VITE_API_URL`** pointing at your backend base URL when not using local defaults.

Development (frontend + backend from repo root helpers):

```bash
cd frontend
npm run dev          # Frontend only
npm run dev:all      # Frontend + backend (needs backend venv + deps)
```

Tests and lint:

```bash
cd frontend
npm test
npm run lint
npm run build
```

## Documentation

| Topic | Location |
| ----- | -------- |
| Backend overview / index | [`backend/docs/README.md`](backend/docs/README.md) |
| Local setup & embeddings | [`backend/docs/SETUP-INSTRUCTIONS.md`](backend/docs/SETUP-INSTRUCTIONS.md) |
| Tiered notes architecture | [`backend/docs/TIERED-NOTES-SYSTEM.md`](backend/docs/TIERED-NOTES-SYSTEM.md) |
| Analytics | [`backend/docs/ANALYTICS-SETUP.md`](backend/docs/ANALYTICS-SETUP.md) |
| Railway deployment | [`backend/docs/RAILWAY_DEPLOYMENT.md`](backend/docs/RAILWAY_DEPLOYMENT.md) |

Historical planning docs were renamed with an **`ARCHIVE`** suffix — see backend docs index.

## Design

- **Palette**: Dark forest green, off-white UI, terracotta accents  
- **Type**: Plus Jakarta Sans (UI), JetBrains Mono (code)  
- **Layout**: Centered, max-width container  

## License

MIT  

## Author

James Dawson  
