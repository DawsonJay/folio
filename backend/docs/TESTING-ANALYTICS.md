# Testing the Analytics Feature

This guide provides multiple ways to test the analytics implementation.

## Prerequisites

1. **Start local PostgreSQL:**
   ```bash
   cd backend
   docker-compose up -d
   ```

2. **Run migrations:**
   ```bash
   alembic upgrade head
   ```

3. **Start the API server:**
   ```bash
   uvicorn app.main:app --reload
   ```

## Option 1: Automated Test Script (Recommended)

Run the automated test script:

```bash
cd backend
python scripts/test_analytics.py
```

This script will:
1. Reset analytics to start fresh
2. Ask 6 test questions (with some duplicates)
3. Verify the analytics count unique questions correctly
4. Test query filters (limit, days)
5. Display a summary of results

Expected output:
- Total questions: 6
- Unique questions: 4
- "What is Folio?" should appear 3 times

## Option 2: Manual Testing with curl

### Step 1: Reset Analytics

```bash
curl -X POST http://localhost:8000/api/analytics/reset
```

Expected response:
```json
{
  "deleted_count": 0,
  "message": "Successfully deleted 0 question records"
}
```

### Step 2: Ask Questions

```bash
# Question 1
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Folio?"}'

# Question 2
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Tell me about your experience"}'

# Question 3 (duplicate of Question 1)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Folio?"}'
```

### Step 3: Check Analytics

```bash
curl http://localhost:8000/api/analytics/questions | jq
```

Expected response:
```json
{
  "questions": [
    {
      "question": "What is Folio?",
      "count": 2,
      "last_asked": "2026-02-13T...",
      "first_asked": "2026-02-13T..."
    },
    {
      "question": "Tell me about your experience",
      "count": 1,
      "last_asked": "2026-02-13T...",
      "first_asked": "2026-02-13T..."
    }
  ],
  "total_unique": 2,
  "total_questions": 3
}
```

### Step 4: Test Filters

**Limit results:**
```bash
curl "http://localhost:8000/api/analytics/questions?limit=1" | jq
```

**Filter by days:**
```bash
curl "http://localhost:8000/api/analytics/questions?days=7" | jq
```

**Combine filters:**
```bash
curl "http://localhost:8000/api/analytics/questions?days=30&limit=5" | jq
```

## Option 3: Interactive Testing via Browser/Frontend

1. Open your frontend application (if running)
2. Ask several questions through the chat interface
3. Click some suggestion chips
4. Visit the analytics endpoint in your browser:
   - http://localhost:8000/api/analytics/questions

You should see both typed questions and clicked suggestions logged.

## Option 4: Direct Database Inspection

Connect to the database and query directly:

```bash
# Connect to PostgreSQL
docker exec -it folio_postgres_local psql -U folio_user -d folio_db

# View all analytics events
SELECT id, event_type, question_text, confidence, response_time_ms, timestamp 
FROM analytics_events 
ORDER BY timestamp DESC 
LIMIT 10;

# Count questions by text
SELECT question_text, COUNT(*) as count
FROM analytics_events
WHERE event_type = 'question_asked'
GROUP BY question_text
ORDER BY count DESC;

# Exit PostgreSQL
\q
```

## Option 5: FastAPI Interactive Docs

1. Go to http://localhost:8000/docs
2. Expand the `/api/analytics/questions` endpoint
3. Click "Try it out"
4. Test with different parameters
5. Expand the `/api/analytics/reset` endpoint
6. Click "Try it out" and "Execute"

## What to Verify

### ✅ Core Functionality
- [ ] Questions are logged to the database
- [ ] Duplicate questions are counted correctly
- [ ] Total questions count is accurate
- [ ] Unique questions count is accurate
- [ ] Timestamps are recorded correctly

### ✅ Metadata Tracking
- [ ] Confidence level is stored
- [ ] Top score is stored
- [ ] Response time is measured in milliseconds
- [ ] Session ID is generated and stored

### ✅ API Endpoints
- [ ] GET `/api/analytics/questions` returns data
- [ ] Query parameter `days` filters results
- [ ] Query parameter `limit` limits results
- [ ] POST `/api/analytics/reset` clears data

### ✅ Chat Integration
- [ ] Typed questions are logged
- [ ] Clicked suggestions are logged
- [ ] High confidence answers are logged
- [ ] Low confidence/redirect answers are logged
- [ ] Profanity-triggered responses are logged

### ✅ Error Handling
- [ ] Analytics errors don't break chat functionality
- [ ] Invalid queries return appropriate errors
- [ ] Database connection errors are handled

## Troubleshooting

### "Connection refused" errors

Make sure the server is running:
```bash
uvicorn app.main:app --reload
```

### "No analytics data" after asking questions

Check if the database is connected:
```bash
curl http://localhost:8000/db-test
```

Check the server logs for analytics errors.

### Database migration issues

Reset and rerun migrations:
```bash
docker-compose down -v
docker-compose up -d
alembic upgrade head
```

### Python dependencies missing

Reinstall requirements:
```bash
pip install -r requirements.txt
```

## Performance Testing

Test with multiple rapid requests:

```bash
for i in {1..20}; do
  curl -X POST http://localhost:8000/api/chat \
    -H "Content-Type: application/json" \
    -d '{"question": "Test question '$i'"}'
  echo ""
done

# Check results
curl http://localhost:8000/api/analytics/questions
```

Verify:
- All 20 questions are logged
- Response times are reasonable (<500ms for analytics)
- No duplicate session IDs unless intended

## Success Criteria

The analytics feature is working correctly if:

1. ✅ All questions asked through the chat are logged
2. ✅ Duplicate questions have count > 1
3. ✅ Unique questions are identified correctly
4. ✅ Response times are measured
5. ✅ Session IDs are tracked
6. ✅ Analytics can be queried with filters
7. ✅ Reset functionality clears data
8. ✅ Chat functionality works even if analytics fails

