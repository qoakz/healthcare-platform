# 🚀 Healthcare Platform Deployment Guide

## Quick Setup (5 minutes)

### 1. Create GitHub Repository
1. Go to [GitHub.com](https://github.com) and sign in
2. Click **"+"** → **"New repository"**
3. Name: `healthcare-platform`
4. Description: `HIPAA-compliant healthcare platform with patient management, video consultations, and medical records`
5. Make it **Public**
6. **Don't** initialize with README
7. Click **"Create repository"**

### 2. Push Your Code
```bash
# Update remote URL (replace YOUR_USERNAME)
git remote set-url origin https://github.com/YOUR_USERNAME/healthcare-platform.git

# Push to GitHub
git push -u origin main
```

### 3. Deploy Frontend (Vercel)
1. Go to [vercel.com](https://vercel.com) and sign in with GitHub
2. Click **"New Project"**
3. Import your `healthcare-platform` repository
4. Configure:
   - **Framework**: Next.js
   - **Root Directory**: `app`
   - **Build Command**: `npm run build`
5. Set Environment Variables:
   - `NEXT_PUBLIC_API_URL` = `https://your-backend.railway.app` (set after backend deploy)
   - `NEXT_PUBLIC_COGNITO_DOMAIN` = Your AWS Cognito domain
   - `NEXT_PUBLIC_COGNITO_CLIENT_ID` = Your Cognito client ID
6. Click **"Deploy"**

### 4. Deploy Backend (Railway)
1. Go to [railway.app](https://railway.app) and sign in with GitHub
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your `healthcare-platform` repository
4. Configure:
   - **Root Directory**: `api`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python manage.py migrate && python manage.py runserver 0.0.0.0:$PORT`
5. Set Environment Variables:
   ```env
   SECRET_KEY=your-secret-key-here-make-it-long-and-random
   DEBUG=False
   ALLOWED_HOSTS=your-app.railway.app
   DATABASE_URL=postgresql://... (Railway provides this)
   REDIS_URL=redis://... (Railway provides this)
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```
6. Click **"Deploy"**

### 5. Update Frontend with Backend URL
1. Go back to Vercel dashboard
2. Go to your project → Settings → Environment Variables
3. Update `NEXT_PUBLIC_API_URL` with your Railway backend URL
4. Redeploy

## 🎯 One-Click Deploy Buttons

Add these to your README (replace YOUR_USERNAME):

```markdown
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/healthcare-platform&env=NEXT_PUBLIC_API_URL,NEXT_PUBLIC_COGNITO_DOMAIN,NEXT_PUBLIC_COGNITO_CLIENT_ID&envDescription=Environment%20variables%20needed%20for%20the%20frontend&project-name=healthcare-platform)

[![Deploy to Railway](https://railway.app/button.svg)](https://railway.app/template/your-template-id?referralCode=your-code)
```

## 🔧 Environment Variables Reference

### Frontend (Vercel)
- `NEXT_PUBLIC_API_URL` - Your backend URL
- `NEXT_PUBLIC_COGNITO_DOMAIN` - AWS Cognito domain
- `NEXT_PUBLIC_COGNITO_CLIENT_ID` - Cognito client ID

### Backend (Railway)
- `SECRET_KEY` - Django secret key
- `DEBUG` - Set to False for production
- `ALLOWED_HOSTS` - Your domain
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `EMAIL_HOST` - SMTP server
- `EMAIL_HOST_USER` - Email username
- `EMAIL_HOST_PASSWORD` - Email password

## 🚨 Troubleshooting

### Common Issues:
1. **CORS Error**: Make sure `ALLOWED_HOSTS` includes your frontend domain
2. **Database Error**: Ensure `DATABASE_URL` is set correctly
3. **Build Error**: Check that all dependencies are in `requirements.txt`
4. **Environment Variables**: Make sure all required variables are set

### Debug Commands:
```bash
# Check backend logs
railway logs

# Check frontend logs
vercel logs

# Test API locally
curl https://your-backend.railway.app/api/auth/me/
```

## 🎉 Success!

Once deployed, your healthcare platform will be available at:
- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://your-app.railway.app`

Test the registration flow:
1. Go to `https://your-app.vercel.app/auth/register`
2. Create a new account
3. Verify the registration works!

## 📞 Support

If you encounter issues:
1. Check the logs in Vercel/Railway dashboards
2. Verify all environment variables are set
3. Test the API endpoints directly
4. Check the GitHub repository for updates

---

**Ready to deploy?** Follow the steps above and your healthcare platform will be live in minutes! 🚀
