# GoDaddy DNS Setup for Vercel

## Instructions for Louie Bernstein

This guide will help you configure your domain (`louiebernstein.com`) in GoDaddy to point to your Vercel deployment.

---

## Step 1: Domain Added in Vercel ✅

**Status:** Both domains have been added to Vercel:
- ✅ `louiebernstein.com`
- ✅ `www.louiebernstein.com`

Now you need to configure DNS records in GoDaddy using the exact values below.

---

## Step 2: Configure DNS in GoDaddy

### Access GoDaddy DNS Settings

1. **Log into GoDaddy**
   - Go to: https://www.godaddy.com
   - Click "Sign In" (top right)
   - Enter your credentials

2. **Navigate to DNS Management**
   - Click "My Products" (top menu)
   - Find `louiebernstein.com` in your domain list
   - Click the **three dots (⋯)** next to your domain
   - Select **"DNS"** or **"Manage DNS"**

---

## Step 3: Add These Exact DNS Records

**⚠️ IMPORTANT:** Delete any existing A records for `@` and `www` that point to old hosting first!

### Record 1: Apex Domain (louiebernstein.com)

**Add this A record:**

| Type | Name | Value | TTL |
|------|------|-------|-----|
| **A** | `@` (or blank) | `76.76.21.21` | 600 (or default) |

**In GoDaddy:**
- Click **"Add"** or **"+ Add Record"**
- **Type:** Select `A`
- **Name:** Enter `@` (or leave blank - this means root domain)
- **Value:** Enter `76.76.21.21`
- **TTL:** Leave default (usually 600 seconds)
- Click **"Save"**

### Record 2: WWW Subdomain (www.louiebernstein.com)

**Add this A record:**

| Type | Name | Value | TTL |
|------|------|-------|-----|
| **A** | `www` | `76.76.21.21` | 600 (or default) |

**In GoDaddy:**
- Click **"Add"** or **"+ Add Record"**
- **Type:** Select `A`
- **Name:** Enter `www`
- **Value:** Enter `76.76.21.21`
- **TTL:** Leave default (usually 600 seconds)
- Click **"Save"**

**Note:** Vercel recommends using A records for both the apex domain and www subdomain. This is the correct configuration.

---

## Step 4: Remove Old Records (Important!)

**Delete or update these if they exist:**

- ❌ Any A records pointing to old hosting IPs
- ❌ Any CNAME records pointing to old hosting
- ❌ Any forwarding rules (these can conflict)

**Keep these:**
- ✅ MX records (for email)
- ✅ TXT records (for email verification, SPF, DKIM, etc.)

---

## Step 5: Wait for DNS Propagation

- DNS changes can take **15 minutes to 48 hours** to propagate
- Usually works within **1-2 hours**
- **Note:** If GoDaddy support had to make changes, it may take up to **24 hours** for full propagation
- You can check status at: https://dnschecker.org

**Current Status:** GoDaddy support has made the DNS changes. Waiting for propagation (up to 24 hours).

---

## Step 6: Verify in Vercel

After DNS changes:
1. Vercel will automatically detect when DNS is configured correctly
2. SSL certificate will be issued automatically (can take a few minutes)
3. Your site will be live at `louiebernstein.com` and `www.louiebernstein.com`

---

## Troubleshooting

### If domain doesn't connect:

1. **Check DNS records are correct**
   - Use: https://dnschecker.org
   - Search for `louiebernstein.com`
   - Verify A records show Vercel IPs

2. **Wait longer**
   - DNS can take up to 48 hours (rare, but possible)

3. **Check Vercel dashboard**
   - Go to your project → Settings → Domains
   - See if there are any error messages

4. **Contact me**
   - I can help troubleshoot if needed

---

## Quick Reference: What to Tell Louie

**Copy and paste this to Louie:**

---

> **Hey Louie,**
> 
> I've added your domain to Vercel. Now I need you to update your DNS settings in GoDaddy. Here's exactly what to do:
> 
> **Step 1:** Log into GoDaddy → My Products → louiebernstein.com → DNS (or Manage DNS)
> 
> **Step 2:** Delete any old A records for `@` and `www` that point to your old hosting
> 
> **Step 3:** Add these TWO records:
> 
> **Record 1 - Root Domain:**
> - Type: **A**
> - Name: **@** (or leave blank)
> - Value: **76.76.21.21**
> - TTL: Default (600)
> 
> **Record 2 - WWW Subdomain:**
> - Type: **A**
> - Name: **www**
> - Value: **76.76.21.21**
> - TTL: Default (600)
> 
> **Step 4:** Save all changes
> 
> **Step 5:** Wait 1-2 hours for DNS to propagate (usually works within 30-60 minutes)
> 
> **Important:** Don't delete your MX records (for email) or TXT records. Only modify the A records for the website.
> 
> Once you've done this, let me know and I'll verify everything is working!
> 
> If you run into any issues, just let me know!

---

---

## Important Notes

- ⚠️ **Don't delete MX records** (these handle email)
- ⚠️ **Don't delete TXT records** (these verify email/domain)
- ✅ **Only modify A and CNAME records** for the website
- ✅ **Keep all other records as-is**

---

## After DNS is Configured

Once the domain is connected:
1. ✅ Site will be live at `louiebernstein.com`
2. ✅ SSL certificate will auto-generate
3. ✅ Both `www` and non-`www` will work
4. ✅ I'll update any hardcoded URLs in the codebase
5. ✅ We can add a sitemap for even better AEO

---

**Questions?** Let me know if Louie needs help with any step!

