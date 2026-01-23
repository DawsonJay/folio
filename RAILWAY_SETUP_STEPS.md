# Railway Setup - Step-by-Step Instructions

## The Problem
Railway is trying to build from the repository root and can't determine how to build because it sees both `backend/` and `frontend/` directories.

## The Solution
You need to create **TWO separate services** in Railway, one for backend and one for frontend, each with its root directory configured.

## Step-by-Step Setup

### Step 1: Create Backend Service

1. Go to [Railway Dashboard](https://railway.app)
2. Click **"New Project"** (or open your existing project)
3. Click **"New Service"** → **"GitHub Repo"**
4. Select your `folio` repository
5. Railway will create a service - **name it "backend"** (or rename it)
6. **CRITICAL**: Click on the service → Click **"Settings"** (gear icon)
7. Scroll down to **"Root Directory"**
8. **Set it to:** `backend` (just the word "backend", no slash, no dot)
9. Click **"Save"** or **"Update"**

### Step 2: Create Frontend Service

1. In the same Railway project, click **"New Service"** again
2. Select **"GitHub Repo"** → Choose the same `folio` repository
3. **Name it "frontend"** (or rename it)
4. **CRITICAL**: Click on the service → Click **"Settings"** (gear icon)
5. Scroll down to **"Root Directory"**
6. **Set it to:** `frontend` (just the word "frontend", no slash, no dot)
7. Click **"Save"** or **"Update"**

### Step 3: Verify Configuration

After setting root directories, Railway should:
- **Backend service**: Look in `backend/` directory, find `requirements.txt` and `nixpacks.toml`
- **Frontend service**: Look in `frontend/` directory, find `package.json` and `nixpacks.toml`

### Step 4: Trigger Deployment

1. Push a new commit to GitHub, OR
2. In Railway, click **"Redeploy"** on each service

### Step 5: Check Build Logs

- Backend should show: "Using Nixpacks" and Python build steps
- Frontend should show: "Using Nixpacks" and Node.js build steps

## Troubleshooting

### If you only see ONE service:
- You need to create a SECOND service for the frontend
- Railway doesn't auto-detect monorepos - you must create separate services

### If Root Directory setting is missing:
- Make sure you're in the service Settings, not project Settings
- The setting is under the individual service, not the project

### If build still fails:
- Verify the root directory is set correctly (no leading/trailing slashes)
- Check that `backend/nixpacks.toml` and `frontend/nixpacks.toml` exist
- Check build logs for specific error messages

## Expected Result

After setup, you should have:
- **Two services** in your Railway project: "backend" and "frontend"
- **Backend service** building from `backend/` directory
- **Frontend service** building from `frontend/` directory
- Both services deploying successfully

