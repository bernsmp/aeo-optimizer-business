# DNS Records for GoDaddy - Copy This to Louie

---

**Hey Louie,**

I've added your domain to Vercel. Now I need you to update your DNS settings in GoDaddy. Here's exactly what to do:

## Step 1: Access DNS Settings
- Log into GoDaddy
- Go to **My Products** → Find `louiebernstein.com` → Click **DNS** (or **Manage DNS**)

## Step 2: Delete Old Records
- Find and **delete** any old A records for `@` (root) and `www` that point to your old hosting
- **Keep** all MX records (for email) and TXT records

## Step 3: Add These Two Records

### Record 1 - Root Domain (louiebernstein.com)
- **Type:** `A`
- **Name:** `@` (or leave blank)
- **Value:** `76.76.21.21`
- **TTL:** Default (600)

### Record 2 - WWW Subdomain (www.louiebernstein.com)
- **Type:** `A`
- **Name:** `www`
- **Value:** `76.76.21.21`
- **TTL:** Default (600)

## Step 4: Save
- Click **Save** on each record
- Wait 1-2 hours for DNS to propagate (usually works within 30-60 minutes)

## Important Notes
- ✅ **Don't delete** MX records (these handle your email)
- ✅ **Don't delete** TXT records (these verify your domain/email)
- ✅ **Only modify** the A records for the website

Once you've done this, let me know and I'll verify everything is working!

---

**Questions?** Just let me know!

