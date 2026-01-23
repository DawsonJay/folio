# Railway Deployment Guide

This guide explains how to deploy the Folio project using a monorepo structure with separate backend and frontend services.

## Production URLs

**Backend API:** https://folio-production-16b7.up.railway.app

- Health Check: https://folio-production-16b7.up.railway.app/health
- Database Test: https://folio-production-16b7.up.railway.app/db-test

**Frontend:** (URL will be provided after frontend service is created)

- Frontend service URL will be like: `https://folio-frontend-[hash].up.railway.app`

## Architecture

The project uses a **monorepo structure** with two separate Railway services:

- **Backend Service**: FastAPI application (Python)
- **Frontend Service**: React application (Node.js)

Both services are deployed from the same GitHub repository but run as independent services that can scale and deploy separately.

## Prerequisites

1. Railway account (you already have one)
2. GitHub repository connected
3. Environment variables ready

## Deployment Steps

### Backend Service Setup

#### 1. Create Backend Service

1. Go to [Railway Dashboard](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `folio` repository
5. Railway will create a service

#### 2. Configure Backend Root Directory

**CRITICAL STEP - THIS MUST BE DONE:**

1. Click on your service in Railway
2. Click **Settings** (gear icon) in the top right
3. Scroll down to find **"Root Directory"** setting
4. **Set Root Directory to:** `backend` (just the word "backend", no slashes)
5. Click **Save** or **Update**

**Why this is critical:** The project is organized with `backend/` and `frontend/` directories. Setting root directory to `backend` tells Railway to look in the `backend/` directory where `requirements.txt`, `Procfile`, and `app/main.py` are located.

**After setting root directory:** Railway will auto-detect Python from `requirements.txt` and use the `Procfile` start command.

#### 3. Set Backend Start Command (Optional but Recommended)

After setting the root directory, you may need to set the start command:

1. In your service Settings
2. Find **"Start Command"** or **"Deploy"** section
3. Set it to: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Save

Railway might auto-detect this, but setting it explicitly ensures it works.

#### 4. How Backend Works

Once root directory is set to `backend`:
1. Railway detects `requirements.txt` in the `backend/` directory
2. Auto-detects Python and installs dependencies
3. Runs the start command to start FastAPI
4. Your API is live!

### Frontend Service Setup

#### 1. Create Frontend Service

1. In your Railway project dashboard
2. Click **"New"** → **"GitHub Repo"**
3. Select the same `folio` repository (same repo as backend)
4. Railway will create a new service

#### 2. Configure Frontend Root Directory

**CRITICAL STEP - THIS MUST BE DONE:**

1. Click on the new frontend service in Railway
2. Click **Settings** (gear icon) in the top right
3. Scroll down to find **"Root Directory"** setting
4. **Set Root Directory to:** `frontend` (just the word "frontend", no slashes)
5. Click **Save** or **Update**

**After setting root directory:** Railway will auto-detect Node.js from `package.json` and use `nixpacks.toml` for build configuration.

#### 3. Configure Frontend Environment Variables

1. In your frontend service, go to **Variables** tab
2. Add new variable:
   - **Name:** `VITE_API_URL`
   - **Value:** `https://folio-production-16b7.up.railway.app` (your backend URL)
3. Click **Save**

**Why this is needed:** The frontend needs to know where to find the backend API. This environment variable is used at build time by Vite.

#### 4. How Frontend Works

Once root directory is set to `frontend`:
1. Railway detects `package.json` in the `frontend/` directory
2. Reads `frontend/nixpacks.toml` → installs Node.js 18
3. Runs `npm install`
4. Runs `npm run build` (builds React app)
5. Starts with `npx serve dist -p $PORT` (serves static files)

### Environment Variables

#### Backend Service Variables

Set these in Railway dashboard → Backend Service → Variables:

**Required:**
- `PORT` (auto-set by Railway)
- `DATABASE_URL` - PostgreSQL connection string (auto-provided by Railway if PostgreSQL service is added)

**For future RAG implementation:**
- `OPENAI_API_KEY` - Your OpenAI API key
- `PINECONE_API_KEY` - Your Pinecone API key
- `PINECONE_ENVIRONMENT` - Your Pinecone environment
- `PINECONE_INDEX_NAME` - Your Pinecone index name

**For future rate limiting:**
- `REDIS_URL` - Redis connection string (Railway provides this if you add a Redis service)

#### Frontend Service Variables

Set these in Railway dashboard → Frontend Service → Variables:

**Required:**
- `VITE_API_URL` - Backend API URL (e.g., `https://folio-production-16b7.up.railway.app`)
- `PORT` (auto-set by Railway)

### 5. Verify Deployment

#### Backend Verification

1. **Health Check**: Visit `https://folio-production-16b7.up.railway.app/health`
   - Should return: `{"status": "ok"}`

2. **Root Endpoint**: Visit `https://folio-production-16b7.up.railway.app/`
   - Should return: `{"message": "Folio API", "version": "0.1.0", "status": "running"}`

3. **Database Test**: Visit `https://folio-production-16b7.up.railway.app/db-test`
   - Should return: `{"status": "connected", "test_items_count": 0}`

#### Frontend Verification

1. **Visit Frontend URL**: Railway will provide a URL like `https://folio-frontend-[hash].up.railway.app`
   - Should show the React application
   - Should display "✓ Backend Connected" (green status) if backend is reachable

2. **Check Backend Connection**: The frontend should successfully call the backend health endpoint
   - If connection fails, verify `VITE_API_URL` environment variable is set correctly

## Project Structure

```
folio/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app (API endpoints)
│   │   ├── database.py      # SQLAlchemy database setup
│   │   └── models/          # Database models
│   ├── Procfile             # Start command for Railway
│   ├── requirements.txt     # Python dependencies
│   └── runtime.txt          # Python version pinning
├── frontend/
│   ├── src/                 # React source code
│   ├── dist/                # Built static files (generated by build)
│   ├── nixpacks.toml        # Build configuration for Railway
│   ├── railway.json         # Railway deployment config
│   └── package.json         # Node.js dependencies
└── ...
```

## Current Status

- **Backend**: FastAPI app with health check and database connection ✓
- **Frontend**: React app ready for deployment (separate service) ✓
- **Architecture**: Two-service monorepo deployment

## Troubleshooting

### Backend Build Fails
- Check that root directory is set to `backend`
- Verify `backend/requirements.txt` exists
- Verify `backend/Procfile` exists
- Check build logs for specific errors
- Verify Python version in `backend/runtime.txt` is compatible

### Frontend Build Fails
- Check that root directory is set to `frontend`
- Verify `frontend/package.json` exists
- Verify `frontend/nixpacks.toml` exists
- Check build logs for specific errors
- Verify Node.js version in `frontend/nixpacks.toml` is compatible

### Frontend Not Loading
- Verify frontend build completed successfully
- Check that `frontend/dist/` directory exists after build
- Verify frontend service is running (check Railway dashboard)
- Check frontend service logs for errors

### API Not Working
- Verify backend service is running
- Check backend service logs for errors
- Verify `VITE_API_URL` environment variable is set correctly in frontend service
- Test backend endpoints directly (e.g., `/health`, `/db-test`)

### Frontend Can't Connect to Backend
- Verify `VITE_API_URL` environment variable is set in frontend service
- Check that backend URL is correct (no trailing slashes)
- Verify backend CORS settings allow frontend origin
- Check browser console for CORS errors
- Test backend health endpoint directly in browser

### CORS Issues
- Backend CORS is currently set to allow all origins (`*`)
- For production, update `backend/app/main.py` to allow only your frontend domain
- Verify CORS middleware is configured in `backend/app/main.py`

## Benefits of Two-Service Architecture

- **Independent scaling**: Frontend and backend can scale separately
- **Independent deployment**: Deploy frontend without affecting backend
- **Better architecture**: Separation of concerns
- **Portfolio value**: Demonstrates microservices understanding
- **Industry standard**: Matches real-world deployment patterns
- **Flexibility**: Easy to add CDN, different hosting, etc. later

## Next Steps

After successful deployment:
1. Set up custom domain (optional) for both services
2. Configure production environment variables for both services
3. Update CORS settings for production (restrict to frontend domain)
4. Set up monitoring and logging for both services
5. Add PostgreSQL and Redis services when ready
6. Configure Railway networking if needed (service-to-service communication)
