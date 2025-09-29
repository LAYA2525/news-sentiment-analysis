# 🚀 GitHub Setup & Deployment Guide

## 📋 Prerequisites Checklist

Before pushing to GitHub and deploying, make sure you have:

- [ ] Git installed on your computer
- [ ] GitHub account created
- [ ] NewsAPI.org API key
- [ ] All project files ready (README, requirements.txt, etc.)

## 🔧 Step 1: Prepare Your Project

### 1.1 Remove Sensitive Data
Make sure your actual API key is NOT in any files that will be committed:

```bash
# Check that .env is in .gitignore
grep -q "\.env" .gitignore && echo "✅ .env is ignored" || echo "❌ Add .env to .gitignore"
```

### 1.2 Test Locally
Ensure everything works on your machine:

```bash
# Install dependencies
pip install -r requirements.txt

# Train model
python train_model_simple.py

# Test dashboard (should open in browser)
streamlit run app_streamlit.py
```

## 📂 Step 2: Initialize Git Repository

Open PowerShell/Command Prompt in your project directory:

```bash
# Navigate to your project
cd "c:\Users\layak\OneDrive\Documents\BIG DATA\PROJECT1\news-sentiment"

# Initialize Git repository
git init

# Add all files
git add .

# Make first commit
git commit -m "Initial commit: News Sentiment Analysis System"
```

## 🌐 Step 3: Create GitHub Repository

### 3.1 On GitHub.com:
1. Go to [github.com](https://github.com)
2. Click "+" → "New repository"
3. Repository name: `news-sentiment-analysis`
4. Description: `Real-time news sentiment analysis with ML and Streamlit dashboard`
5. Set to **Public** (required for free Streamlit Cloud)
6. ❌ **Don't** initialize with README (you already have one)
7. Click "Create repository"

### 3.2 Connect Local to GitHub:
```bash
# Add remote origin (replace 'yourusername' with your GitHub username)
git remote add origin https://github.com/yourusername/news-sentiment-analysis.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## 🎯 Step 4: Deploy to Streamlit Cloud (Recommended - FREE)

### 4.1 Setup Streamlit Cloud:
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `yourusername/news-sentiment-analysis`
5. Branch: `main`
6. Main file path: `app_streamlit.py`
7. Click "Deploy!"

### 4.2 Add Secrets (IMPORTANT):
1. In Streamlit Cloud dashboard, click your app
2. Click "⚙️ Settings" → "Secrets"
3. Add your secrets in TOML format:
   ```toml
   NEWS_API_KEY = "your_actual_api_key_here"
   POLL_INTERVAL_SECONDS = "30"
   NEWS_QUERY = "technology"
   PAGE_SIZE = "10"
   ```
4. Click "Save"

### 4.3 Your App is Live! 🎉
Your app will be available at: `https://yourusername-news-sentiment-analysis-app-streamlit-xyz123.streamlit.app`

## 🔄 Step 5: Alternative Deployment - Heroku

### 5.1 Install Heroku CLI:
Download from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)

### 5.2 Deploy to Heroku:
```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-news-sentiment-app

# Set environment variables
heroku config:set NEWS_API_KEY=your_actual_api_key_here
heroku config:set POLL_INTERVAL_SECONDS=30
heroku config:set NEWS_QUERY=technology
heroku config:set PAGE_SIZE=10

# Deploy
git push heroku main
```

## 🔧 Step 6: Update and Maintain

### 6.1 Making Changes:
```bash
# Make your changes to files
# Then commit and push:
git add .
git commit -m "Description of changes"
git push origin main
```

### 6.2 Streamlit Cloud Auto-Deploy:
- Streamlit Cloud automatically redeploys when you push to GitHub
- Check deployment status in Streamlit Cloud dashboard

## 🛠️ Troubleshooting

### Common Issues:

#### "Module not found" errors:
- Check `requirements.txt` has all dependencies
- Redeploy after updating requirements

#### "API key not found":
- Verify secrets are set correctly in Streamlit Cloud
- Check environment variable names match your code

#### App won't start:
- Check logs in Streamlit Cloud dashboard
- Ensure `app_streamlit.py` is the correct main file

#### No data showing:
- For deployment, you might need to modify the app to work without the background services
- Consider creating a demo mode with sample data

## 🔐 Security Best Practices

1. **Never commit API keys** to GitHub
2. **Use environment variables** for all sensitive data
3. **Keep .env in .gitignore**
4. **Use secrets management** in deployment platforms
5. **Regular security updates** of dependencies

## 📈 Next Steps

After successful deployment:

1. **Share your app** with the world! 🌍
2. **Add to your portfolio/resume** 📄
3. **Collect user feedback** 💬
4. **Monitor usage and performance** 📊
5. **Plan future enhancements** 🚀

## 🎯 Demo App Structure for Deployment

Since the full real-time system needs multiple services, consider creating a simplified demo version for deployment:

```python
# demo_app.py - Simplified version for deployment
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Load or generate demo data
def load_demo_data():
    # Use sample predictions instead of real-time data
    # This ensures the app works without background services
    pass
```

## 📞 Support

If you encounter issues:
1. Check the GitHub Issues page
2. Review Streamlit documentation
3. Check deployment platform docs
4. Contact the maintainer

---

🎉 **Congratulations! Your news sentiment analysis system is now live and accessible to the world!** 🎉