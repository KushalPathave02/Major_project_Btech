# Frontend Deployment Guide - FinTrack

## 📋 Overview
This guide will help you deploy your React frontend to **Render** (Free hosting platform).

---

## 🚀 Option 1: Deploy to Render (Recommended - Free)

### Step 1: Prepare Your Project

1. **Update `.env` file in `client/` folder**
   ```env
   REACT_APP_API_URL=https://your-backend-url.onrender.com
   ```
   Replace with your actual backend URL from Render.

2. **Create `.gitignore` if not exists** (Already done)
   Make sure these are in `.gitignore`:
   ```
   node_modules/
   build/
   .env
   ```

3. **Test build locally**
   ```bash
   cd client
   npm run build
   ```
   This should create a `build/` folder without errors.

### Step 2: Push to GitHub

1. **Make sure all changes are committed**
   ```bash
   cd /Users/kushal/Downloads/Major_project-main
   git add .
   git commit -m "Prepare frontend for deployment"
   git push origin main
   ```

### Step 3: Deploy on Render

1. **Go to Render Dashboard**
   - Visit: https://render.com
   - Sign in with GitHub

2. **Create New Static Site**
   - Click "New +" button
   - Select "Static Site"

3. **Connect Your Repository**
   - Select your GitHub repository: `Major_project_Btech`
   - Click "Connect"

4. **Configure Build Settings**
   ```
   Name: fintrack-frontend (or any name you want)
   Branch: main
   Root Directory: client
   Build Command: npm install && npm run build
   Publish Directory: build
   ```

5. **Add Environment Variables**
   - Click "Advanced"
   - Add environment variable:
     ```
     Key: REACT_APP_API_URL
     Value: https://your-backend-url.onrender.com
     ```

6. **Deploy**
   - Click "Create Static Site"
   - Wait 3-5 minutes for deployment
   - You'll get a URL like: `https://fintrack-frontend.onrender.com`

### Step 4: Update Backend CORS

After deployment, update your backend `.env` file:
```env
FRONTEND_URL=https://fintrack-frontend.onrender.com
```

Then redeploy your backend on Render.

---

## 🚀 Option 2: Deploy to Netlify (Alternative - Free)

### Step 1: Install Netlify CLI

```bash
npm install -g netlify-cli
```

### Step 2: Build Your Project

```bash
cd client
npm run build
```

### Step 3: Deploy

```bash
netlify deploy --prod
```

Follow the prompts:
- Authorize with GitHub
- Choose "Create & configure a new site"
- Publish directory: `build`

### Step 4: Set Environment Variables

1. Go to Netlify Dashboard
2. Select your site
3. Go to "Site settings" → "Environment variables"
4. Add:
   ```
   REACT_APP_API_URL=https://your-backend-url.onrender.com
   ```

---

## 🚀 Option 3: Deploy to Vercel (Alternative - Free)

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Deploy

```bash
cd client
vercel
```

Follow the prompts:
- Login with GitHub
- Link to existing project or create new
- Set root directory to `client`
- Override build command: `npm run build`
- Override output directory: `build`

### Step 3: Set Environment Variables

```bash
vercel env add REACT_APP_API_URL
```
Enter your backend URL when prompted.

Then redeploy:
```bash
vercel --prod
```

---

## 📝 Quick Deployment Checklist

### Before Deployment:
- [ ] Backend is deployed and working
- [ ] `.env` has correct `REACT_APP_API_URL`
- [ ] All changes committed to GitHub
- [ ] `npm run build` works locally without errors

### After Deployment:
- [ ] Frontend URL is accessible
- [ ] Can see login/register pages
- [ ] Update backend `FRONTEND_URL` in `.env`
- [ ] Test registration and login
- [ ] Test all features (dashboard, transactions, etc.)

---

## 🔧 Common Issues & Solutions

### Issue 1: "API URL not set" Error
**Solution:** 
- Make sure `REACT_APP_API_URL` is set in environment variables
- Redeploy after adding environment variable

### Issue 2: CORS Error
**Solution:**
- Update backend `FRONTEND_URL` to match your deployed frontend URL
- Redeploy backend

### Issue 3: White Screen After Deployment
**Solution:**
- Check browser console for errors
- Verify build completed successfully
- Check if all environment variables are set

### Issue 4: 404 on Page Refresh
**Solution for Render:**
- Add `_redirects` file in `public/` folder:
  ```
  /*    /index.html   200
  ```

**Solution for Netlify:**
- Add `netlify.toml` in `client/` folder:
  ```toml
  [[redirects]]
    from = "/*"
    to = "/index.html"
    status = 200
  ```

---

## 📱 Testing Your Deployment

After deployment, test these features:

1. **Registration**
   - Go to `/register`
   - Create new account
   - Check if verification email is sent

2. **Login**
   - Go to `/login`
   - Login with verified account
   - Should redirect to dashboard

3. **Dashboard**
   - Check if data loads
   - Test currency switcher
   - Test light/dark mode

4. **Transactions**
   - Upload CSV file
   - Check if transactions appear

5. **All Pages**
   - Test navigation
   - Check responsive design on mobile

---

## 🎯 Recommended: Deploy to Render

**Why Render?**
- ✅ Free tier available
- ✅ Automatic deployments from GitHub
- ✅ Easy environment variable management
- ✅ Good performance
- ✅ SSL certificate included
- ✅ Custom domain support

**Deployment Time:** 3-5 minutes

---

## 📞 Need Help?

If you face any issues:

1. **Check Render/Netlify/Vercel logs**
   - Build logs show errors during deployment

2. **Check browser console**
   - F12 → Console tab
   - Look for API errors

3. **Verify environment variables**
   - Make sure `REACT_APP_API_URL` is correct
   - Should start with `https://`

4. **Test backend separately**
   - Visit backend URL in browser
   - Should see "Financial Dashboard API"

---

## 🔄 Redeployment

To redeploy after making changes:

### Render/Netlify/Vercel (Auto-deploy):
```bash
git add .
git commit -m "Your changes"
git push origin main
```
Platform will automatically redeploy.

### Manual Redeploy:
- Go to platform dashboard
- Click "Trigger deploy" or "Redeploy"

---

## 🌐 Custom Domain (Optional)

After deployment, you can add a custom domain:

1. Buy domain from Namecheap/GoDaddy
2. Go to platform settings
3. Add custom domain
4. Update DNS records as instructed
5. Wait for DNS propagation (24-48 hours)

---

## ✅ Final URLs

After deployment, you'll have:

- **Frontend:** `https://fintrack-frontend.onrender.com`
- **Backend:** `https://your-backend.onrender.com`

Update these in:
- Backend `.env` → `FRONTEND_URL`
- Frontend `.env` → `REACT_APP_API_URL`

---

**Happy Deploying! 🚀**
