# Quick Test Setup

## Current Situation

- PostgreSQL is already running on port 5432
- You need to configure the database connection before testing

## Setup Options

### Option 1: Use Existing PostgreSQL (Recommended)

Create a `.env` file in the `backend` directory:

```bash
cd backend
nano .env
```

Add these lines (adjust credentials if needed):
```
DATABASE_URL=postgresql://your_username:your_password@localhost:5432/folio_db
OPENAI_API_KEY=your_actual_key_here
```

Then create the database:
```bash
# Replace 'your_username' with your PostgreSQL username
createdb -U your_username folio_db
```

### Option 2: Use Railway Database (Production)

If you already have Railway set up:

```bash
cd backend
nano .env
```

Add your Railway PostgreSQL URL:
```
DATABASE_URL=postgresql://...your-railway-url...
OPENAI_API_KEY=your_actual_key_here
```

### Option 3: Stop Existing PostgreSQL and Use Docker

```bash
# Stop existing PostgreSQL
sudo systemctl stop postgresql

# Start Docker PostgreSQL
docker run -d \
  --name folio_postgres_local \
  -e POSTGRES_USER=folio_user \
  -e POSTGRES_PASSWORD=folio_password \
  -e POSTGRES_DB=folio_db \
  -p 5432:5432 \
  postgres:15

# Create .env
cd backend
nano .env
```

Add:
```
DATABASE_URL=postgresql://folio_user:folio_password@localhost:5432/folio_db
OPENAI_API_KEY=your_actual_key_here
```

## After Setting Up Database

Run these commands:

```bash
cd backend

# 1. Install dependencies (if not already)
pip install -r requirements.txt

# 2. Run migrations
alembic upgrade head

# 3. Start the API server (in one terminal)
uvicorn app.main:app --reload

# 4. Run the test script (in another terminal)
python scripts/test_analytics.py
```

## Quick Manual Test (No Setup Required)

If you just want to see if the code is correct without database setup, you can check:

1. **Code Review:**
   ```bash
   # Check the model
   cat app/models/analytics_event.py
   
   # Check the service
   cat app/services/analytics_service.py
   
   # Check the API endpoints
   cat app/api/analytics.py
   ```

2. **Linting:**
   ```bash
   # Check for Python errors
   python -m py_compile app/models/analytics_event.py
   python -m py_compile app/services/analytics_service.py
   python -m py_compile app/api/analytics.py
   ```

## Current Status

✅ Code is written and ready
✅ Database schema is defined
✅ Alembic migrations are created
✅ Test scripts are ready

⏳ Needs: Database connection configured (`.env` file)
⏳ Needs: Migrations run
⏳ Needs: API server started

Would you like me to help with any of these steps?

