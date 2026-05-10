# 🚀 DEPLOY NOW - Action Plan

## Your Backend is Ready to Deploy! 🎉

Everything is prepared. Follow these exact steps to deploy your backend on Railway in **15 minutes**.

---

## ⏱️ Timeline

- **Step 1-2:** 2 minutes (Create Railway account & project)
- **Step 3-4:** 3 minutes (Configure commands & variables)
- **Step 5:** 10 minutes (Deploy & wait)
- **Step 6:** 2 minutes (Verify)
- **Total:** ~15 minutes

---

## 🎯 What You Need

1. **Groq API Key** - Get from https://console.groq.com/keys
   - Click "Create API Key"
   - Copy the key (starts with `gsk_` or `sk_`)

2. **Railway Account** - Sign up at https://railway.app
   - Free tier is sufficient

3. **GitHub Account** - Already have it ✅

---

## 📋 Step-by-Step Instructions

### STEP 1: Get Your Groq API Key (2 minutes)

1. Go to https://console.groq.com/keys
2. Click **"Create API Key"** button
3. Copy the key (it will look like: `gsk_...` or `sk_...`)
4. **Save it somewhere safe** - you'll need it in Step 4

---

### STEP 2: Create Railway Project (2 minutes)

1. Go to https://railway.app
2. Click **"Start Free"** (or log in if you have account)
3. Click **"New Project"** button (top right)
4. Select **"Deploy from GitHub repo"**
5. Click **"Configure GitHub App"** (if first time)
6. Authorize Railway to access GitHub
7. Select repository: **`Groww-Mutual-Fund-FAQ-Assistant`**
8. Select branch: **`master`**
9. Click **"Deploy"**

**⏱️ Wait 1-2 minutes for Railway to initialize**

---

### STEP 3: Configure Build Command (1 minute)

1. In Railway dashboard, click on your service
2. Click **"Settings"** tab
3. Find **"Build Command"** field
4. **Clear it** and paste this:

```bash
pip install -r src/phase4_ui/requirements.txt && pip install -r src/phase3_rag/requirements.txt && pip install -r src/phase2_embedding/requirements.txt
```

5. Click **"Save"** or press Enter

---

### STEP 4: Configure Start Command (1 minute)

1. In the same **"Settings"** tab
2. Find **"Start Command"** field
3. **Clear it** and paste this:

```bash
python -m uvicorn src.phase4_ui.api:app --host 0.0.0.0 --port $PORT
```

4. Click **"Save"** or press Enter

---

### STEP 5: Add Environment Variables (2 minutes)

1. Click **"Variables"** tab
2. Click **"Add Variable"** button
3. Add **Variable 1:**
   - **Key:** `GROQ_API_KEY`
   - **Value:** `sk-...` (paste your Groq API key from Step 1)
   - Click **"Add"**

4. Click **"Add Variable"** again
5. Add **Variable 2:**
   - **Key:** `HF_HUB_OFFLINE`
   - **Value:** `1`
   - Click **"Add"**

6. Click **"Add Variable"** again
7. Add **Variable 3:**
   - **Key:** `TRANSFORMERS_OFFLINE`
   - **Value:** `1`
   - Click **"Add"**

**✅ All three variables added**

---

### STEP 6: Enable Public Networking (1 minute)

1. Click **"Networking"** tab
2. Click **"Generate Domain"** button
3. Copy the generated URL (e.g., `https://groww-mutual-fund-faq-assistant-production.up.railway.app`)
4. **Save this URL** - you'll need it for frontend deployment

**Example:**
```
https://groww-mf-backend-prod.up.railway.app
```

---

### STEP 7: Deploy (10 minutes)

1. Go to **"Deployments"** tab
2. Click **"Deploy"** button
3. Watch the logs for build progress

**You'll see:**
- ✅ `Building...`
- ✅ `Installing dependencies...`
- ✅ `Starting server...`
- ✅ `Listening on 0.0.0.0:PORT`

**⏱️ Wait 5-10 minutes for deployment to complete**

---

### STEP 8: Verify Deployment (2 minutes)

#### Test 1: Health Check

Open your browser and go to:
```
https://groww-mutual-fund-faq-assistant-production.up.railway.app/api/health
```

**Replace `YOUR_RAILWAY_URL` with your actual URL from Step 6**

Example:
```
https://groww-mutual-fund-faq-assistant-production.up.railway.app/api/health
```

You should see:
```json
{"status":"healthy","engine_ready":true}
```

#### Test 2: Query Test

Open your browser and go to:
```
https://groww-mutual-fund-faq-assistant-production.up.railway.app/api/query?query=What%20is%20the%20expense%20ratio%20of%20Tata%20ELSS%20Fund?
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

## 🎨 Next: Deploy Frontend on Vercel (Optional)

Once backend is deployed, you can deploy the frontend:

1. Go to https://vercel.com
2. Click **"Add New"** → **"Project"**
3. Select **"Import Git Repository"**
4. Select `Groww-Mutual-Fund-FAQ-Assistant`
5. Set **Root Directory** to `src/phase4_ui/frontend`
6. Add environment variable:
   - **Key:** `VITE_API_BASE_URL`
   - **Value:** `https://groww-mutual-fund-faq-assistant-production.up.railway.app/api`
7. Click **"Deploy"**

---

## 🆘 Troubleshooting

### ❌ Deployment Failed

**Check the logs:**
1. Go to **Deployments** tab
2. Click on the failed deployment
3. View **Logs** to see the error

**Common fixes:**
- Verify `GROQ_API_KEY` is set correctly (copy-paste carefully)
- Verify Build Command is exactly as shown above
- Verify Start Command is exactly as shown above

### ❌ Health Check Returns Error

**Solution:**
1. Check Railway logs for errors
2. Verify all three environment variables are set
3. Redeploy the service

### ❌ "Module not found" Error

**Solution:**
1. Verify Build Command includes all three requirements files
2. Check that the repository structure is correct
3. Redeploy

---

## 📞 Need Help?

- **Railway Docs:** https://docs.railway.app
- **Groq Console:** https://console.groq.com
- **GitHub Repo:** https://github.com/Ashabharathy/Groww-Mutual-Fund-FAQ-Assistant

---

## 📝 Checklist

- [ ] Got Groq API key from https://console.groq.com/keys
- [ ] Created Railway account at https://railway.app
- [ ] Created new Railway project from GitHub
- [ ] Set Build Command
- [ ] Set Start Command
- [ ] Added GROQ_API_KEY variable
- [ ] Added HF_HUB_OFFLINE variable
- [ ] Added TRANSFORMERS_OFFLINE variable
- [ ] Generated public domain
- [ ] Clicked Deploy
- [ ] Waited for deployment to complete
- [ ] Tested health endpoint (/api/health)
- [ ] Tested query endpoint (/api/query)
- [ ] Saved Railway URL for frontend deployment

---

## 🎯 Success Criteria

✅ Health endpoint returns `{"status":"healthy","engine_ready":true}`  
✅ Query endpoint returns correct responses  
✅ No errors in Railway logs  
✅ Backend is accessible from the internet  

---

## 🚀 You're Ready!

Everything is prepared. Just follow the steps above and your backend will be live in 15 minutes!

**Start with STEP 1 now!** 👆

---

**Status:** Ready to Deploy  
**Difficulty:** Easy ⭐⭐☆☆☆  
**Time Required:** 15 minutes  
**Last Updated:** May 10, 2026

