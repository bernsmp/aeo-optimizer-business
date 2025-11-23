# How to Get Files in Your Local Workspace

## The Problem

Files exist in the **remote workspace** (`/workspace`) but your **local workspace** (`/Users/maxb/Desktop/Vibe Projects/aeo-optimizer-business`) isn't showing them.

## Solution: Pull from Git

The files are committed to git. Run these commands **in your local terminal**:

```bash
cd "/Users/maxb/Desktop/Vibe Projects/aeo-optimizer-business"
git fetch origin
git checkout cursor/brainstorm-ai-website-strategy-composer-1-1ac8
git pull origin cursor/brainstorm-ai-website-strategy-composer-1-1ac8
```

Then check:
```bash
ls -la business-plans/
```

You should see 37 markdown files.

## If That Doesn't Work

The files might be on a different branch. Try:

```bash
git branch -a
```

Look for branches with "cursor" or "brainstorm" in the name.

## Alternative: Check Current Branch

See what branch you're on:
```bash
git branch
```

If you're on `main`, switch to the cursor branch:
```bash
git checkout cursor/brainstorm-ai-website-strategy-composer-1-1ac8
```

---

**All 37 files are committed and ready - you just need to pull them to your local workspace!**
