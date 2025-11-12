# 🌐 DNS Setup Guide: Add Subdomains for Vercel

Step-by-step instructions for adding DNS records in **Vercel** or **Namesilo**.

---

## 🎯 What We're Doing

Adding DNS CNAME records to point subdomains to Vercel:

```
piedpiper.gozeroshot.dev  → Vercel (Pied Piper project)
financial.gozeroshot.dev  → Vercel (Financial Modeling)
multimodal.gozeroshot.dev → Vercel (Multimodal Studio)
bi.gozeroshot.dev         → Vercel (BI Agent)
```

---

## 📋 Choose Your Method

**Option 1:** Use Vercel DNS (Easiest, Recommended)  
**Option 2:** Use Namesilo DNS (Keep current registrar)

---

# OPTION 1: Vercel DNS (Recommended - Easiest)

## ✨ Why Vercel DNS?

- ✅ **Automatic subdomain routing** - Just deploy, domain works
- ✅ **Instant propagation** - No waiting
- ✅ **FREE** - No extra cost
- ✅ **Auto SSL** - Certificates just work
- ✅ **Simple** - Manage everything in one place

---

## 🚀 Step-by-Step: Transfer DNS to Vercel

### 1️⃣ Log into Vercel Dashboard

Go to: https://vercel.com/dashboard

---

### 2️⃣ Add Your Domain to Vercel

1. Click **"Domains"** in left sidebar
2. Click **"Add Domain"**
3. Enter: `gozeroshot.dev`
4. Click **"Add"**

Vercel will give you nameservers (save these!):

```
ns1.vercel-dns.com
ns2.vercel-dns.com
```

---

### 3️⃣ Update Nameservers at Namesilo

1. Log into **Namesilo**: https://www.namesilo.com/account_domains.php
2. Find `gozeroshot.dev` in your domains list
3. Click **"Manage DNS"** or **"Change Nameservers"**
4. Select **"Use Custom Nameservers"**
5. Remove old nameservers
6. Add Vercel nameservers:
   ```
   ns1.vercel-dns.com
   ns2.vercel-dns.com
   ```
7. Click **"Submit"** or **"Update"**

**⏰ Wait:** 5 minutes to 48 hours (usually 15-30 minutes)

---

### 4️⃣ Verify DNS Transfer

Check if nameservers updated:

```bash
# Check nameservers
dig NS gozeroshot.dev

# Should show:
# gozeroshot.dev.  IN  NS  ns1.vercel-dns.com.
# gozeroshot.dev.  IN  NS  ns2.vercel-dns.com.
```

Or use online tool: https://www.whatsmydns.net/#NS/gozeroshot.dev

---

### 5️⃣ Add Subdomains in Vercel (After DNS Transfer)

Once nameservers are updated:

1. Go to your Vercel project (e.g., `pied-piper-legal-simulator`)
2. Click **Settings** → **Domains**
3. Click **"Add Domain"**
4. Enter: `piedpiper.gozeroshot.dev`
5. Click **"Add"**

**Vercel automatically:**
- ✅ Creates DNS record
- ✅ Issues SSL certificate
- ✅ Routes traffic

**Repeat for each project:**
- `financial.gozeroshot.dev`
- `multimodal.gozeroshot.dev`
- `bi.gozeroshot.dev`

---

### ✅ Done with Vercel DNS!

Your subdomains work immediately. No manual DNS records needed.

---

---

# OPTION 2: Namesilo DNS (Keep Current Setup)

## 🔧 Why Namesilo DNS?

- Keep email/other services at Namesilo
- More control over DNS
- Familiar interface

---

## 🚀 Step-by-Step: Add DNS Records in Namesilo

### 1️⃣ Log into Namesilo

Go to: https://www.namesilo.com/account_home.php

---

### 2️⃣ Access DNS Manager

1. Click **"Domain Manager"** (top menu)
2. Find `gozeroshot.dev` in your domains list
3. Click the **blue circle icon** next to domain (DNS settings)
4. OR click domain → **"Manage DNS for this domain"**

You'll see the DNS Records page.

---

### 3️⃣ Add CNAME Records for Each Subdomain

For **EACH** subdomain, add a new CNAME record:

#### Pied Piper (piedpiper.gozeroshot.dev)

1. Scroll to **"Add/Edit a Resource Record"** section
2. Fill in:
   ```
   HOSTNAME: piedpiper
   TYPE: CNAME
   VALUE: cname.vercel-dns.com
   DISTANCE/PRIO: (leave blank)
   TTL: 3600
   ```
3. Click **"Submit"**

#### Financial Modeling (financial.gozeroshot.dev)

1. Add new record:
   ```
   HOSTNAME: financial
   TYPE: CNAME
   VALUE: cname.vercel-dns.com
   TTL: 3600
   ```
2. Click **"Submit"**

#### Multimodal Studio (multimodal.gozeroshot.dev)

1. Add new record:
   ```
   HOSTNAME: multimodal
   TYPE: CNAME
   VALUE: cname.vercel-dns.com
   TTL: 3600
   ```
2. Click **"Submit"**

#### BI Agent (bi.gozeroshot.dev)

1. Add new record:
   ```
   HOSTNAME: bi
   TYPE: CNAME
   VALUE: cname.vercel-dns.com
   TTL: 3600
   ```
2. Click **"Submit"**

---

### 📋 Visual Guide - Namesilo Form

```
┌─────────────────────────────────────────────────────────┐
│  Add/Edit a Resource Record                              │
├─────────────────────────────────────────────────────────┤
│  HOSTNAME:  [piedpiper                           ]       │
│             (subdomain name only, no domain)             │
│                                                          │
│  TYPE:      [CNAME ▼]                                    │
│                                                          │
│  VALUE:     [cname.vercel-dns.com                ]       │
│             (Vercel's CNAME target)                      │
│                                                          │
│  DISTANCE:  [        ]  (leave blank for CNAME)          │
│                                                          │
│  TTL:       [3600    ]  (1 hour)                         │
│                                                          │
│  [Submit]  [Cancel]                                      │
└─────────────────────────────────────────────────────────┘
```

---

### 4️⃣ Verify DNS Records

After submitting all records, check they're listed:

**Your DNS records should show:**

```
HOSTNAME       TYPE    VALUE                    TTL
piedpiper      CNAME   cname.vercel-dns.com    3600
financial      CNAME   cname.vercel-dns.com    3600
multimodal     CNAME   cname.vercel-dns.com    3600
bi             CNAME   cname.vercel-dns.com    3600
```

---

### 5️⃣ Wait for DNS Propagation

**Time:** 5 minutes to 48 hours (usually 15-30 minutes)

Check propagation:
```bash
# Test each subdomain
dig piedpiper.gozeroshot.dev
dig financial.gozeroshot.dev
dig multimodal.gozeroshot.dev
dig bi.gozeroshot.dev

# Should show CNAME to cname.vercel-dns.com
```

Or use: https://www.whatsmydns.net/#CNAME/piedpiper.gozeroshot.dev

---

### 6️⃣ Add Domains in Vercel (After DNS Propagates)

Once DNS is live (15+ minutes):

1. Go to Vercel project: https://vercel.com/dashboard
2. Click project (e.g., `pied-piper-legal-simulator`)
3. **Settings** → **Domains**
4. Click **"Add Domain"**
5. Enter: `piedpiper.gozeroshot.dev`
6. Click **"Add"**

Vercel will:
- ✅ Verify DNS record (instant if propagated)
- ✅ Issue SSL certificate (5-10 minutes)
- ✅ Route traffic

**Repeat for each project** (financial, multimodal, bi)

---

### ✅ Done with Namesilo DNS!

Your subdomains are now live at Namesilo, pointing to Vercel.

---

---

## 🧪 Testing Your Setup

### Check DNS Records

```bash
# Method 1: dig command
dig piedpiper.gozeroshot.dev

# Should show:
# piedpiper.gozeroshot.dev. 3600 IN CNAME cname.vercel-dns.com.

# Method 2: nslookup
nslookup piedpiper.gozeroshot.dev

# Method 3: Online tool
# Visit: https://www.whatsmydns.net/
# Enter: piedpiper.gozeroshot.dev
# Type: CNAME
# Check globally
```

---

### Test HTTPS Access

```bash
# Test HTTP response
curl -I https://piedpiper.gozeroshot.dev

# Should return:
# HTTP/2 200
# or
# HTTP/2 301 (redirect to HTTPS)

# Should NOT return:
# Could not resolve host (DNS not ready)
# SSL certificate problem (SSL not ready)
```

---

### Browser Test

1. Open browser
2. Go to: `https://piedpiper.gozeroshot.dev`
3. Check:
   - ✅ Page loads
   - ✅ Green lock icon (SSL working)
   - ✅ No certificate warnings

---

## 🆚 Vercel DNS vs Namesilo DNS Comparison

| Feature | Vercel DNS | Namesilo DNS |
|---------|-----------|--------------|
| **Setup Time** | 5 minutes | 30 minutes |
| **Propagation** | Instant | 15-30 mins |
| **SSL Certificates** | Auto | Auto (after DNS) |
| **Subdomain Management** | Auto (just deploy) | Manual CNAME each |
| **Cost** | FREE | FREE |
| **Control** | Less (Vercel controls) | More (you control) |
| **Email Support** | Need separate service | Can keep at Namesilo |
| **Best For** | Pure web projects | Mixed services |

---

## 🎯 Which Should You Choose?

### Choose **Vercel DNS** if:
- ✅ Your domain is ONLY for web projects
- ✅ You want easiest setup
- ✅ You don't need email on this domain
- ✅ You want instant subdomain creation

### Choose **Namesilo DNS** if:
- ✅ You have email at this domain
- ✅ You use other DNS features (MX, TXT records)
- ✅ You want to keep everything at one registrar
- ✅ You're comfortable with DNS management

**My Recommendation:** Start with **Namesilo DNS** (keep control), switch to Vercel DNS later if you want.

---

## 🐛 Troubleshooting

### DNS Record Not Showing?

**Namesilo:**
1. Check you clicked "Submit" after adding record
2. Check HOSTNAME is correct (e.g., "piedpiper" not "piedpiper.gozeroshot.dev")
3. Check TYPE is "CNAME" not "A"
4. Check VALUE is "cname.vercel-dns.com" (exactly)
5. Wait 15-30 minutes for propagation

**Vercel DNS:**
1. Check nameservers are updated at registrar
2. Wait 30 minutes to 24 hours for nameserver change
3. Use `dig NS gozeroshot.dev` to verify

---

### Domain Not Verifying in Vercel?

1. Wait 30 minutes for DNS propagation
2. Check DNS record is correct:
   ```bash
   dig piedpiper.gozeroshot.dev
   # Should show CNAME to cname.vercel-dns.com
   ```
3. Try removing and re-adding domain in Vercel
4. Check you own root domain (gozeroshot.dev) in Vercel

---

### SSL Certificate Not Working?

- Auto-issues after domain verification (5-10 minutes)
- Check domain is verified in Vercel first
- Try accessing via HTTPS: `https://piedpiper.gozeroshot.dev`
- Check Vercel dashboard: Settings → Domains → SSL status

---

### "Could Not Resolve Host" Error?

- DNS not propagated yet
- Wait 15-30 minutes
- Check DNS record exists in Namesilo/Vercel
- Use `dig` to verify

---

## 📝 Quick Reference

### Namesilo DNS Record Format
```
HOSTNAME: [subdomain]  (e.g., piedpiper, financial, bi)
TYPE: CNAME
VALUE: cname.vercel-dns.com
TTL: 3600
```

### Vercel Nameservers (if using Vercel DNS)
```
ns1.vercel-dns.com
ns2.vercel-dns.com
```

### Test Commands
```bash
# Check DNS
dig piedpiper.gozeroshot.dev

# Check nameservers
dig NS gozeroshot.dev

# Test HTTPS
curl -I https://piedpiper.gozeroshot.dev

# Check globally
# https://www.whatsmydns.net/
```

---

## 🎯 Next Steps After DNS Setup

1. ✅ DNS records added (Vercel or Namesilo)
2. ✅ Wait 15-30 minutes for propagation
3. ✅ Add domains in Vercel dashboard
4. ✅ Wait for SSL certificates (5-10 mins)
5. ✅ Test all subdomains work
6. ✅ Update main portfolio site with links
7. ✅ Update project READMEs with live URLs

---

## 📞 Support Links

**Vercel:**
- Dashboard: https://vercel.com/dashboard
- Docs: https://vercel.com/docs/concepts/projects/domains
- DNS Help: https://vercel.com/docs/concepts/projects/domains/add-a-domain

**Namesilo:**
- Login: https://www.namesilo.com/account_home.php
- DNS Manager: https://www.namesilo.com/account_domains.php
- Support: https://www.namesilo.com/Support/

**DNS Tools:**
- DNS Checker: https://www.whatsmydns.net/
- DNS Propagation: https://dnschecker.org/

---

**Choose your path:**
- **Quick & Easy:** Follow "OPTION 1: Vercel DNS"
- **Keep Control:** Follow "OPTION 2: Namesilo DNS"

Both are FREE and work perfectly! 🚀

