# FinTrack - Quick Start Guide

## 🚀 Local Development Setup

### Prerequisites
- Node.js (v16 or higher)
- Python 3.8+
- MongoDB Atlas account (or local MongoDB)
- Gmail account (for email verification)

---

## 📦 Step 1: Clone & Install

### Backend Setup
```bash
cd flask_server

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd client

# Install dependencies
npm install
```

---

## ⚙️ Step 2: Configure Environment Variables

### Backend Configuration (`flask_server/.env`)
```env
# MongoDB
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/fintrack?retryWrites=true&w=majority

# Security
SECRET_KEY=your-secret-key-here-generate-random-string

# Email (Gmail)
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-gmail-app-password
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587

# URLs
FRONTEND_URL=http://localhost:3000
APP_PUBLIC_BASE_URL=http://localhost:5000

# Optional: AI Features
GEMINI_API_KEY=your-gemini-api-key
```

### Frontend Configuration (`client/.env`)
```env
REACT_APP_API_URL=http://localhost:5000
```

---

## 🔑 Step 3: Setup Gmail for Email Verification

1. **Enable 2-Step Verification**
   - Go to: https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Name it "FinTrack"
   - Copy the 16-character password
   - Add to `EMAIL_PASS` in `.env`

---

## ▶️ Step 4: Run the Application

### Terminal 1 - Backend
```bash
cd flask_server
source venv/bin/activate  # On Mac/Linux
python app.py
```
Backend will run on: http://localhost:5000

### Terminal 2 - Frontend
```bash
cd client
npm start
```
Frontend will run on: http://localhost:3000

---

## 🧪 Step 5: Test the Application

1. **Open Browser**
   - Go to: http://localhost:3000

2. **Register New User**
   - Click "Register"
   - Fill in details with **real email**
   - Submit

3. **Verify Email**
   - Check your email inbox
   - Click "Verify Email Now" button
   - Or copy verification link

4. **Login**
   - Go to login page
   - Enter credentials
   - Access dashboard

5. **Test Features**
   - Upload CSV transactions
   - View dashboard analytics
   - Test currency switcher
   - Toggle light/dark mode

---

## 📁 Project Structure

```
Major_project-main/
├── flask_server/           # Backend (Python Flask)
│   ├── app.py             # Main application
│   ├── routes/            # API routes
│   ├── models/            # Data models
│   ├── email_service.py   # Email functionality
│   └── .env               # Backend config
│
├── client/                # Frontend (React TypeScript)
│   ├── src/
│   │   ├── pages/        # Page components
│   │   ├── components/   # Reusable components
│   │   ├── theme.ts      # Theme configuration
│   │   └── App.tsx       # Main app component
│   ├── public/           # Static files
│   └── .env              # Frontend config
│
└── README.md             # Project documentation
```

---

## 🐛 Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

**MongoDB connection failed:**
- Check MONGO_URI in `.env`
- Verify MongoDB Atlas IP whitelist (allow 0.0.0.0/0)
- Check network connection

**Email not sending:**
- Verify Gmail App Password
- Check EMAIL_USER and EMAIL_PASS in `.env`
- Ensure 2-Step Verification is enabled

### Frontend Issues

**Port 3000 already in use:**
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

**API URL not set error:**
- Check `REACT_APP_API_URL` in `client/.env`
- Restart frontend after changing .env

**CORS error:**
- Check `FRONTEND_URL` in backend `.env`
- Restart backend after changing .env

---

## 📊 Sample CSV Format for Transactions

Create a CSV file with this format:

```csv
date,amount,category,status,description
2024-01-15,5000,salary,completed,Monthly salary
2024-01-16,-1200,rent,completed,House rent
2024-01-17,-500,groceries,completed,Weekly groceries
2024-01-18,-200,transport,completed,Fuel
2024-01-20,2000,freelance,completed,Project payment
```

---

## 🔐 Security Best Practices

1. **Never commit `.env` files**
   - Already in `.gitignore`
   - Contains sensitive data

2. **Use strong SECRET_KEY**
   - Generate random string
   - At least 32 characters

3. **Use App Passwords**
   - Not your main Gmail password
   - More secure and revocable

4. **Keep dependencies updated**
   ```bash
   # Backend
   pip list --outdated
   
   # Frontend
   npm outdated
   ```

---

## 🚀 Deployment

See detailed deployment guides:
- **Frontend:** `FRONTEND_DEPLOYMENT_GUIDE.md`
- **Backend:** Deploy to Render/Heroku
- **Email Setup:** `EMAIL_SETUP_GUIDE.md`

---

## 📚 Available Features

✅ User Authentication (Register/Login)
✅ Email Verification
✅ Dashboard with Analytics
✅ Transaction Management
✅ CSV Upload
✅ Currency Conversion (INR/USD/EUR)
✅ Light/Dark Mode
✅ Wallet Management
✅ AI Chatbot (with Gemini API)
✅ Expense Forecasting
✅ Profile Management

---

## 🆘 Need Help?

1. **Check Logs**
   - Backend: Terminal running Flask
   - Frontend: Browser Console (F12)

2. **Verify Configuration**
   - All `.env` variables set
   - MongoDB connection working
   - Email credentials correct

3. **Test Individually**
   - Test backend: http://localhost:5000
   - Test frontend: http://localhost:3000

---

## 📝 Development Tips

1. **Hot Reload**
   - Frontend auto-reloads on save
   - Backend needs manual restart

2. **Debug Mode**
   - Backend: Set `debug=True` in `app.py`
   - Frontend: Check browser console

3. **Database**
   - Use MongoDB Compass to view data
   - Connect with MONGO_URI

---

**Happy Coding! 💻**
