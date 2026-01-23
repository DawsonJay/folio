# Railway Deployment Fix

## Issue
Railway was failing to build because it couldn't determine how to build the app from the root directory.

## Solution
Created `nixpacks.toml` files in both `backend/` and `frontend/` directories to explicitly tell Railway how to build each service.

## Configuration Files Added

### Backend (`backend/nixpacks.toml`)
- Specifies Python 3.11
- Installs dependencies from `requirements.txt`
- Starts with uvicorn on the Railway PORT

### Frontend (`frontend/nixpacks.toml`)
- Specifies Node.js 18
- Installs npm dependencies
- Builds the Vite project
- Serves static files from `dist/` directory

## Railway Service Configuration

**Important**: In the Railway dashboard, you need to set the root directory for each service:

1. **Backend Service**:
   - Go to service settings
   - Set "Root Directory" to `backend`
   - Railway will use `backend/nixpacks.toml`

2. **Frontend Service**:
   - Go to service settings  
   - Set "Root Directory" to `frontend`
   - Railway will use `frontend/nixpacks.toml`

## Alternative: Using Railway CLI

If you prefer, you can also configure this via Railway CLI:
```bash
railway service --set rootDirectory=backend
railway service --set rootDirectory=frontend
```

## Verification

After setting root directories:
1. Backend should detect Python and build successfully
2. Frontend should detect Node.js and build successfully
3. Both services should deploy and start correctly

