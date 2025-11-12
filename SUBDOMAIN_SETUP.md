# Setting Up piedpiper.gozeroshot.dev Subdomain

## ✅ Vercel Free Tier Supports Custom Domains & Subdomains!

You can use **subdomains for FREE** on Vercel. No Pro plan needed.

---

## 📝 Subdomain Format

✅ **Correct:** `piedpiper.gozeroshot.dev`  
❌ **Wrong:** `gozeroshot.dev.piedpiper` (not valid DNS format)

---

## 🔧 Setup Steps

### 1️⃣ Add Domain to Vercel (If Not Already Done)

```bash
# First time only - add your root domain
vercel domains add gozeroshot.dev
```

This tells Vercel you own `gozeroshot.dev`.

---

### 2️⃣ Configure DNS Records

Go to your domain registrar (where you bought gozeroshot.dev) and add these DNS records:

#### For Frontend: `piedpiper.gozeroshot.dev`
```
Type: CNAME
Name: piedpiper
Value: cname.vercel-dns.com
TTL: 3600 (or Auto)
```

#### For API: `api-piedpiper.gozeroshot.dev`
```
Type: CNAME
Name: api-piedpiper
Value: cname.vercel-dns.com
TTL: 3600
```

**OR** if your registrar uses full domain format:
```
Type: CNAME
Name: piedpiper.gozeroshot.dev
Value: cname.vercel-dns.com
```

---

### 3️⃣ Add Subdomain to Vercel Projects

#### Frontend Project
```bash
cd /Users/anixlynch/dev/coursera-portfolio-projects/pied-piper-legal-simulator/public
vercel
# When deployed, go to Vercel Dashboard:
```

**Via Vercel Dashboard:**
1. Go to https://vercel.com/dashboard
2. Click on `public` project
3. Go to **Settings** → **Domains**
4. Click **Add Domain**
5. Enter: `piedpiper.gozeroshot.dev`
6. Click **Add**

Vercel will automatically verify DNS and issue SSL certificate.

#### API Project
```bash
cd /Users/anixlynch/dev/coursera-portfolio-projects/pied-piper-legal-simulator
vercel
```

**Via Vercel Dashboard:**
1. Go to `pied-piper-legal-simulator` project
2. Settings → Domains
3. Add: `api-piedpiper.gozeroshot.dev` (or `api.piedpiper.gozeroshot.dev`)

---

### 4️⃣ Update Frontend to Use New API Domain

Edit `public/index.html`:

```javascript
// OLD
const API_BASE = "https://pied-piper-legal-simulator.vercel.app";

// NEW
const API_BASE = "https://api-piedpiper.gozeroshot.dev";
```

Or use environment detection:
```javascript
const API_BASE = window.location.hostname === 'localhost' 
  ? "http://localhost:8000"
  : window.location.hostname === 'piedpiper.gozeroshot.dev'
    ? "https://api-piedpiper.gozeroshot.dev"
    : "https://pied-piper-legal-simulator.vercel.app";
```

---

### 5️⃣ Wait for DNS Propagation

DNS changes can take 5 minutes to 48 hours, but usually ~15 minutes.

**Check DNS propagation:**
```bash
# Check if DNS is live
dig piedpiper.gozeroshot.dev
nslookup piedpiper.gozeroshot.dev

# Should show CNAME pointing to vercel
```

Or use online tool: https://www.whatsmydns.net/

---

## 🎯 Final URLs

After setup completes:

| Service | URL | Vercel Default |
|---------|-----|----------------|
| **Frontend** | https://piedpiper.gozeroshot.dev | https://public-anix-lynchs-projects.vercel.app |
| **API** | https://api-piedpiper.gozeroshot.dev | https://pied-piper-legal-simulator.vercel.app |

---

## 🔐 SSL Certificates

Vercel automatically provisions **free SSL certificates** via Let's Encrypt for custom domains. No configuration needed!

---

## 💰 Vercel Free Tier Limits

✅ **What's Included (FREE):**
- Custom domains: **Unlimited**
- Subdomains: **Unlimited**
- SSL certificates: **Free**
- Bandwidth: 100 GB/month
- Build time: 6,000 minutes/month
- Serverless functions: 100 GB-hours/month
- Team members: 1 (hobby plan)

❌ **Pro Plan Required For:**
- Team collaboration (multiple users)
- Advanced analytics
- Password protection
- Custom redirects (beyond vercel.json)
- Priority support

**For your use case: FREE TIER IS PERFECT!**

---

## 🧪 Testing After Setup

```bash
# Test frontend
curl -I https://piedpiper.gozeroshot.dev

# Test API
curl https://api-piedpiper.gozeroshot.dev/
curl https://api-piedpiper.gozeroshot.dev/episodes

# Should return JSON
```

---

## 🎨 Alternative Subdomain Patterns

You could also use:

1. **Separate subdomains:**
   - `app.piedpiper.gozeroshot.dev` (frontend)
   - `api.piedpiper.gozeroshot.dev` (backend)

2. **Simpler:**
   - `piedpiper.gozeroshot.dev` (frontend)
   - `api.gozeroshot.dev` (backend - can be used for multiple projects)

3. **Project-based:**
   - `pied-piper.gozeroshot.dev` (frontend)
   - `api-pied-piper.gozeroshot.dev` (backend)

All FREE on Vercel!

---

## 📋 Quick Setup Commands

```bash
# 1. Add DNS records at your registrar
#    (See step 2 above)

# 2. Deploy projects (if not already)
cd /Users/anixlynch/dev/coursera-portfolio-projects/pied-piper-legal-simulator
vercel --prod  # API

cd public/
vercel --prod  # Frontend

# 3. Add domains via Vercel CLI or Dashboard
# Via CLI (requires domain already added to Vercel):
vercel domains add piedpiper.gozeroshot.dev --project=public
vercel domains add api-piedpiper.gozeroshot.dev --project=pied-piper-legal-simulator

# Or use Dashboard (easier):
# https://vercel.com/dashboard → Project → Settings → Domains
```

---

## 🐛 Troubleshooting

### Domain not verifying?
1. Check DNS records are correct
2. Wait 15-30 minutes for propagation
3. Try removing and re-adding domain in Vercel
4. Verify you own the root domain (gozeroshot.dev) in Vercel

### SSL certificate not provisioning?
- Usually auto-provisions in 5-10 minutes
- Check domain is verified first
- Vercel will email you when ready

### 403 Forbidden or Authentication Required?
- Disable "Deployment Protection" in Project Settings → Deployment Protection
- Set to "Off" for public projects

---

## ✨ Recommended Setup

**Best practice for your portfolio:**

```
Frontend:  piedpiper.gozeroshot.dev
API:       api.piedpiper.gozeroshot.dev  (NOT api-piedpiper)
```

This is cleaner and follows standard subdomain conventions.

**DNS Records:**
```
Type: CNAME
Name: piedpiper
Value: cname.vercel-dns.com

Type: CNAME
Name: api.piedpiper   (or just "api" if registrar supports nested)
Value: cname.vercel-dns.com
```

---

## 🚀 Next Steps

1. **Add DNS records** at your registrar
2. **Add domains in Vercel** dashboard
3. **Update frontend** API URL
4. **Test** after DNS propagates (15 mins)
5. **Update portfolio** links to use custom domain

**No Vercel Pro needed - FREE tier works perfectly!**

---

## 📝 After Setup

Update your portfolio integration:

```javascript
{
  title: "Pied Piper Legal Simulator",
  links: {
    demo: "https://piedpiper.gozeroshot.dev",  // ← NEW
    api: "https://api.piedpiper.gozeroshot.dev", // ← NEW
    github: "https://github.com/anix-lynch/pied-piper-legal-simulator"
  }
}
```

Much cleaner URLs! 🎉

