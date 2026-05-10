# 🚂 Railway Backend Deployment Guide

## Quick Start (5 minutes)

This guide will walk you through deploying the Groww MF Saathi backend on Railway.

---

## Prerequisites

1. **GitHub Account** - Repository already pushed to: `https://github.com/Ashabharathy/Groww-Mutual-Fund-FAQ-Assistant.git`
2. **Railway Account** - Sign up at https://railway.app (free tier available)
3. **Groq API Key** - Get from https://console.groq.com/keys

---

## Step 1: Create Railway Account & Project

### 1.1 Sign Up / Log In to Railway

1. Go to https://railway.app
2. Click **"Start Free"** or log in if you have an account
3. You'll be redirected to the dashboard

### 1.2 Create a New Project

1. Click **"New Project"** button (top right)
2. Select **"Deploy from GitHub repo"**
3. Click **"Configure GitHub App"** if prompted
4. Authorize Railway to access your GitHub account
5. Select the repository: `Groww-Mutual-Fund-FAQ-Assistant`
6. Select branch: `master`
7. Click **"Deploy"**

---

## Step 2: Configure Railway Service

Railway will auto-detect the project type. We need to configure it manually:

### 2.1 Set Build Command

1. In Railway dashboard, go to your project
2. Click on the service (should be named something like `groww-mutual-fund-faq-assistant`)
3. Go to **Settings** tab
4. Find **Build Command** and set it to:

```bash
pip install -r src/phase4_ui/requirements.txt && pip install -r src/phase3_rag/requirements.txt && pip install -r src/phase2_embedding/requirements.txt
```

### 2.2 Set Start Command

1. Find **Start Command** and set it to:

```bash
python -m uvicorn src.phase4_ui.api:app --host 0.0.0.0 --port $PORT
```

### 2.3 Set Root Directory (if needed)

- Leave **Root Directory** empty (project root is correct)

---

## Step 3: Add Environment Variables

### 3.1 Add Variables to Railway

1. In the service settings, go to **Variables** tab
2. Click **"Add Variable"** and add the following:

| Key | Value | Notes |
|-----|-------|-------|
| `GROQ_API_KEY` | `sk-...` | Get from https://console.groq.com/keys |
| `HF_HUB_OFFLINE` | `1` | Use cached HuggingFace models |
| `TRANSFORMERS_OFFLINE` | `1` | Disable HF Hub network calls |

**Important:** Do NOT include `PORT` variable - Railway sets this automatically via `$PORT`

### 3.2 Get Your Groq API Key

1. Go to https://console.groq.com/keys
2. Create a new API key if you don't have one
3. Copy the key (starts with `gsk_` or `sk_`)
4. Paste it in Railway's `GROQ_API_KEY` variable

---

## Step 4: Enable Public Networking

1. In Railway service settings, go to **Networking** tab
2. Click **"Generate Domain"** or enable **Public Networking**
3. Copy the generated URL (e.g., `https://groww-mutual-fund-faq-assistant-production.up.railway.app`)
4. **Save this URL** - you'll need it for the frontend deployment

---

## Step 5: Deploy

### 5.1 Trigger Deployment

1. Go back to the **Deployments** tab
2. Click **"Deploy"** button
3. Wait for the build to complete (5-10 minutes)
4. Watch the logs for any errors

### 5.2 Monitor Build Progress

The logs will show:
- `Building...` - Installing dependencies
- `Starting...` - Starting the FastAPI server
- `Listening on 0.0.0.0:PORT` - Server is ready

---

## Step 6: Verify Deployment

### 6.1 Test Health Endpoint

Once deployment is complete, test the health endpoint:

```bash
curl https://YOUR_RAILWAY_URL/api/health
```

Expected response:
```json
{"status": "healthy", "engine_ready": true}
```

### 6.2 Test Query Endpoint

Test a sample query:

```bash
curl -X POST https://YOUR_RAILWAY_URL/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the expense ratio of Tata ELSS Fund?"}'
```

Expected response:
```json
{
  "answer": "The Expense Ratio of Tata ELSS Fund Direct Growth is 0.87% as of 10 May 2026.\n\nSource: https://groww.in/mutual-funds/tata-elss-fund-direct-growth\nLast updated from sources: 2026-05-10"
}
```

### 6.3 Check Logs

If there are errors:
1. Go to **Deployments** tab
2. Click on the latest deployment
3. View the **Logs** to see what went wrong

---

## Common Issues & Solutions

### Issue: `GROQ_API_KEY not found`

**Solution:**
1. Go to Railway service **Variables** tab
2. Verify `GROQ_API_KEY` is set correctly
3. Redeploy the service

### Issue: `ModuleNotFoundError: No module named 'src'`

**Solution:**
1. Verify **Build Command** includes all three requirements files
2. Check that the repository structure is correct
3. Redeploy

### Issue: `Port binding error`

**Solution:**
1. Ensure Start Command uses `$PORT` variable
2. Do NOT hardcode port 8000
3. Redeploy

### Issue: `Model download fails`

**Solution:**
1. Verify `HF_HUB_OFFLINE=1` is set
2. Verify `TRANSFORMERS_OFFLINE=1` is set
3. The embedding model should be cached locally
4. Redeploy

### Issue: `CORS errors from frontend`

**Solution:**
- The backend already has CORS enabled for all origins
- Verify the frontend is sending requests to the correct Railway URL
- Check browser console for the exact error

---

## Next Steps

### After Backend Deployment

1. **Copy the Railway URL** (e.g., `https://groww-mutual-fund-faq-assistant-production.up.railway.app`)
2. **Deploy Frontend on Vercel** - Use this URL as `VITE_API_BASE_URL`
3. **Test End-to-End** - Query from frontend should reach backend

### Monitoring

1. **View Logs:** Go to **Deployments → Logs** to see real-time logs
2. **Check Metrics:** Go to **Metrics** tab to see CPU, memory, network usage
3. **Set Alerts:** Configure alerts for deployment failures (optional)

### Scaling

- **Free Tier:** 5GB/month bandwidth, sufficient for testing
- **Upgrade:** If you exceed limits, upgrade to paid plan ($5-50/month)

---

## Deployment Checklist

- [ ] Railway account created
- [ ] GitHub repository connected to Railway
- [ ] Build Command configured
- [ ] Start Command configured
- [ ] Environment variables added (GROQ_API_KEY, HF_HUB_OFFLINE, TRANSFORMERS_OFFLINE)
- [ ] Public Networking enabled
- [ ] Deployment completed successfully
- [ ] Health endpoint returns `{"status": "healthy", "engine_ready": true}`
- [ ] Sample query returns correct response
- [ ] Railway URL copied for frontend deployment

---

## Useful Links

- **Railway Dashboard:** https://railway.app/dashboard
- **Railway Docs:** https://docs.railway.app
- **Groq Console:** https://console.groq.com
- **GitHub Repository:** https://github.com/Ashabharathy/Groww-Mutual-Fund-FAQ-Assistant

---

## Support

If you encounter issues:

1. Check the **Logs** in Railway dashboard
2. Verify all **Environment Variables** are set correctly
3. Ensure **Build Command** and **Start Command** are correct
4. Check the **Troubleshooting** section above
5. Review Railway documentation: https://docs.railway.app

---

**Status:** Ready for Deployment  
**Last Updated:** May 10, 2026
