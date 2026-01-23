# Railway Deployment Guide

This guide explains how to deploy the Folio project. Currently set up as minimal backend-only deployment. Frontend will be added once backend deploys successfully.

## Prerequisites

1. Railway account (you already have one)
2. GitHub repository connected
3. Environment variables ready

## Deployment Steps

### 1. Connect GitHub Repository to Railway

1. Go to [Railway Dashboard](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `folio` repository
5. Railway will create a service

### 2. Configure Service Root Directory

**CRITICAL STEP:**

1. Click on your service
2. Click **Settings** (gear icon)
3. Scroll down to **Root Directory**
4. **Set Root Directory to:** `backend`
5. Click **Save** or **Update**

This tells Railway to build from the `backend/` directory, which contains the `nixpacks.toml` that builds both frontend and backend.

### 3. How It Works

The `backend/nixpacks.toml` configuration:
1. Installs Python dependencies
2. Starts FastAPI server with:
   - Health check at `/health`
   - Root endpoint at `/`

### 4. Environment Variables

Set these in Railway dashboard → Service → Variables:

**Required:**
- `PORT` (auto-set by Railway)

**For future RAG implementation:**
- `OPENAI_API_KEY` - Your OpenAI API key
- `PINECONE_API_KEY` - Your Pinecone API key
- `PINECONE_ENVIRONMENT` - Your Pinecone environment
- `PINECONE_INDEX_NAME` - Your Pinecone index name

**For future database:**
- `DATABASE_URL` - PostgreSQL connection string (Railway provides this if you add a PostgreSQL service)

**For future rate limiting:**
- `REDIS_URL` - Redis connection string (Railway provides this if you add a Redis service)

### 5. Verify Deployment

1. **Health Check**: Visit `https://your-app.railway.app/health`
   - Should return: `{"status": "ok"}`

2. **Root Endpoint**: Visit `https://your-app.railway.app/`
   - Should return: `{"message": "Folio API", "version": "0.1.0", "status": "running"}`

## Project Structure

```
folio/
├── backend/
│   ├── app/
│   │   └── main.py          # FastAPI app (serves API + frontend)
│   ├── nixpacks.toml        # Builds frontend + backend
│   └── requirements.txt
├── frontend/
│   ├── src/                 # React source code
│   ├── dist/                # Built static files (generated)
│   └── package.json
└── ...
```

## Current Status

- **Backend only**: Minimal FastAPI app with health check
- **Frontend**: Will be added once backend deploys successfully

## Troubleshooting

### Build Fails
- Check that root directory is set to `backend`
- Verify `backend/nixpacks.toml` exists
- Check build logs for specific errors

### Frontend Not Loading
- Verify frontend build completed successfully
- Check that `frontend/dist/` directory exists after build
- Check FastAPI logs for static file serving errors

### API Not Working
- Verify API endpoints are prefixed with `/api/`
- Check CORS settings if making requests from different origin
- Check FastAPI logs for errors

### CORS Issues
- Backend CORS is currently set to allow all origins (`*`)
- For production, update `backend/app/main.py` to allow only your domain

## Next Steps

After successful deployment:
1. Set up custom domain (optional)
2. Configure production environment variables
3. Update CORS settings for production
4. Set up monitoring and logging
5. Add PostgreSQL and Redis services when ready
