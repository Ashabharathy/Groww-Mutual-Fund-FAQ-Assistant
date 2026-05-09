# 🚀 Railway Deployment - Quick Start (Step by Step)

## Overview

This is a **visual step-by-step guide** to deploy the Groww MF Saathi backend on Railway in **5 minutes**.

---

## What You'll Need

✅ GitHub account (already have it)  
✅ Groq API key (get from https://console.groq.com/keys)  
✅ Railway account (free at https://railway.app)

---

## Step 1: Go to Railway Dashboard

**URL:** https://railway.app

1. Click **"Start Free"** or log in
2. You'll see the Railway dashboard

---

## Step 2: Create New Project

**In Railway Dashboard:**

1. Click **"New Project"** (top right button)
2. Select **"Deploy from GitHub repo"**
3. Click **"Configure GitHub App"** (if first time)
4. Authorize Railway to access GitHub
5. Select repository: **`Groww-Mutual-Fund-FAQ-Assistant`**
6. Select branch: **`master`**
7. Click **"Deploy"**

**⏱️ Wait 1-2 minutes for Railway to initialize**

---

## Step 3: Configure Build & Start Commands

**In Railway Service Settings:**

### 3.1 Go to Settings Tab

1. Click on your service (should appear in the project)
2. Click **"Settings"** tab

### 3.2 Set Build Command

Find the **Build Command** field and paste:

```bash
pip install -r src/phase4_ui/requirements.txt && pip install -r src/phase3_rag/requirements.txt && pip install -r src/phase2_embedding/requirements.txt
```

### 3.3 Set Start Command

Find the **Start Command** field and paste:

```bash
python -m uvicorn src.phase4_ui.api:app --host 0.0.0.0 --port $PORT
```

**✅ Save changes**

---

## Step 4: Add Environment Variables

**In Railway Service Settings:**

1. Click **"Variables"** tab
2. Click **"Add Variable"** button
3. Add these three variables:

### Variable 1: GROQ_API_KEY

- **Key:** `GROQ_API_KEY`
- **Value:** `sk-...` (your Groq API key from https://console.groq.com/keys)

### Variable 2: HF_HUB_OFFLINE

- **Key:** `HF_HUB_OFFLINE`
- **Value:** `1`

### Variable 3: TRANSFORMERS_OFFLINE

- **Key:** `TRANSFORMERS_OFFLINE`
- **Value:** `1`

**✅ All three variables added**

---

## Step 5: Enable Public Networking

**In Railway Service Settings:**

1. Click **"Networking"** tab
2. Click **"Generate Domain"** button
3. Copy the generated URL (e.g., `https://groww-mf-backend-prod.up.railway.app`)
4. **Save this URL** - you'll need it for frontend

**Example URL:**
```
https://groww-mf-backend-prod.up.railway.app
```

---

## Step 6: Deploy

**In Railway Dashboard:**

1. Go to **"Deployments"** tab
2. Click **"Deploy"** button
3. Watch the logs for build progress

**⏱️ Wait 5-10 minutes for deployment to complete**

You'll see:
- ✅ `Building...`
- ✅ `Installing dependencies...`
- ✅ `Starting server...`
- ✅ `Listening on 0.0.0.0:PORT`

---

## Step 7: Verify Deployment

### Test 1: Health Check

Open your browser and go to:
```
https://YOUR_RAILWAY_URL/api/health
```

You should see:
```json
{"status":"healthy","engine_ready":true}
```

### Test 2: Query Test

Open your browser and go to:
```
https://YOUR_RAILWAY_URL/api/query?query=What%20is%20the%20expense%20ratio%20of%20Tata%20ELSS%20Fund?
```

Or use curl:
```bash
curl -X POST https://YOUR_RAILWAY_URL/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the expense ratio of Tata ELSS Fund?"}'
```

You should see a response with the answer and source.

---

## ✅ Deployment Complete!

Your backend is now live on Railway! 🎉

**Your Backend URL:**
```
https://YOUR_RAILWAY_URL
```

---

## Next: Deploy Frontend on Vercel

1. Go to https://vercel.com
2. Create new project from GitHub
3. Select `Groww-Mutual-Fund-FAQ-Assistant` repository
4. Set **Root Directory** to `src/phase4_ui/frontend`
5. Add environment variable:
   - **Key:** `VITE_API_BASE_URL`
   - **Value:** `https://YOUR_RAILWAY_URL/api`
6. Deploy

---

## Troubleshooting

### ❌ Deployment Failed

**Check the logs:**
1. Go to **Deployments** tab
2. Click on the failed deployment
3. View **Logs** to see the error

**Common fixes:**
- Verify `GROQ_API_KEY` is set correctly
- Verify Build Command includes all three requirements files
- Verify Start Command uses `$PORT` (not hardcoded 8000)

### ❌ Health Check Returns Error

**Solution:**
1. Check Railway logs for errors
2. Verify all environment variables are set
3. Redeploy the service

### ❌ CORS Errors from Frontend

**Solution:**
- Backend already has CORS enabled
- Verify frontend is using correct Railway URL
- Check browser console for exact error

---

## Monitoring

**View Logs:**
- Go to **Deployments** → Click deployment → **Logs**

**View Metrics:**
- Go to **Metrics** tab to see CPU, memory, network usage

**Set Alerts (Optional):**
- Go to **Settings** → **Alerts** to configure notifications

---

## Useful Commands

### Test Health Endpoint
```bash
curl https://YOUR_RAILWAY_URL/api/health
```

### Test Query Endpoint
```bash
curl -X POST https://YOUR_RAILWAY_URL/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Who is the fund manager of Tata Small Cap Fund?"}'
```

### View Logs (if you have Railway CLI installed)
```bash
railway logs
```

---

## Summary

| Step | Action | Time |
|------|--------|------|
| 1 | Create Railway project | 1 min |
| 2 | Configure build/start commands | 1 min |
| 3 | Add environment variables | 1 min |
| 4 | Enable public networking | 1 min |
| 5 | Deploy | 5-10 min |
| 6 | Verify deployment | 1 min |
| **Total** | | **10-15 min** |

---

## Links

- **Railway Dashboard:** https://railway.app/dashboard
- **Groq Console:** https://console.groq.com/keys
- **GitHub Repo:** https://github.com/Ashabharathy/Groww-Mutual-Fund-FAQ-Assistant
- **Railway Docs:** https://docs.railway.app

---

**Status:** Ready to Deploy  
**Last Updated:** May 10, 2026
