# URGENT FIX: API Deployment Protection Blocking Requests

## Problem
The API has Vercel Deployment Protection enabled (returning HTTP 401), blocking all requests.

## Fix (Do this in Vercel Dashboard NOW)

1. Go to: https://vercel.com/anix-lynchs-projects/pied-piper-legal-simulator
2. Click **Settings** → **Deployment Protection**
3. Set to **"Off"** or **"Standard Protection"**
4. Click **Save**

## Alternative: Use vercel CLI
```bash
cd /Users/anixlynch/dev/coursera-portfolio-projects/pied-piper-legal-simulator
vercel project rm-protection
```

## After fixing, the API will work at:
- https://pied-piper-legal-simulator-anix-lynchs-projects.vercel.app

The frontend is already configured to use this URL.

