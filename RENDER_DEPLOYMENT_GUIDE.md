# Render Deployment Guide

This guide will help you deploy your Financial Dashboard application on Render with both backend (Flask API) and frontend (React) services.

## Prerequisites

1. A [Render account](https://render.com) (free tier available)
2. Your code pushed to a GitHub/GitLab repository
3. MongoDB Atlas account (for the database) or existing MongoDB connection string

## Deployment Options

You have **two options** for deploying on Render:

### Option 1: Using render.yaml (Recommended - Infrastructure as Code)

This method uses the `render.yaml` file to define both services automatically.

#### Steps:

1. **Push your code to GitHub/GitLab**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Connect to Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click **"New +"** → **"Blueprint"**
   - Connect your GitHub/GitLab account and select your repository
   - Render will detect the `render.yaml` file automatically

3. **Configure Environment Variables**
   
   You'll need to set these environment variables in Render:

   **For Backend Service (financial-dashboard-api):**
   - `MONGO_URI` - Your MongoDB connection string (e.g., from MongoDB Atlas)
   - `SECRET_KEY` - A strong secret key for JWT (generate a random string)
   - `EMAIL_USER` - Your Gmail address (for email functionality)
   - `EMAIL_PASS` - Your Gmail app password (not regular password)
   - `MAIL_DEFAULT_SENDER` - Same as EMAIL_USER
   - `GEMINI_API_KEY` - Your Google Gemini API key (if using AI features)
   - `FRONTEND_URL` - Will be: `https://financial-dashboard-client.onrender.com` (or your custom domain)

   **For Frontend Service (financial-dashboard-client):**
   - `REACT_APP_API_URL` - Will be: `https://financial-dashboard-api.onrender.com` (your backend URL)

4. **Deploy**
   - Click "Apply" to create both services
   - Render will build and deploy both services automatically
   - Wait for the builds to complete (this may take 5-10 minutes)

---

### Option 2: Manual Deployment (Two Separate Services)

If you prefer to set up services manually:

#### Backend Deployment

1. **Create Web Service**
   - Go to Render Dashboard
   - Click **"New +"** → **"Web Service"**
   - Connect your repository
   - Configure:
     - **Name:** `financial-dashboard-api`
     - **Runtime:** `Python 3`
     - **Build Command:** `cd flask_server && pip install -r requirements.txt`
     - **Start Command:** `cd flask_server && gunicorn app:app`
     - **Plan:** Free (or paid as needed)

2. **Set Environment Variables** (same as above)

3. **Deploy** - Click "Create Web Service"

#### Frontend Deployment

1. **Create Static Site**
   - Click **"New +"** → **"Static Site"**
   - Connect the same repository
   - Configure:
     - **Name:** `financial-dashboard-client`
     - **Build Command:** `cd client && npm install && npm run build`
     - **Publish Directory:** `client/build`

2. **Set Environment Variables**
   - `REACT_APP_API_URL` - Your backend URL (from step 1)

3. **Deploy** - Click "Create Static Site"

---

## Post-Deployment Configuration

### 1. Update API URL in Frontend

If you didn't use environment variables, update the API URL in your React app:
```typescript
// In your API config file (e.g., src/config/api.ts or similar)
const API_URL = process.env.REACT_APP_API_URL || 'https://financial-dashboard-api.onrender.com';
```

### 2. Set Up MongoDB Atlas (if not done already)

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free cluster
3. Create a database user
4. Whitelist IP address: `0.0.0.0/0` (allow access from anywhere for Render)
5. Get your connection string and add it to `MONGO_URI` in Render

### 3. Gmail App Password Setup

To enable email functionality:
1. Go to your Google Account → Security
2. Enable 2-Step Verification
3. Go to "App passwords"
4. Create a new app password
5. Use this password for `EMAIL_PASS` environment variable

### 4. Get Google Gemini API Key (Optional)

If using AI features:
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an API key
3. Add it to `GEMINI_API_KEY` environment variable

---

## Important Notes

### Free Tier Limitations

- **Render Free Tier** spins down after 15 minutes of inactivity
- First request after spin-down may take 30-60 seconds (cold start)
- Consider upgrading to paid tier for production use

### CORS Configuration

The backend is already configured to accept requests from Render URLs. The `FRONTEND_URL` environment variable ensures proper CORS settings.

### Database Persistence

Make sure you're using MongoDB Atlas or another cloud MongoDB instance - **do not use a local MongoDB connection** as Render services are ephemeral.

### File Uploads

The `uploads/` folder is ephemeral on Render free tier. For production, consider using:
- AWS S3
- Cloudinary
- Render Persistent Disks (paid feature)

---

## Troubleshooting

### Backend Not Starting
- Check build logs in Render dashboard
- Verify all environment variables are set
- Ensure `requirements.txt` is up to date

### Frontend Can't Connect to Backend
- Verify `REACT_APP_API_URL` is set correctly
- Check backend service is running
- Check browser console for CORS errors

### Database Connection Issues
- Verify `MONGO_URI` is correct
- Check MongoDB Atlas IP whitelist includes `0.0.0.0/0`
- Verify database user has correct permissions

### Email Not Working
- Verify Gmail app password (not regular password)
- Check `EMAIL_USER` and `EMAIL_PASS` are set
- Ensure 2-Step Verification is enabled on Gmail

---

## Custom Domains (Optional)

To use custom domains:
1. Go to your service in Render dashboard
2. Click "Settings" → "Custom Domain"
3. Add your domain and follow DNS configuration instructions

---

## Monitoring & Logs

- View logs in Render dashboard under each service
- Set up log drains for production monitoring
- Use Render's metrics to monitor performance

---

## Cost Optimization

**Free Tier:**
- Backend: 750 hours/month free
- Frontend: Unlimited bandwidth for static sites
- Database: MongoDB Atlas free tier (512MB)

**Upgrading:**
- Consider paid tier ($7/month) for always-on services
- Use persistent disk for file uploads
- Set up autoscaling for high traffic

---

## Next Steps

1. ✅ Deploy both services
2. ✅ Configure environment variables
3. ✅ Test all functionality
4. 🔄 Set up monitoring
5. 🔄 Configure custom domains (optional)
6. 🔄 Set up CI/CD (Render auto-deploys from Git)

---

## Support

For issues:
- Check [Render Documentation](https://render.com/docs)
- Review service logs in Render dashboard
- Check your repository's GitHub Actions (if configured)

---

**Your services will be available at:**
- Backend: `https://financial-dashboard-api.onrender.com`
- Frontend: `https://financial-dashboard-client.onrender.com`

(URLs may vary based on your service names)
