# Analytics Setup Guide

This guide explains how to set up and use the analytics feature for tracking user questions.

## Overview

The analytics system tracks all questions asked by users, including:
- Full question text
- Response confidence and score
- Response time in milliseconds
- Session ID for tracking conversations
- Timestamp of when the question was asked

## Local Development Setup

### 1. Install Dependencies

First, make sure you have the updated requirements installed:

```bash
cd backend
pip install -r requirements.txt
```

This will install Alembic (the database migration tool) and other dependencies.

### 2. Start Local PostgreSQL Database

We use Docker Compose to run PostgreSQL locally:

```bash
cd backend
docker-compose up -d
```

This starts a PostgreSQL 15 container on port 5432 with:
- Database: `folio_db`
- User: `folio_user`
- Password: `folio_password`

### 3. Configure Environment Variables

Create a `.env` file in the `backend` directory:

```bash
DATABASE_URL=postgresql://folio_user:folio_password@localhost:5432/folio_db
OPENAI_API_KEY=your_openai_key_here
```

### 4. Run Database Migrations

Apply the database schema using Alembic:

```bash
cd backend
alembic upgrade head
```

This creates the `analytics_events` table in your local database.

### 5. Start the API Server

```bash
cd backend
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## Database Commands

### Check PostgreSQL Status

```bash
docker-compose ps
```

### Stop PostgreSQL

```bash
docker-compose down
```

### Reset Database (Delete All Data)

```bash
docker-compose down -v
docker-compose up -d
alembic upgrade head
```

### View PostgreSQL Logs

```bash
docker-compose logs -f postgres
```

## API Endpoints

### Get Question Analytics

**GET** `/api/analytics/questions`

Query parameters:
- `days` (optional): Filter questions from last N days
- `limit` (optional): Limit number of results

Example:
```bash
curl "http://localhost:8000/api/analytics/questions?days=7&limit=10"
```

Response:
```json
{
  "questions": [
    {
      "question": "What is Folio?",
      "count": 15,
      "last_asked": "2026-02-13T10:30:00Z",
      "first_asked": "2026-02-10T08:15:00Z"
    }
  ],
  "total_unique": 25,
  "total_questions": 150
}
```

### Reset Question Analytics

**POST** `/api/analytics/reset`

Deletes all question records from the database.

Example:
```bash
curl -X POST "http://localhost:8000/api/analytics/reset"
```

Response:
```json
{
  "deleted_count": 150,
  "message": "Successfully deleted 150 question records"
}
```

## Database Schema

### analytics_events Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| event_type | String | Event type (e.g., "question_asked") |
| timestamp | DateTime | When the event occurred (UTC) |
| session_id | String | User session identifier |
| question_text | Text | Full question text |
| answer_text | Text | Answer provided (optional) |
| confidence | String | Confidence level (high/medium/low/redirect) |
| top_score | Float | Similarity score from vector search |
| response_time_ms | Integer | Response time in milliseconds |
| ip_address | String | User IP address (optional) |
| user_agent | String | User agent string (optional) |
| metadata | JSON | Additional event data (optional) |

## How It Works

1. User asks a question via the `/api/chat` endpoint
2. The chat endpoint processes the question and generates a response
3. Before returning the response, the question is logged to the `analytics_events` table
4. Each question is stored with full metadata (confidence, response time, etc.)
5. Analytics endpoints aggregate this data to show unique questions with counts

## Testing analytics

Use the same prerequisites as [Local Development Setup](#local-development-setup): PostgreSQL (e.g. Docker Compose), `DATABASE_URL` + `OPENAI_API_KEY` in `backend/.env`, `alembic upgrade head`, and `uvicorn app.main:app --reload`.

### Option 1: Automated script (recommended)

```bash
cd backend
python scripts/test_analytics.py
```

This resets analytics, posts several chat questions (with duplicates), checks counts, and exercises optional query filters (`days`, `limit`).

### Option 2: Manual testing with curl

**Reset:**

```bash
curl -X POST http://localhost:8000/api/analytics/reset
```

**Ask questions via chat:**

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Folio?"}'

curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Tell me about your experience"}'

curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Folio?"}'
```

**Inspect aggregates:**

```bash
curl "http://localhost:8000/api/analytics/questions?days=7&limit=10"
```

### Option 3: FastAPI `/docs`

Open `http://localhost:8000/docs`, try `GET /api/analytics/questions` and `POST /api/analytics/reset`.

### Option 4: Database inspection

With Docker Postgres (container name may vary; check `docker ps`):

```bash
docker exec -it folio_postgres_local psql -U folio_user -d folio_db -c \
  "SELECT question_text, confidence, response_time_ms, timestamp FROM analytics_events ORDER BY timestamp DESC LIMIT 10;"
```

### Verify behavior

- Chat still works if analytics persistence fails (errors should be swallowed in the chat path where implemented).
- Duplicate question texts aggregate with `count` > 1 in `/api/analytics/questions`.
- `GET /db-test` reports DB connectivity if you need to debug connection issues locally.

### Alternative: existing local PostgreSQL

If you already run Postgres on port 5432 instead of Compose, point `DATABASE_URL` at your instance, create database `folio_db`, then run `alembic upgrade head`. See [SETUP-INSTRUCTIONS.md](SETUP-INSTRUCTIONS.md).

## Production Deployment

On Railway (or other production environments):

1. Railway automatically provides the `DATABASE_URL` environment variable
2. The app detects Railway's PostgreSQL URL format and adjusts it automatically
3. Run migrations: `alembic upgrade head`
4. The analytics system starts tracking questions immediately

## Extending the System

The `analytics_events` table is designed to be extensible. The `event_type` field allows tracking other events:

- `suggestion_clicked` - Track which suggestions users click
- `session_started` - Track new sessions
- `conversation_exported` - Track when users export conversations
- `project_link_clicked` - Track project engagement

To add new event types, use the `AnalyticsService.log_question()` method with different event_type values, or create new specialized methods in the service.

## Troubleshooting

### "alembic: command not found"

Make sure you've installed the requirements:
```bash
pip install -r requirements.txt
```

### "could not connect to server"

Make sure PostgreSQL is running:
```bash
docker-compose up -d
docker-compose ps
```

### "table already exists" error

This means the tables were created with `create_all()` instead of migrations. Drop them first:
```bash
docker-compose down -v
docker-compose up -d
alembic upgrade head
```

### Reset everything and start fresh

```bash
cd backend
docker-compose down -v
docker-compose up -d
alembic upgrade head
uvicorn app.main:app --reload
```

