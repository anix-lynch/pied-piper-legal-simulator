# 🎯 Vercel + GitHub Organization Strategy

## The Problem You're Solving

❌ **Before:** 50+ GitHub repos, can only pin 6, hard to showcase all projects  
✅ **After:** Clean subdomain structure, all projects accessible, GitHub stays organized

---

## 🏗️ Recommended Architecture

### Use Subdomains as Your Project Index

```
gozeroshot.dev                    → Main portfolio site
├── piedpiper.gozeroshot.dev     → Pied Piper Legal Simulator
├── resume.gozeroshot.dev         → Dynamic Resume MCP
├── financial.gozeroshot.dev      → Financial Modeling Tool
├── multimodal.gozeroshot.dev     → Multimodal GenAI Studio
├── bi.gozeroshot.dev             → Business Intelligence Agent
└── api.gozeroshot.dev            → Shared API gateway (optional)
```

**Each subdomain** = Live project (never goes down as long as Vercel project exists)

---

## 📁 GitHub Organization

### Strategy 1: Monorepo (Recommended for You)

Keep everything in one place:

```
coursera-portfolio-projects/
├── pied-piper-legal-simulator/
├── financial-modeling-automation/
├── multimodal-genai-studio/
├── ai-business-intelligence-agent/
└── README.md  (Index of all projects + live links)
```

**Benefits:**
- ✅ One repo to maintain
- ✅ Shared dependencies
- ✅ Easy to navigate
- ✅ Pin just this ONE repo on GitHub

**Pin this repo** with description:
> "Portfolio of 10+ AI/ML projects - Live demos at gozeroshot.dev"

---

### Strategy 2: Separate Repos with Consistent Naming

```
anix-lynch/pied-piper-legal-simulator     → piedpiper.gozeroshot.dev
anix-lynch/financial-modeling-automation  → financial.gozeroshot.dev
anix-lynch/multimodal-genai-studio        → multimodal.gozeroshot.dev
anix-lynch/ai-business-intelligence       → bi.gozeroshot.dev
anix-lynch/resume-mcp                     → resume.gozeroshot.dev
```

**Benefits:**
- ✅ Clean separation
- ✅ Individual stars/forks
- ✅ Each has own deployment

**Pin strategy:** Pin 6 best projects, mention others in portfolio site

---

## 🎨 Vercel Project Organization

### Create Vercel Teams/Folders (Visual Organization)

Vercel doesn't have folders, but you can use **naming conventions**:

```
Vercel Projects:
├── portfolio-main                    → gozeroshot.dev
├── portfolio-piedpiper              → piedpiper.gozeroshot.dev
├── portfolio-financial              → financial.gozeroshot.dev
├── portfolio-multimodal             → multimodal.gozeroshot.dev
├── portfolio-bi-agent               → bi.gozeroshot.dev
└── portfolio-resume                 → resume.gozeroshot.dev
```

**Prefix everything with `portfolio-`** so they group together in Vercel dashboard.

---

## 🔗 Master Portfolio Page (gozeroshot.dev)

Your main site becomes the **single source of truth**:

```javascript
// src/data/projects.js
export const projects = [
  {
    id: 'pied-piper',
    title: 'Pied Piper Legal Simulator',
    url: 'https://piedpiper.gozeroshot.dev',
    api: 'https://api.piedpiper.gozeroshot.dev',
    github: 'https://github.com/anix-lynch/coursera-portfolio-projects/tree/master/pied-piper-legal-simulator',
    status: 'live',
    featured: true,
    tags: ['Legal Tech', 'AI Agents', 'FastAPI', 'React']
  },
  {
    id: 'financial-modeling',
    title: 'Financial Modeling Automation',
    url: 'https://financial.gozeroshot.dev',
    github: 'https://github.com/anix-lynch/coursera-portfolio-projects/tree/master/financial-modeling-automation',
    status: 'live',
    featured: true,
    tags: ['Finance', 'Excel', 'Streamlit']
  },
  // ... all your projects
];
```

**GitHub profile pins:**
1. coursera-portfolio-projects (monorepo)
2. gozeroshot.dev (portfolio site)
3-6. Your 4 most impressive individual projects

---

## 🗄️ Keep Projects Forever Strategy

### In Vercel:

**DO:**
- ✅ Keep projects deployed indefinitely (FREE)
- ✅ Use environment variables for secrets
- ✅ Enable auto-deployment from GitHub
- ✅ Use custom domains (subdomains)

**DON'T:**
- ❌ Delete Vercel projects (they're free!)
- ❌ Archive projects unless broken
- ❌ Remove GitHub repos (keep for code history)

### In GitHub:

**DO:**
- ✅ Keep all repos public (shows work history)
- ✅ Add good README to each project
- ✅ Link to live demo in README
- ✅ Use topics/tags for discoverability

**DON'T:**
- ❌ Delete old projects (archive if needed)
- ❌ Make repos private (unless sensitive)

---

## 🎯 Your Specific Setup Plan

### Phase 1: Organize Existing Projects

```bash
# Current state
coursera-portfolio-projects/
├── pied-piper-legal-simulator/      → piedpiper.gozeroshot.dev ✅ (just did this!)
├── financial-modeling-automation/   → financial.gozeroshot.dev (next)
├── multimodal-genai-studio/         → multimodal.gozeroshot.dev (next)
└── ai-business-intelligence-agent/  → bi.gozeroshot.dev (next)
```

### Phase 2: Add Subdomains

For each project, repeat what we just did:

1. **Add DNS record:**
   ```
   financial     → CNAME → cname.vercel-dns.com
   multimodal    → CNAME → cname.vercel-dns.com
   bi            → CNAME → cname.vercel-dns.com
   ```

2. **Deploy to Vercel:**
   ```bash
   cd financial-modeling-automation
   vercel --prod
   # Add domain in dashboard: financial.gozeroshot.dev
   ```

3. **Update main portfolio** to link to subdomain

### Phase 3: GitHub Pinning Strategy

**Pin these 6 repos:**

1. **coursera-portfolio-projects** ⭐⭐⭐  
   "10+ AI/ML projects - Live at gozeroshot.dev"

2. **gozeroshot.dev** ⭐⭐  
   "Personal portfolio - Built with Astro"

3. **pied-piper-legal-simulator** ⭐  
   "AI legal simulator - Live at piedpiper.gozeroshot.dev"

4. **Your most impressive ML project** ⭐  
   With live demo link

5. **Your most impressive data engineering project** ⭐  
   With live demo link

6. **Your most impressive full-stack project** ⭐  
   With live demo link

All others? Still accessible via main portfolio site!

---

## 📊 DNS Record Master List

Organize your DNS like this:

```
# Root
gozeroshot.dev                → Vercel (main portfolio)

# Project subdomains
piedpiper.gozeroshot.dev     → Vercel (Pied Piper)
financial.gozeroshot.dev     → Vercel (Financial Modeling)
multimodal.gozeroshot.dev    → Vercel (Multimodal Studio)
bi.gozeroshot.dev            → Vercel (BI Agent)
resume.gozeroshot.dev        → Vercel (Resume MCP)

# API subdomains (optional - can share one)
api.gozeroshot.dev           → Vercel (shared API gateway)
# OR individual:
api.piedpiper.gozeroshot.dev → Vercel (Pied Piper API)
api.financial.gozeroshot.dev → Vercel (Financial API)

# Utility subdomains
blog.gozeroshot.dev          → Ghost/Medium (optional)
docs.gozeroshot.dev          → GitBook/Notion (optional)
```

**All FREE on Vercel!**

---

## 🎨 Portfolio Site Structure

Your main `gozeroshot.dev` becomes a **project dashboard**:

```
┌─────────────────────────────────────────────────────────┐
│  ANIX LYNCH                                             │
│  AI/ML Engineer & Data Scientist                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  🚀 LIVE PROJECTS                                       │
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ Pied     │  │ Financial│  │ Multimodal│            │
│  │ Piper    │  │ Modeling │  │ GenAI     │            │
│  │ Legal    │  │          │  │ Studio    │            │
│  └──────────┘  └──────────┘  └──────────┘             │
│  🔗 View      🔗 View      🔗 View                      │
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ BI       │  │ Resume   │  │ More     │            │
│  │ Agent    │  │ MCP      │  │ Projects │            │
│  └──────────┘  └──────────┘  └──────────┘             │
│                                                         │
│  📊 10+ Projects Live | 📦 All Code on GitHub          │
└─────────────────────────────────────────────────────────┘
```

Each card links to subdomain!

---

## 🔄 Deployment Workflow

### Single Command Per Project

```bash
# Deploy/update any project
cd coursera-portfolio-projects/pied-piper-legal-simulator
git add -A && git commit -m "Update" && git push

# Vercel auto-deploys to piedpiper.gozeroshot.dev
# Takes 30 seconds, zero downtime
```

**Set up once, works forever!**

---

## 📝 Master README Template

For your monorepo `coursera-portfolio-projects/README.md`:

```markdown
# Coursera Portfolio Projects

Live portfolio of 10+ AI/ML projects demonstrating full-stack capabilities.

## 🚀 Live Projects

| Project | Demo | Tech Stack | Status |
|---------|------|------------|--------|
| [Pied Piper Legal Simulator](./pied-piper-legal-simulator) | [🔗 Live](https://piedpiper.gozeroshot.dev) | FastAPI, React, Claude | ✅ Live |
| [Financial Modeling](./financial-modeling-automation) | [🔗 Live](https://financial.gozeroshot.dev) | Streamlit, Excel | ✅ Live |
| [Multimodal GenAI Studio](./multimodal-genai-studio) | [🔗 Live](https://multimodal.gozeroshot.dev) | HuggingFace, Gradio | ✅ Live |
| [BI Agent](./ai-business-intelligence-agent) | [🔗 Live](https://bi.gozeroshot.dev) | LangChain, DuckDB | ✅ Live |

## 🌐 Portfolio

Visit [gozeroshot.dev](https://gozeroshot.dev) for full portfolio.

## 📧 Contact

- Portfolio: https://gozeroshot.dev
- GitHub: https://github.com/anix-lynch
- LinkedIn: [Your LinkedIn]
```

---

## 💡 Benefits of This Approach

### For You:
- ✅ All projects always accessible
- ✅ Clean, memorable URLs
- ✅ No pinning limit stress
- ✅ Professional presentation
- ✅ Easy to maintain

### For Recruiters/Visitors:
- ✅ One place to see everything
- ✅ All demos work (no "deployment paused")
- ✅ Clean URLs to remember
- ✅ Shows you can do DevOps

### For Costs:
- ✅ 100% FREE (Vercel free tier)
- ✅ Unlimited projects
- ✅ Unlimited subdomains
- ✅ FREE SSL certificates

---

## 🎯 Action Plan (Next Hour)

1. **Add DNS records** for your other projects:
   ```
   financial.gozeroshot.dev
   multimodal.gozeroshot.dev
   bi.gozeroshot.dev
   ```

2. **Deploy each to Vercel:**
   ```bash
   cd financial-modeling-automation && vercel --prod
   cd ../multimodal-genai-studio && vercel --prod
   cd ../ai-business-intelligence-agent && vercel --prod
   ```

3. **Add domains in Vercel** dashboard for each

4. **Update main portfolio** (gozeroshot.dev) with all links

5. **Update GitHub profile:**
   - Pin coursera-portfolio-projects
   - Update bio with gozeroshot.dev link
   - Update all project READMEs with live links

---

## 🏆 End Result

**GitHub Profile:**
- Pin 1 monorepo with "10+ projects live"
- Clean, organized, all code accessible

**Portfolio Site (gozeroshot.dev):**
- Master index of all projects
- Each project = clickable card → subdomain
- Professional, scalable

**Never Delete:**
- Keep all Vercel projects (FREE!)
- Keep all GitHub repos (history matters)
- Subdomains work forever

**You control everything from one place!**

---

## 📚 Quick Reference

```bash
# Your master command
cd ~/dev/coursera-portfolio-projects

# Deploy any project
cd <project-name>
vercel --prod

# Update main portfolio
cd ~/dev/www.gozeroshot.dev
# Edit, commit, push (auto-deploys)
```

**Everything stays organized, nothing gets deleted, all projects accessible!**

