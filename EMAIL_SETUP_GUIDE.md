# Email Verification Setup Guide for FinTrack

## Overview
Your FinTrack application now sends beautiful HTML verification emails to users when they register. Follow this guide to configure email sending.

## What's Been Updated

### 1. **Email Service** (`flask_server/email_service.py`)
- Now sends professional HTML emails with FinTrack branding
- Includes a styled verification button
- Shows verification link in the email
- Mobile-responsive design

### 2. **Verification Flow**
- User registers → Receives verification email
- User clicks "Verify Email Now" button in email
- User is redirected to verification page
- After verification, user can login

## Email Configuration Steps

### Option 1: Gmail (Recommended for Testing)

1. **Enable 2-Step Verification on your Gmail account**
   - Go to: https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Name it "FinTrack"
   - Copy the 16-character password

3. **Update `.env` file in `flask_server/` folder**
   ```env
   EMAIL_USER=your-email@gmail.com
   EMAIL_PASS=your-16-character-app-password
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   ```

4. **Set Public Base URL** (Important!)
   ```env
   APP_PUBLIC_BASE_URL=http://localhost:5000
   ```
   Or for production:
   ```env
   APP_PUBLIC_BASE_URL=https://your-backend-url.com
   ```

### Option 2: Other Email Providers

#### SendGrid
```env
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
EMAIL_USER=apikey
EMAIL_PASS=your-sendgrid-api-key
```

#### Outlook/Hotmail
```env
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
EMAIL_USER=your-email@outlook.com
EMAIL_PASS=your-password
```

## Testing Email Verification

### 1. Start the Flask Server
```bash
cd flask_server
python app.py
```

### 2. Start the React Client
```bash
cd client
npm start
```

### 3. Register a New User
- Go to: http://localhost:3000/register
- Fill in the registration form with a **real email address**
- Click "Register"

### 4. Check Your Email
- Open your email inbox
- Look for email from FinTrack
- Click the "Verify Email Now" button

### 5. Verify and Login
- You'll be redirected to the verification success page
- Click "Go to Login" or wait for auto-redirect
- Login with your credentials

## Email Template Preview

The email includes:
- 📧 Email icon
- **FinTrack** logo/branding
- Welcome message with user's name
- Large "Verify Email Now" button (purple gradient)
- Alternative verification link (copy-paste option)
- 1-hour expiry notice
- Professional footer

## Troubleshooting

### Email Not Sending
1. **Check .env configuration**
   - Verify EMAIL_USER and EMAIL_PASS are correct
   - Make sure no extra spaces in credentials

2. **Gmail App Password Issues**
   - Ensure 2-Step Verification is enabled
   - Generate a new App Password
   - Use the password without spaces

3. **Check Flask Server Logs**
   - Look for email-related errors in terminal
   - Error messages will indicate the issue

### Verification Link Not Working
1. **Check APP_PUBLIC_BASE_URL**
   - Must match your backend URL
   - For local: `http://localhost:5000`
   - For production: Your deployed backend URL

2. **Link Expired**
   - Links expire after 1 hour
   - User needs to register again

### User Can't Login After Registration
- User must verify email first
- Check if verification was successful
- Look for "is_verified: true" in MongoDB user document

## Security Notes

⚠️ **Important Security Practices:**

1. **Never commit `.env` file to Git**
   - Already in `.gitignore`
   - Contains sensitive credentials

2. **Use App Passwords, not main password**
   - More secure
   - Can be revoked independently

3. **Verification links expire in 1 hour**
   - Prevents old links from being used
   - Users must register again if expired

## Production Deployment

For production (Render, Heroku, etc.):

1. **Set environment variables in hosting platform**
   - Don't rely on .env file
   - Use platform's environment variable settings

2. **Update APP_PUBLIC_BASE_URL**
   ```env
   APP_PUBLIC_BASE_URL=https://your-backend.onrender.com
   ```

3. **Update FRONTEND_URL**
   ```env
   FRONTEND_URL=https://your-frontend.onrender.com
   ```

## Email Preview

When users receive the email, they'll see:
- Beautiful gradient background (purple)
- White card with rounded corners
- FinTrack branding
- Clear call-to-action button
- Alternative link for manual verification
- Professional design matching your app

---

**Need Help?** 
- Check Flask server logs for errors
- Verify all environment variables are set
- Test with a real email address (not temporary email services)
