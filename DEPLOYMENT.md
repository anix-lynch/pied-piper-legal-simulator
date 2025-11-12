# Pied Piper Legal Simulator - Deployment Guide

## 🚀 Live URLs

### Backend API
**Production:** https://pied-piper-legal-simulator.vercel.app

**Endpoints:**
- `GET /` - Health check
- `GET /episodes` - List all 5 Silicon Valley scenarios
- `POST /simulate` - Generate 3-outcome analysis (VC Win, Founder Win, Win-Win)
- `GET /export/{episode_id}` - Export simulation as markdown

### Frontend
**Production:** https://public-anix-lynchs-projects.vercel.app

### GitHub Repository
https://github.com/anix-lynch/pied-piper-legal-simulator

---

## 📋 Quick Test

```bash
# Test API health
curl https://pied-piper-legal-simulator.vercel.app/

# List episodes
curl https://pied-piper-legal-simulator.vercel.app/episodes

# Run simulation
curl -X POST https://pied-piper-legal-simulator.vercel.app/simulate \
  -H "Content-Type: application/json" \
  -d '{"episode_id": "S02E04", "mode": "all"}'

# Export markdown
curl https://pied-piper-legal-simulator.vercel.app/export/S02E04
```

---

## 🔧 Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Frontend (Vercel Static)                                │
│  └─ public/index.html → React + TailwindCSS             │
└─────────────────────────────────────────────────────────┘
                           ↓ HTTPS
┌─────────────────────────────────────────────────────────┐
│  Backend API (Vercel Serverless Python)                  │
│  └─ api/index.py → FastAPI + ClauseMatch + Narrative    │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  Data Layer                                              │
│  ├─ data/episodes.json (5 scenarios)                     │
│  └─ data/clauses.json (15+ term-sheet clauses)          │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Deployment Process

### 1. Backend API Deployment

```bash
cd /Users/anixlynch/dev/coursera-portfolio-projects/pied-piper-legal-simulator

# Deploy API
vercel --prod

# Add environment variable
vercel env add ANTHROPIC_API_KEY production
```

**vercel.json** for API:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

### 2. Frontend Deployment

```bash
cd public/
vercel --prod
```

**vercel.json** for frontend:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "index.html",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

### 3. Connect Frontend to Backend

Frontend automatically detects production and connects to:
```javascript
const API_BASE = "https://pied-piper-legal-simulator.vercel.app";
```

---

## 🔐 Environment Variables

Required for backend:
- `ANTHROPIC_API_KEY` - Claude API key for AI narratives (optional, falls back to static summaries)

```bash
# Add to Vercel
vercel env add ANTHROPIC_API_KEY production
```

---

## 📊 Sample API Response

```json
{
  "episode": {
    "episode_id": "S02E04",
    "title": "The Board Coup",
    "conflict_type": "board_control",
    "scene": "Raviga attempts to replace Richard as CEO"
  },
  "scenarios": {
    "vc_win": {
      "clauses": ["VC holds 3/5 board seats"],
      "narrative": "VCs secure maximum control...",
      "clause_details": [...]
    },
    "founder_win": {
      "clauses": ["Founder retains 60% voting via dual-class shares"],
      "narrative": "Founder retains control...",
      "clause_details": [...]
    },
    "winwin": {
      "clauses": ["Board parity 3-3 with rotating chair"],
      "narrative": "Balanced structure...",
      "clause_details": [...]
    }
  },
  "alignment_scores": {
    "vc_win": {"vc": 90, "founder": 10, "balance": 20},
    "founder_win": {"vc": 20, "founder": 85, "balance": 35},
    "winwin": {"vc": 50, "founder": 50, "balance": 100}
  }
}
```

---

## 🎨 Frontend Features

- **Episode Selector** - Dropdown with 5 Silicon Valley scenarios
- **3-Panel Display** - Side-by-side VC Win 💰, Founder Win 💡, Win-Win 🤝
- **Alignment Bars** - Visual progress bars for VC/Founder/Balance scores
- **Markdown Export** - Download button for portfolio/resume use
- **Responsive Design** - TailwindCSS, mobile-friendly

---

## 🔄 Redeploy

```bash
# Redeploy API
cd /Users/anixlynch/dev/coursera-portfolio-projects/pied-piper-legal-simulator
git add -A && git commit -m "Update" && git push
vercel --prod

# Redeploy frontend
cd public/
vercel --prod
```

---

## 📈 Custom Domains (Future)

To add custom domains:

1. Go to Vercel Dashboard → Project Settings → Domains
2. Add domain: `api.piedpiper.gozeroshot.dev` (API)
3. Add domain: `piedpiper.gozeroshot.dev` (Frontend)
4. Update DNS records:
   - Type: CNAME
   - Name: api.piedpiper / piedpiper
   - Value: cname.vercel-dns.com

---

## 💡 Portfolio Integration

Add to `gozeroshot.dev`:

```js
{
  title: "Pied Piper Legal Simulator",
  desc: "AI-powered VC term-sheet negotiation simulator with 3 outcomes",
  link: "https://public-anix-lynchs-projects.vercel.app",
  api: "https://pied-piper-legal-simulator.vercel.app",
  github: "https://github.com/anix-lynch/pied-piper-legal-simulator",
  tags: ["Legal Tech", "AI Agents", "FastAPI", "React", "Claude"],
  screenshot: "/projects/pied-piper.png"
}
```

---

## 🧪 Testing

```bash
# Run local tests
./test_local.sh

# Test production API
curl https://pied-piper-legal-simulator.vercel.app/episodes
```

---

## 📝 Notes

- **No DuckDB on Vercel serverless** - Using JSON files instead
- **Claude API optional** - Falls back to static summaries if no API key
- **CORS enabled** - Frontend can call API from any domain
- **Serverless functions** - FastAPI running on Vercel Python runtime
- **Static frontend** - Pure HTML/React, no build step needed

---

**Deployed:** November 12, 2025  
**Stack:** FastAPI + React + TailwindCSS + Vercel + Claude  
**Total Build Time:** ~2 hours

