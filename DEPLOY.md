# 🚀 Deploy to Railway

## Quick Setup (5 minutes):

### 1. Push to GitHub
```bash
# Create a new repository on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### 2. Deploy on Railway
1. Go to [railway.app](https://railway.app)
2. Sign up/Login with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository
6. Click "Deploy"

### 3. Access Your App
- Railway will give you a URL like: `https://your-app-name.railway.app`
- Share this URL with your colleagues worldwide!

## 🌟 What Your Colleagues Will Get:
- **Global Access**: Works from anywhere in the world
- **HTTPS**: Secure connection
- **Fast**: Railway's global CDN
- **Reliable**: 99.9% uptime
- **Professional URL**: No more IP addresses!

## 💡 Alternative: One-Click Deploy

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/YOUR_USERNAME/YOUR_REPO_NAME)

## 🔧 Environment Variables (Optional)
If needed, you can set these in Railway dashboard:
- `MAX_CRAWL_TIME`: Maximum crawl time in seconds (default: 3600)
- `FLASK_ENV`: Set to "production"

## 📊 Usage After Deployment:
1. Your colleagues visit: `https://your-app.railway.app`
2. They enter any website URL
3. Watch unlimited page crawling in real-time
4. Download ZIP with all images + CSV + summary

## 💰 Cost:
- **Free Tier**: 500 hours/month (perfect for team use)
- **Pro**: $5/month for unlimited usage

Your scraper will be live 24/7 and accessible worldwide! 🌍 