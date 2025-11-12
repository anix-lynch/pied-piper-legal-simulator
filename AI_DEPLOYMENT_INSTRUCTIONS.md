# 🤖 AI Agent Instructions: Deploy Projects to Vercel Subdomains

**PURPOSE:** Use this file to instruct any AI assistant to deploy my portfolio projects to custom subdomains on Vercel.

---

## 🎯 GOAL

Deploy all projects from `coursera-portfolio-projects` monorepo to individual Vercel subdomains under `gozeroshot.dev`.

---

## 📋 CONTEXT

**Domain:** gozeroshot.dev (I own this)  
**Vercel Account:** anix-lynch (free tier)  
**GitHub:** https://github.com/anix-lynch  
**Monorepo:** https://github.com/anix-lynch/coursera-portfolio-projects

**Why:** 
- Solve GitHub pinning limit (can only pin 6 repos)
- All projects accessible via clean subdomain URLs
- Professional portfolio presentation
- Never delete projects (Vercel free tier = unlimited projects)

---

## 🏗️ DESIRED ARCHITECTURE

```
gozeroshot.dev                    → Main portfolio site (already deployed)
├── piedpiper.gozeroshot.dev     → Pied Piper Legal Simulator ✅ DONE
├── financial.gozeroshot.dev     → Financial Modeling Automation
├── multimodal.gozeroshot.dev    → Multimodal GenAI Studio
├── bi.gozeroshot.dev            → AI Business Intelligence Agent
└── resume.gozeroshot.dev        → Dynamic Resume MCP

Future projects:
├── cocktail.gozeroshot.dev      → Cocktailverse
├── mocktail.gozeroshot.dev      → Mocktailverse
└── [projectname].gozeroshot.dev → Any new project
```

**Each subdomain** = Separate Vercel deployment pointing to subfolder in monorepo.

---

## 📁 PROJECT LOCATIONS

All in: `/Users/anixlynch/dev/coursera-portfolio-projects/`

| Project Folder | Subdomain | Status |
|----------------|-----------|--------|
| `pied-piper-legal-simulator` | piedpiper.gozeroshot.dev | ✅ DONE |
| `financial-modeling-automation` | financial.gozeroshot.dev | ⏳ TODO |
| `multimodal-genai-studio` | multimodal.gozeroshot.dev | ⏳ TODO |
| `ai-business-intelligence-agent` | bi.gozeroshot.dev | ⏳ TODO |

---

## 🚀 DEPLOYMENT STEPS (Per Project)

### 1️⃣ Add DNS Record

**At domain registrar** (GoDaddy/Namecheap/Cloudflare):

```
Type: CNAME
Name: [subdomain-prefix]  (e.g., "financial", "multimodal", "bi")
Value: cname.vercel-dns.com
TTL: Auto or 3600
```

**Example:**
```
Name: financial
Value: cname.vercel-dns.com
```

This creates `financial.gozeroshot.dev`

---

### 2️⃣ Deploy to Vercel

```bash
cd /Users/anixlynch/dev/coursera-portfolio-projects/[project-folder]

# Deploy to Vercel
vercel --prod --yes

# Example:
cd /Users/anixlynch/dev/coursera-portfolio-projects/financial-modeling-automation
vercel --prod --yes
```

**Note:** First deploy creates the Vercel project. Subsequent deploys update it.

---

### 3️⃣ Add Custom Domain in Vercel

**Via CLI:**
```bash
vercel domains add [subdomain].gozeroshot.dev
```

**Via Dashboard (Easier):**
1. Go to https://vercel.com/dashboard
2. Click the deployed project
3. Settings → Domains
4. Add Domain: `[subdomain].gozeroshot.dev`
5. Click Add

Vercel will:
- ✅ Verify DNS (takes 5-15 mins)
- ✅ Issue FREE SSL certificate
- ✅ Route traffic automatically

---

### 4️⃣ Verify Deployment

```bash
# Wait 15 minutes for DNS propagation
sleep 900

# Test
curl -I https://[subdomain].gozeroshot.dev

# Should return 200 OK with SSL
```

---

## 🔧 PROJECT-SPECIFIC CONFIGURATIONS

### Financial Modeling Automation

**Entry point:** `app.py` (Streamlit)

**vercel.json** (create if missing):
```json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

**requirements.txt:** Already exists

---

### Multimodal GenAI Studio

**Entry point:** `app.py` (Gradio/Streamlit)

**vercel.json:**
```json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

**requirements.txt:** Already exists

---

### AI Business Intelligence Agent

**Entry point:** `app.py` (Streamlit)

**vercel.json:**
```json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

**requirements.txt:** Already exists

---

## 🎨 AFTER ALL DEPLOYMENTS

### Update Main Portfolio (gozeroshot.dev)

**File:** `~/dev/www.gozeroshot.dev/src/data/projects.js` (or similar)

Add:
```javascript
{
  title: "Pied Piper Legal Simulator",
  url: "https://piedpiper.gozeroshot.dev",
  github: "https://github.com/anix-lynch/coursera-portfolio-projects/tree/master/pied-piper-legal-simulator",
  tags: ["Legal Tech", "AI", "FastAPI", "React"],
  status: "live"
},
{
  title: "Financial Modeling Automation",
  url: "https://financial.gozeroshot.dev",
  github: "https://github.com/anix-lynch/coursera-portfolio-projects/tree/master/financial-modeling-automation",
  tags: ["Finance", "Excel", "Streamlit"],
  status: "live"
},
// ... rest
```

---

### Update Monorepo README

**File:** `/Users/anixlynch/dev/coursera-portfolio-projects/README.md`

```markdown
# Coursera Portfolio Projects

Live portfolio of 10+ AI/ML projects.

## 🚀 Live Projects

| Project | Demo | Status |
|---------|------|--------|
| [Pied Piper Legal Simulator](./pied-piper-legal-simulator) | [🔗 piedpiper.gozeroshot.dev](https://piedpiper.gozeroshot.dev) | ✅ Live |
| [Financial Modeling](./financial-modeling-automation) | [🔗 financial.gozeroshot.dev](https://financial.gozeroshot.dev) | ✅ Live |
| [Multimodal GenAI Studio](./multimodal-genai-studio) | [🔗 multimodal.gozeroshot.dev](https://multimodal.gozeroshot.dev) | ✅ Live |
| [BI Agent](./ai-business-intelligence-agent) | [🔗 bi.gozeroshot.dev](https://bi.gozeroshot.dev) | ✅ Live |

Visit [gozeroshot.dev](https://gozeroshot.dev) for full portfolio.
```

---

## 🔐 ENVIRONMENT VARIABLES

Some projects need API keys. Add via Vercel:

```bash
# Via CLI
vercel env add ANTHROPIC_API_KEY production

# Via Dashboard
# Project → Settings → Environment Variables → Add
```

**Common keys needed:**
- `ANTHROPIC_API_KEY` (Pied Piper, BI Agent)
- `OPENAI_API_KEY` (Multimodal Studio)
- `HUGGINGFACE_TOKEN` (Multimodal Studio)

**Keys stored in:** `~/.config/secrets/global.env`

---

## 📊 DNS RECORDS MASTER LIST

Add these **once** at domain registrar:

```
Type: CNAME | Name: piedpiper  | Value: cname.vercel-dns.com  ✅ DONE
Type: CNAME | Name: financial  | Value: cname.vercel-dns.com  ⏳ TODO
Type: CNAME | Name: multimodal | Value: cname.vercel-dns.com  ⏳ TODO
Type: CNAME | Name: bi         | Value: cname.vercel-dns.com  ⏳ TODO
Type: CNAME | Name: resume     | Value: cname.vercel-dns.com  ⏳ TODO
Type: CNAME | Name: cocktail   | Value: cname.vercel-dns.com  ⏳ FUTURE
Type: CNAME | Name: mocktail   | Value: cname.vercel-dns.com  ⏳ FUTURE
```

---

## 🧪 VERIFICATION CHECKLIST

After each deployment:

- [ ] DNS record added and propagated (15 mins)
- [ ] Project deployed to Vercel (`vercel --prod`)
- [ ] Custom domain added in Vercel dashboard
- [ ] SSL certificate issued (auto, 5 mins)
- [ ] Subdomain accessible via HTTPS
- [ ] Main portfolio updated with link
- [ ] Monorepo README updated
- [ ] Project-specific README has live demo link

---

## 🚨 TROUBLESHOOTING

### DNS not propagating?
```bash
# Check DNS
dig [subdomain].gozeroshot.dev

# Should show CNAME to vercel
# Wait 15-30 minutes if not showing
```

### Vercel deployment failed?
1. Check `vercel.json` exists
2. Check `requirements.txt` or `package.json` exists
3. Check for build errors in Vercel dashboard
4. Try: `vercel --debug`

### Domain not verifying in Vercel?
1. Verify DNS record is correct (CNAME to `cname.vercel-dns.com`)
2. Wait 30 minutes for propagation
3. Remove and re-add domain in Vercel
4. Check root domain (`gozeroshot.dev`) is verified in Vercel

### SSL certificate not issuing?
- Automatically issues after domain verification (5-10 mins)
- Check "Domains" tab in Vercel project for status

---

## 🎯 SUCCESS CRITERIA

**For each project:**
- ✅ Accessible at `[name].gozeroshot.dev`
- ✅ HTTPS working (green lock icon)
- ✅ Auto-deploys on git push to master
- ✅ Listed in main portfolio site
- ✅ Listed in monorepo README

**Overall:**
- ✅ All projects live and accessible
- ✅ Clean URLs (no .vercel.app)
- ✅ Professional portfolio presentation
- ✅ GitHub organized (1 pinned monorepo)

---

## 💡 AI AGENT EXECUTION TEMPLATE

**When I say:** "Deploy [project-name] to [subdomain].gozeroshot.dev"

**You should:**

1. Navigate to project folder
2. Check if `vercel.json` exists, create if needed
3. Run `vercel --prod --yes`
4. Instruct me to add DNS record (I'll do manually)
5. Wait for my confirmation DNS is added
6. Add domain in Vercel via CLI or remind me to do via dashboard
7. Wait 15 mins for DNS propagation
8. Test with `curl -I https://[subdomain].gozeroshot.dev`
9. Update main portfolio site
10. Update monorepo README
11. Confirm deployment complete

---

## 📝 QUICK COMMANDS

```bash
# Deploy single project
cd /Users/anixlynch/dev/coursera-portfolio-projects/[project-name]
vercel --prod --yes

# Deploy all (run from monorepo root)
for dir in */; do
  cd "$dir"
  if [ -f "app.py" ] || [ -f "package.json" ]; then
    echo "Deploying $dir..."
    vercel --prod --yes
  fi
  cd ..
done

# Check all domains
for sub in piedpiper financial multimodal bi resume; do
  echo "Checking $sub.gozeroshot.dev..."
  curl -I https://$sub.gozeroshot.dev 2>&1 | head -1
done
```

---

## 🎨 NAMING CONVENTIONS

**Vercel Project Names:** `portfolio-[shortname]`
- portfolio-piedpiper
- portfolio-financial
- portfolio-multimodal
- portfolio-bi-agent

**Subdomains:** `[shortname].gozeroshot.dev`
- piedpiper.gozeroshot.dev
- financial.gozeroshot.dev
- multimodal.gozeroshot.dev
- bi.gozeroshot.dev

**Keep consistent!**

---

## 🔄 MAINTENANCE

### Update a project:
```bash
cd /Users/anixlynch/dev/coursera-portfolio-projects/[project-name]
git add -A
git commit -m "Update"
git push

# Vercel auto-deploys (GitHub integration)
# Or manual: vercel --prod
```

### Add new project:
1. Add DNS record for new subdomain
2. Deploy with `vercel --prod`
3. Add domain in Vercel
4. Update portfolio site
5. Update monorepo README

---

## 🏆 FINAL NOTES

**Vercel Free Tier Limits (More than enough!):**
- ✅ Unlimited projects
- ✅ Unlimited custom domains
- ✅ 100 GB bandwidth/month
- ✅ 6,000 build minutes/month
- ✅ FREE SSL certificates

**Cost:** $0/month forever

**Maintenance:** Zero (auto-deploy from GitHub)

**Organization:** All projects in one place, all accessible via clean URLs

---

## 📞 HELP REFERENCES

- **Subdomain Setup:** See `SUBDOMAIN_SETUP.md` in pied-piper-legal-simulator repo
- **Organization Strategy:** See `VERCEL_ORGANIZATION_STRATEGY.md`
- **Deployment Template:** See `PORTFOLIO_DEPLOYMENT_TEMPLATE.md`

---

**Last Updated:** November 12, 2025  
**Status:** Pied Piper ✅ Deployed | Others ⏳ Ready to Deploy  
**AI Agent:** Use this file as complete deployment guide

