# 🎨 Vercel Frontend Deployment Guide

## Overview

This guide will walk you through deploying the Groww MF Saathi frontend on Vercel.

---

## Prerequisites

1. **Vercel Account** - Sign up at https://vercel.com
2. **GitHub Account** - Already have it ✅
3. **Railway Backend URL** - From backend deployment (e.g., `https://groww-mf-backend-prod.up.railway.app`)

---

## Step 1: Create Vercel Project

### 1.1 Go to Vercel Dashboard

1. Go to https://vercel.com
2. Click **"Add New"** → **"Project"**
3. Click **"Import Git Repository"**

### 1.2 Authorize Vercel

1. Click **"Authorize GitHub"** (if first time)
2. Grant Vercel access to your GitHub account
3. Select the `Groww-Mutual-Fund-FAQ-Assistant` repository

### 1.3 Import Project

1. Click **"Import"**
2. Vercel will scan the repository

---

## Step 2: Configure Build Settings

### 2.1 Set Root Directory

1. In the import dialog, find **"Root Directory"** field
2. Set it to: `src/phase4_ui/frontend`

### 2.2 Set Build Command

1. Find **"Build Command"** field
2. Set it to: `npm run build`

### 2.3 Set Output Directory

1. Find **"Output Directory"** field
2. Set it to: `dist`

### 2.4 Set Install Command

1. Find **"Install Command"** field
2. Set it to: `npm install`

---

## Step 3: Add Environment Variables

### 3.1 Add VITE_API_BASE_URL

1. In the import dialog, find **"Environment Variables"** section
2. Click **"Add"** to add a new variable
3. Set:
   - **Name:** `VITE_API_BASE_URL`
   - **Value:** `https://YOUR_RAILWAY_URL/api`
   
   Replace `YOUR_RAILWAY_URL` with your actual Railway backend URL
   
   Example: `https://groww-mf-backend-prod.up.railway.app/api`

---

## Step 4: Deploy

### 4.1 Click Deploy

1. Click **"Deploy"** button
2. Vercel will start building the project
3. Wait 2-3 minutes for build to complete

### 4.2 Monitor Build

1. Watch the build progress in the dashboard
2. Check logs for any errors
3. Once complete, Vercel will provide a URL

---

## Step 5: Verify Deployment

### 5.1 Test Frontend

1. Open the Vercel URL in your browser
2. Verify the frontend loads correctly
3. Check that:
   - Sidebar is visible
   - Groww logo appears
   - User info shows (Asha, ashabharathy@gmail.com)
   - Theme toggle works
   - Suggestions appear

### 5.2 Test Query

1. Click on a suggestion or type a query
2. Verify the query is sent to the backend
3. Verify the response appears with source link
4. Check browser console for any errors

### 5.3 Test Theme Toggle

1. Click **Settings** in sidebar
2. Toggle between Dark and Light theme
3. Verify theme changes

### 5.4 Test Dual Chat

1. Click **"Dual Chat"** in sidebar
2. Verify two chat panels appear
3. Send queries in both panels

---

## Environment Variables

### Frontend (Vercel)

| Variable | Value | Notes |
|----------|-------|-------|
| `VITE_API_BASE_URL` | `https://YOUR_RAILWAY_URL/api` | Backend API endpoint |

### Local Development

Create `.env.local` in `src/phase4_ui/frontend/`:

```
VITE_API_BASE_URL=http://localhost:8000/api
```

---

## Configuration Files

### vercel.json

Located at project root, specifies:
- Build command
- Output directory
- Framework (Vite)
- Environment variables

### .env.example

Located in `src/phase4_ui/frontend/`, shows example environment variables.

### .env.local

Located in `src/phase4_ui/frontend/`, contains local development variables (not committed).

---

## Troubleshooting

### Build Failed

**Check the logs:**
1. Go to Vercel dashboard
2. Click on your project
3. View **Deployments** tab
4. Click on failed deployment
5. Check **Build Logs**

**Common issues:**
- Root directory not set correctly
- Build command incorrect
- Missing dependencies

### API Calls Fail

**Solution:**
1. Verify `VITE_API_BASE_URL` is set correctly
2. Verify Railway backend is running
3. Check browser console for CORS errors
4. Verify backend URL is accessible

### Blank Page

**Solution:**
1. Check browser console for errors
2. Verify environment variables are set
3. Check network tab for failed requests
4. Verify API endpoint is correct

### CORS Errors

**Solution:**
- Backend already has CORS enabled
- Verify backend URL is correct
- Check that backend is running
- Verify frontend is using correct API URL

---

## Post-Deployment

### Custom Domain (Optional)

1. Go to **Settings → Domains**
2. Add your custom domain
3. Follow DNS configuration instructions

### Analytics (Optional)

1. Go to **Analytics** tab
2. Monitor page load times
3. Track traffic

### Monitoring (Optional)

1. Set up error tracking
2. Monitor deployment health
3. Configure alerts

---

## Redeployment

### Automatic Redeployment

Vercel automatically redeploys when you push to `master` branch.

### Manual Redeployment

1. Go to **Deployments** tab
2. Click on a previous deployment
3. Click **"Redeploy"**

### Rollback

1. Go to **Deployments** tab
2. Find a previous stable deployment
3. Click **"Redeploy"**

---

## Environment Variables Reference

### Development

```
VITE_API_BASE_URL=http://localhost:8000/api
```

### Production (Vercel)

```
VITE_API_BASE_URL=https://groww-mf-backend-prod.up.railway.app/api
```

---

## Useful Links

| Resource | URL |
|----------|-----|
| Vercel Dashboard | https://vercel.com/dashboard |
| Vercel Docs | https://vercel.com/docs |
| Vite Docs | https://vitejs.dev |
| React Docs | https://react.dev |

---

## Deployment Checklist

- [ ] Vercel account created
- [ ] GitHub repository connected
- [ ] Root directory set to `src/phase4_ui/frontend`
- [ ] Build command set to `npm run build`
- [ ] Output directory set to `dist`
- [ ] Install command set to `npm install`
- [ ] `VITE_API_BASE_URL` environment variable added
- [ ] Deployment completed successfully
- [ ] Frontend loads without errors
- [ ] Query test successful
- [ ] Theme toggle works
- [ ] Dual chat mode works

---

## Summary

| Step | Action | Time |
|------|--------|------|
| 1 | Create Vercel project | 2 min |
| 2 | Configure build settings | 2 min |
| 3 | Add environment variables | 1 min |
| 4 | Deploy | 3 min |
| 5 | Verify | 2 min |
| **Total** | | **10 min** |

---

**Status:** Ready for Deployment  
**Difficulty:** Easy ⭐⭐☆☆☆  
**Time Required:** 10 minutes  
**Last Updated:** May 10, 2026
