# Railway Deployment Guide

This guide explains how to deploy both the backend and frontend services to Railway via GitHub.

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
5. Railway will detect both services automatically

### 2. Configure Backend Service

1. Railway should auto-detect the backend service from `backend/requirements.txt`
2. If not, manually add a service and point it to the `backend/` directory
3. Set the start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Railway will automatically set the `PORT` environment variable

**Environment Variables to Set:**
- `PORT` (auto-set by Railway)
- Future: `OPENAI_API_KEY`, `PINECONE_API_KEY`, `DATABASE_URL`, `REDIS_URL`

### 3. Configure Frontend Service

1. Add a new service in the same Railway project
2. Point it to the `frontend/` directory
3. Railway will auto-detect Node.js from `package.json`
4. Build command: `npm install && npm run build`
5. Start command: `npm run preview` (or use a static file server)

**Alternative: Use Static File Serving**

For production, you might want to use a static file server. Update `frontend/package.json`:

```json
{
  "scripts": {
    "serve": "npx serve dist -p $PORT"
  }
}
```

Then set start command to: `npm run serve`

**Environment Variables to Set:**
- `VITE_API_URL` - Set this to your backend Railway URL (e.g., `https://your-backend.railway.app`)
- `PORT` (auto-set by Railway)

### 4. Get Backend URL

1. After backend deploys, Railway provides a public URL
2. Copy this URL (e.g., `https://folio-backend.railway.app`)
3. Set this as `VITE_API_URL` in the frontend service environment variables

### 5. Verify Deployment

1. **Backend Health Check**: Visit `https://your-backend.railway.app/health`
   - Should return: `{"status": "ok"}`

2. **Frontend**: Visit your frontend Railway URL
   - Should display "Folio" with backend connection status

## Project Structure on Railway

Railway will create two services in one project:
- **backend** - FastAPI service
- **frontend** - React static site

Both services can share environment variables if needed.

## Troubleshooting

### Backend Issues
- Check logs in Railway dashboard
- Verify `requirements.txt` is correct
- Ensure `uvicorn` is in requirements
- Check that `PORT` environment variable is set

### Frontend Issues
- Verify `VITE_API_URL` is set correctly
- Check build logs for TypeScript errors
- Ensure all dependencies are in `package.json`
- Verify the build output exists in `dist/`

### CORS Issues
- Backend CORS is currently set to allow all origins (`*`)
- For production, update `backend/app/main.py` to allow only your frontend domain

## Next Steps

After successful deployment:
1. Set up custom domains (optional)
2. Configure production environment variables
3. Update CORS settings for production
4. Set up monitoring and logging
5. Configure database and Redis services when ready

