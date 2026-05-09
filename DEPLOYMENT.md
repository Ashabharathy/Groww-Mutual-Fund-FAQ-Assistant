# 🚀 Deployment Plan — Groww MF Saathi RAG Chatbot

**Frontend:** Vercel | **Backend:** Railway | **Data Pipeline:** GitHub Actions

---

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Pre-Deployment Checklist](#pre-deployment-checklist)
3. [Backend Deployment (Railway)](#backend-deployment-railway)
4. [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
5. [Environment Variables](#environment-variables)
6. [Post-Deployment Verification](#post-deployment-verification)
7. [Monitoring & Maintenance](#monitoring--maintenance)
8. [Rollback Procedures](#rollback-procedures)

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Repository                         │
│  (Source code + Data pipeline scheduler)                     │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
   ┌─────────────┐          ┌──────────────┐
   │   Vercel    │          │   Railway    │
   │  (Frontend) │          │  (Backend)   │
   │ React/Vite  │◄────────►│  FastAPI     │
   │ Port: 3000  │          │  Port: 8000  │
   └─────────────┘          └──────────────┘
        │                         │
        │                         ▼
        │                   ┌──────────────┐
        │                   │  PostgreSQL  │
        │                   │  (Optional)  │
        │                   └──────────────┘
        │
        └──────────────────────────────────┐
                                           │
                    ┌──────────────────────┴──────────────┐
                    │                                     │
                    ▼                                     ▼
            ┌──────────────────┐            ┌──────────────────┐
            │  GitHub Actions  │            │  HuggingFace Hub │
            │  (Daily 10 AM)   │            │  (Model Cache)   │
            │  Scrape→Chunk→   │            │  all-MiniLM-L6   │
            │  Embed→Commit    │            └──────────────────┘
            └──────────────────┘
```

---

## ✅ Pre-Deployment Checklist

### Local Verification
- [ ] All tests pass locally: `npm run build` (frontend), `pytest` (backend)
- [ ] `.env` file is NOT committed (check `.gitignore`)
- [ ] `venv/`, `node_modules/`, FAISS binaries are excluded
- [ ] Latest code is pushed to `master` branch on GitHub
- [ ] GitHub Actions workflow is enabled (`.github/workflows/data_refresh.yml`)

### GitHub Setup
- [ ] Repository is public (or private with appropriate access)
- [ ] `GROQ_API_KEY` secret is added to GitHub Actions secrets
- [ ] Branch protection rules are configured (optional but recommended)

### Accounts & Credentials
- [ ] Vercel account created and linked to GitHub
- [ ] Railway account created
- [ ] Groq API key obtained
- [ ] HuggingFace account (optional, for model caching)

---

## 🚂 Backend Deployment (Railway)

### Step 1: Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize Railway to access your GitHub account
5. Select the `Groww-Mutual-Fund-FAQ-Assistant` repository
6. Select `master` branch

### Step 2: Configure Railway Service

1. **Service Name:** `groww-mf-backend`
2. **Root Directory:** Leave empty (project root)
3. **Build Command:** 
   ```bash
   pip install -r src/phase4_ui/requirements.txt && \
   pip install -r src/phase3_rag/requirements.txt && \
   pip install -r src/phase2_embedding/requirements.txt
   ```
4. **Start Command:**
   ```bash
   python -m uvicorn src.phase4_ui.api:app --host 0.0.0.0 --port $PORT
   ```

### Step 3: Set Environment Variables

In Railway dashboard, go to **Variables** and add:

```
GROQ_API_KEY=<your-groq-api-key>
HF_HUB_OFFLINE=1
TRANSFORMERS_OFFLINE=1
PORT=8000
```

### Step 4: Configure Networking

1. Go to **Settings → Networking**
2. Enable **Public Networking**
3. Copy the generated URL (e.g., `https://groww-mf-backend-prod.up.railway.app`)
4. This URL will be used in the frontend `.env`

### Step 5: Deploy

1. Click **"Deploy"**
2. Wait for build to complete (5-10 minutes)
3. Check logs for any errors
4. Test the health endpoint:
   ```bash
   curl https://groww-mf-backend-prod.up.railway.app/api/health
   ```
   Expected response:
   ```json
   {"status": "healthy", "engine_ready": true}
   ```

---

## 🎨 Frontend Deployment (Vercel)

### Step 1: Create Vercel Project

1. Go to [vercel.com](https://vercel.com)
2. Click **"Add New"** → **"Project"**
3. Select **"Import Git Repository"**
4. Authorize Vercel to access GitHub
5. Select `Groww-Mutual-Fund-FAQ-Assistant` repository
6. Click **"Import"**

### Step 2: Configure Build Settings

1. **Framework Preset:** Select **"Vite"**
2. **Root Directory:** `src/phase4_ui/frontend`
3. **Build Command:**
   ```bash
   npm run build
   ```
4. **Output Directory:** `dist`
5. **Install Command:**
   ```bash
   npm install
   ```

### Step 3: Set Environment Variables

In Vercel dashboard, go to **Settings → Environment Variables** and add:

```
VITE_API_BASE_URL=https://groww-mf-backend-prod.up.railway.app/api
```

(Replace with your actual Railway backend URL)

### Step 4: Deploy

1. Click **"Deploy"**
2. Wait for build to complete (2-3 minutes)
3. Vercel will provide a URL (e.g., `https://groww-mf-saathi.vercel.app`)
4. Test the frontend by visiting the URL

### Step 5: Configure Custom Domain (Optional)

1. Go to **Settings → Domains**
2. Add your custom domain (e.g., `groww-mf.yourdomain.com`)
3. Follow DNS configuration instructions

---

## 🔐 Environment Variables

### Backend (Railway)

| Variable | Value | Notes |
|---|---|---|
| `GROQ_API_KEY` | `sk-...` | Get from [console.groq.com](https://console.groq.com) |
| `HF_HUB_OFFLINE` | `1` | Use cached HuggingFace models |
| `TRANSFORMERS_OFFLINE` | `1` | Disable HF Hub network calls |
| `PORT` | `8000` | Railway assigns dynamically; use `$PORT` |

### Frontend (Vercel)

| Variable | Value | Notes |
|---|---|---|
| `VITE_API_BASE_URL` | `https://groww-mf-backend-prod.up.railway.app/api` | Backend API endpoint |

### GitHub Actions (for data refresh pipeline)

| Secret | Value | Notes |
|---|---|---|
| `GROQ_API_KEY` | `sk-...` | Same as backend |

---

## ✔️ Post-Deployment Verification

### Backend Health Check

```bash
# Test health endpoint
curl https://groww-mf-backend-prod.up.railway.app/api/health

# Test query endpoint
curl -X POST https://groww-mf-backend-prod.up.railway.app/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the expense ratio of Tata ELSS Fund?"}'
```

### Frontend Smoke Tests

1. Open frontend URL in browser
2. Verify sidebar loads with user info (Asha, ashabharathy@gmail.com)
3. Verify Groww logo appears in top-left
4. Test a suggestion query (e.g., "Expense ratio of Tata ELSS Fund?")
5. Verify response appears with source link
6. Test theme toggle (dark/light)
7. Test dual chat mode

### End-to-End Test

1. Frontend sends query to backend
2. Backend retrieves chunks from FAISS index
3. Groq LLM generates response
4. Response displays with source citation
5. No CORS errors in browser console

---

## 📊 Monitoring & Maintenance

### Railway Monitoring

1. **Logs:** Go to **Deployments → Logs** to view real-time backend logs
2. **Metrics:** Check **Metrics** tab for CPU, memory, and network usage
3. **Alerts:** Set up alerts for deployment failures or high resource usage

### Vercel Monitoring

1. **Deployments:** View all deployments in **Deployments** tab
2. **Analytics:** Check **Analytics** for page load times and traffic
3. **Error Tracking:** Monitor **Error Tracking** for client-side errors

### GitHub Actions Monitoring

1. Go to **Actions** tab in GitHub
2. Monitor `Daily Data Refresh` workflow runs
3. Check logs if a run fails
4. Verify data is committed back to repo daily

### Uptime Monitoring (Optional)

Use a service like [UptimeRobot](https://uptimerobot.com) to monitor:
- Backend health endpoint: `https://groww-mf-backend-prod.up.railway.app/api/health`
- Frontend URL: `https://groww-mf-saathi.vercel.app`

---

## 🔄 Rollback Procedures

### Frontend Rollback (Vercel)

1. Go to **Deployments** tab
2. Find the previous stable deployment
3. Click **"Redeploy"** on that deployment
4. Vercel will rebuild and deploy the previous version

### Backend Rollback (Railway)

1. Go to **Deployments** tab
2. Find the previous stable deployment
3. Click **"Redeploy"** on that deployment
4. Railway will rebuild and deploy the previous version

### Data Rollback (GitHub)

If the daily data refresh introduces bad data:

1. Go to GitHub **Actions** tab
2. Find the failed `Daily Data Refresh` run
3. Check the commit message to identify the bad data
4. Revert the commit:
   ```bash
   git revert <commit-hash>
   git push
   ```
5. The next scheduled run will use the reverted data

---

## 🔧 Troubleshooting

### Backend Issues

| Issue | Solution |
|---|---|
| `GROQ_API_KEY` not found | Add to Railway **Variables** |
| Model download fails | Ensure `HF_HUB_OFFLINE=1` is set; model should be cached |
| Port binding error | Railway assigns `$PORT` dynamically; use it in start command |
| CORS errors from frontend | Ensure backend has `CORSMiddleware` enabled (already in code) |

### Frontend Issues

| Issue | Solution |
|---|---|
| `VITE_API_BASE_URL` undefined | Add to Vercel **Environment Variables** |
| API calls fail with 404 | Verify backend URL is correct and backend is running |
| Build fails | Check `npm run build` works locally first |
| Blank page on load | Check browser console for errors; verify API connectivity |

### Data Pipeline Issues

| Issue | Solution |
|---|---|
| GitHub Actions fails | Check `GROQ_API_KEY` secret is set; view workflow logs |
| Playwright scraping times out | Increase timeout in `scheduler.py` or check Groww site status |
| FAISS index not updating | Verify `git push` succeeds in workflow; check commit history |

---

## 📈 Scaling Considerations

### Current Limits

- **Frontend:** Vercel free tier supports ~100k requests/month
- **Backend:** Railway free tier provides 5GB/month bandwidth
- **Data:** FAISS index with 843 chunks (~50MB)

### When to Scale

- **Frontend:** If traffic exceeds 100k requests/month, upgrade Vercel plan
- **Backend:** If bandwidth exceeds 5GB/month, upgrade Railway plan
- **Data:** If chunks exceed 10k, consider sharding FAISS index or using PostgreSQL

### Upgrade Path

1. **Vercel:** Upgrade to Pro ($20/month) for unlimited bandwidth
2. **Railway:** Upgrade to paid plan ($5-50/month depending on usage)
3. **Database:** Add PostgreSQL on Railway for persistent storage (optional)

---

## 📝 Deployment Checklist (Final)

Before going live:

- [ ] Backend deployed on Railway and health check passes
- [ ] Frontend deployed on Vercel and loads without errors
- [ ] `VITE_API_BASE_URL` points to correct Railway backend
- [ ] `GROQ_API_KEY` is set in both Railway and GitHub Actions
- [ ] End-to-end test passes (query → response with citation)
- [ ] GitHub Actions workflow runs successfully
- [ ] Monitoring is set up (optional but recommended)
- [ ] Custom domain is configured (optional)
- [ ] Team has access to deployment dashboards

---

## 🎯 Next Steps

1. **Day 1:** Deploy backend on Railway, test health endpoint
2. **Day 2:** Deploy frontend on Vercel, test end-to-end
3. **Day 3:** Monitor logs, verify data refresh runs successfully
4. **Day 4+:** Set up monitoring, configure custom domain, optimize performance

---

## 📞 Support & Documentation

- **Vercel Docs:** https://vercel.com/docs
- **Railway Docs:** https://docs.railway.app
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **Vite Docs:** https://vitejs.dev
- **Groq API Docs:** https://console.groq.com/docs

---

**Last Updated:** May 10, 2026  
**Status:** Ready for Deployment
