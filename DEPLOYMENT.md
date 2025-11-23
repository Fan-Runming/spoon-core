# U NO HOO - Deployment Guide

## 🚀 Quick Deploy Options

### Option 1: Replit (Easiest - 5 minutes)

1. **Fork on Replit**
   - Go to https://replit.com
   - Click "Create Repl" → "Import from GitHub"
   - Paste: `https://github.com/Fan-Runming/spoon-core`
   - Click "Import from GitHub"

2. **Set Environment Variables**
   - Click "Secrets" (lock icon) in left sidebar
   - Add: `GEMINI_API_KEY` = `your_api_key_here`

3. **Run**
   - Click the "Run" button
   - Replit will automatically generate a public URL
   - Share this URL as your demo link!

**Example URL**: `https://spoon-core.your-username.repl.co`

---

### Option 2: Railway (Recommended - 10 minutes)

1. **Sign up at Railway**
   - Visit https://railway.app
   - Sign in with GitHub

2. **Deploy from GitHub**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `spoon-core` repository
   - Railway auto-detects Python and deploys

3. **Add Environment Variables**
   - Go to "Variables" tab
   - Add `GEMINI_API_KEY`
   - Add `PORT` = `8000`

4. **Generate Domain**
   - Go to "Settings" → "Networking"
   - Click "Generate Domain"
   - Copy the public URL

**Example URL**: `https://spoon-core-production.up.railway.app`

---

### Option 3: Render (Free - 15 minutes)

1. **Create Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Select `spoon-core`

3. **Configure Build**
   - **Name**: `u-no-hoo`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables**
   - Click "Environment" tab
   - Add `GEMINI_API_KEY` = `your_key`
   - Add `PYTHON_VERSION` = `3.12.0`

5. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment
   - Copy the `.onrender.com` URL

**Example URL**: `https://u-no-hoo.onrender.com`

---

## 🎬 Creating a Video Demo (Optional but Recommended)

### Tool: Loom
1. Go to https://loom.com
2. Click "Start Recording"
3. Show these features:
   - Homepage introduction
   - Add a person through conversation
   - View the generated card
   - Show 5 recent people list
   - Demo voice input
   - Demo photo upload
   - Show LinkedIn integration (if implemented)

### Upload to YouTube
- Set to "Unlisted"
- Add to README and submission

---

## 📊 Creating a Landing Page (Optional)

### Quick Option: Notion
1. Create a Notion page
2. Include:
   - Project title and tagline
   - Problem statement
   - Solution overview
   - Key features (with screenshots)
   - Tech stack
   - Demo link
   - GitHub link
   - Team info
3. Share → "Share to web" → Copy link

### Pro Option: Vercel + Next.js
If you want a professional landing page, I can help create one.

---

## 📋 Submission Checklist

### Required
- [ ] GitHub repository (public)
  - Clean README with setup instructions
  - All code committed and pushed
  - .env.example with placeholder values
  
- [ ] Demo Link (choose one)
  - [ ] Replit URL
  - [ ] Railway URL
  - [ ] Render URL
  - [ ] Other hosting URL

### Recommended
- [ ] Presentation deck (Google Slides/PDF)
  - Problem & Solution (2-3 slides)
  - Key Features (2-3 slides)
  - Demo screenshots (2-3 slides)
  - Tech Stack (1 slide)
  - Future Plans (1 slide)

- [ ] Product explanation
  - [ ] Notion page OR
  - [ ] Google Doc OR
  - [ ] Extended README

### Nice to Have
- [ ] Video demo (Loom/YouTube)
- [ ] Landing page (Notion/Webflow/Vercel)
- [ ] Architecture diagram
- [ ] User flow diagram

---

## ⚠️ Important Notes

### Make Sure Your Demo Works!
Before submitting, test:
1. Demo URL loads correctly
2. Can add a new person
3. Recent people list shows up
4. All buttons are functional
5. No errors in browser console

### Privacy & API Keys
- **Never commit API keys to GitHub**
- Use environment variables
- Include `.env.example` with placeholders

### Judges Access
- All links must be **public** or **unlisted**
- Test links in incognito mode
- No authentication required

---

## 🆘 Troubleshooting

### "Application failed to start"
- Check that `requirements.txt` is complete
- Verify `Procfile` or start command is correct
- Check environment variables are set

### "502 Bad Gateway"
- Service might be starting (wait 2-3 minutes)
- Check logs for errors
- Verify PORT environment variable

### "Module not found"
- Ensure all dependencies in `requirements.txt`
- Some platforms require `python-dotenv`

---

## 📧 Need Help?
- Check platform docs (Railway/Render/Replit)
- Test locally first: `uvicorn main:app --port 8000`
- Verify all environment variables are set

Good luck with your submission! 🚀
