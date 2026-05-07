# Folio Backend — Local setup

This guide matches the current codebase: **FastAPI**, **OpenAI** embeddings + chat, **local embedding store** (`backend/embeddings.json`), **SQLAlchemy** with PostgreSQL or SQLite, and optional **Docker Compose** PostgreSQL for parity with production analytics.

## Prerequisites

- Python **3.11+**
- **`backend/venv`** recommended (required if you use `npm run dev:all` from `frontend/`)
- **OpenAI API key** (required for chat and embeddings)
- **Node** / **Docker** only if you run the frontend or Compose DB

## Environment variables

Copy [`.env.example`](../.env.example) to **`backend/.env`**.

| Variable | Required | Purpose |
| -------- | -------- | ------- |
| `OPENAI_API_KEY` | **Yes** | Embeddings (`text-embedding-3-small`) and chat (`gpt-4o-mini`) |
| `DATABASE_URL` | No | Defaults to `sqlite:///./folio.db` ([`app/database.py`](../app/database.py)). Use PostgreSQL locally or on Railway for analytics. |
| `PORT` | No | Default `8000` locally; Railway sets automatically |

## Install dependencies (venv)

Use the venv interpreter so packages install in the right place:

**Windows (PowerShell):**

```powershell
cd backend
python -m venv venv
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

**macOS / Linux:**

```bash
cd backend
python3 -m venv venv
./venv/bin/python -m pip install --upgrade pip
./venv/bin/python -m pip install -r requirements.txt
```

## Embedding pipeline (after changing notes)

Embeddings are stored in **`backend/embeddings.json`** ([`app/services/embedding_storage.py`](../app/services/embedding_storage.py)). Rebuild whenever Tier 1 or Tier 2 markdown changes.

From **`backend/`**:

```bash
# Tier 1: hand-written Q&A under notes/tier-1-direct-answers/ (excludes metadata/*.md)
python scripts/embed_direct_answers.py

# Tier 2 (+ all other notes): all *.md under backend/notes/ except metadata dirs and template exclusions
python scripts/embed_notes.py
```

**Optional checks:**

- [`scripts/test_retrieval.py`](../scripts/test_retrieval.py) — manual retrieval smoke tests (if present)

## Run the API

```bash
cd backend
uvicorn app.main:app --reload
```

- API root: `http://localhost:8000`
- Interactive docs: `http://localhost:8000/docs`

## Database and analytics

Chat can run with the default **SQLite** file. For **`/api/analytics/*`** and production-like behavior, use **PostgreSQL**:

```bash
cd backend
docker-compose up -d
alembic upgrade head
```

Compose profile and credentials should match your `docker-compose.yml` (defaults are documented in [ANALYTICS-SETUP.md](ANALYTICS-SETUP.md)).

Set in `.env`:

```env
DATABASE_URL=postgresql://folio_user:folio_password@localhost:5432/folio_db
```

Then start the API again. Full analytics setup, API examples, and troubleshooting: **[ANALYTICS-SETUP.md](ANALYTICS-SETUP.md)**.

## Frontend + backend together

From **`frontend/`**:

```bash
npm install
npm run dev:all
```

This expects **`backend/venv`** with dependencies installed. See root [README](../../README.md).

## Project layout (relevant paths)

```
backend/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── api/
│   └── services/
├── notes/
│   ├── tier-1-direct-answers/   # Tier 1 direct answers
│   └── tier-2-atomic-notes/     # Tier 2 RAG corpus (and other note trees)
├── scripts/
│   ├── embed_direct_answers.py
│   ├── embed_notes.py
│   └── ...
├── embeddings.json              # Generated — do not edit by hand
├── alembic/
├── docker-compose.yml
├── requirements.txt
└── docs/                        # This folder
```

## Further reading

| Topic | Doc |
| ----- | --- |
| Backend doc index | [README.md](README.md) |
| Tiered routing architecture | [TIERED-NOTES-SYSTEM.md](TIERED-NOTES-SYSTEM.md) |
| Analytics | [ANALYTICS-SETUP.md](ANALYTICS-SETUP.md) |
| Railway deploy | [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) |
