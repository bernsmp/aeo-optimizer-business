# Google Docs Editing Workflow for Louie Bernstein Articles

## Overview

This workflow allows Louie to edit articles in Google Docs, then sync those changes back to the website. It's the easiest way for him to make edits without needing to work with markdown files directly.

---

## Quick Start

### Step 1: Upload Article to Google Docs

```bash
cd clients/louiebernstein
python tools/sync_article_google_docs.py upload articles/135-percent-quota-pip-article.md
```

Or use the article slug:
```bash
python tools/sync_article_google_docs.py upload 135-percent-quota-pip-article
```

**What happens:**
- Creates a new Google Doc with the article content (or updates existing one)
- Saves the Google Doc link in metadata
- Louie gets a link to edit the article

### Step 2: Louie Edits in Google Docs

1. **Open the Google Doc** (link will be shown after upload)
2. **Click the pencil icon** (top right) → Select **"Suggesting"** mode (recommended)
3. **Make all edits** - they'll show as suggestions
4. **Tell you when done** - "ready to sync" or "pull the latest"

**Why Suggesting Mode?**
- You can see exactly what changed
- Louie can add comments for context
- Easier to review changes before syncing

### Step 3: Download Changes Back

```bash
python tools/sync_article_google_docs.py download 135-percent-quota-pip-article
```

**What happens:**
- Downloads content from Google Docs
- Preserves frontmatter (title, description, keywords, etc.)
- Creates a backup of the original file
- Updates the markdown file with Louie's changes

---

## Commands Reference

### Upload Article to Google Docs
```bash
python tools/sync_article_google_docs.py upload <article-slug-or-path>
```

**Examples:**
```bash
# Using slug
python tools/sync_article_google_docs.py upload 135-percent-quota-pip-article

# Using full path
python tools/sync_article_google_docs.py upload articles/135-percent-quota-pip-article.md

# With custom folder ID
python tools/sync_article_google_docs.py upload 135-percent-quota-pip-article <folder-id>
```

### Download Changes from Google Docs
```bash
python tools/sync_article_google_docs.py download <article-slug-or-path>
```

**Examples:**
```bash
python tools/sync_article_google_docs.py download 135-percent-quota-pip-article
```

---

## How It Works

### File Structure

When you upload an article, a metadata file is created:
```
articles/
  ├── 135-percent-quota-pip-article.md
  └── .135-percent-quota-pip-article_metadata.json  (hidden file)
```

The metadata file stores:
- Google Doc ID
- Google Doc link
- Last upload/download timestamps

### Frontmatter Preservation

The script automatically:
- **Preserves frontmatter** (title, description, keywords, author, date) when downloading
- **Only syncs the body content** to/from Google Docs
- **Keeps SEO metadata intact** during edits

### Backup System

Every download creates a backup:
```
articles/
  ├── 135-percent-quota-pip-article.md
  └── 135-percent-quota-pip-article.md.backup
```

---

## Setup Requirements

### 1. Google Drive API Setup

You need `credentials.json` from Google Cloud Console:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project (or use existing)
3. Enable Google Drive API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download `credentials.json`
6. Place it in the `Jay Article Writer` directory (the script imports from there)

### 2. First-Time Authentication

On first run, the script will:
- Open a browser window
- Ask you to authenticate with Google
- Save a `token.json` file for future use

### 3. Optional: Set Default Folder

You can set an environment variable for the default Google Drive folder:
```bash
export LOUIE_GOOGLE_DRIVE_FOLDER_ID="your-folder-id-here"
```

---

## Workflow Examples

### Example 1: New Article Editing

```bash
# 1. Upload article
python tools/sync_article_google_docs.py upload 135-percent-quota-pip-article

# Output:
# ✅ Created Google Doc: https://docs.google.com/document/d/ABC123/edit
# 
# 💡 Louie can now edit this doc. When ready, run:
#    python sync_article_google_docs.py download 135-percent-quota-pip-article

# 2. Louie edits in Google Docs (using Suggesting mode)

# 3. Download changes
python tools/sync_article_google_docs.py download 135-percent-quota-pip-article

# Output:
# 💾 Backup saved to: 135-percent-quota-pip-article.md.backup
# ✅ Downloaded and merged changes to: 135-percent-quota-pip-article.md
```

### Example 2: Updating Existing Article

```bash
# If article already has a Google Doc, upload will update it
python tools/sync_article_google_docs.py upload 135-percent-quota-pip-article

# Output:
# 📝 Updating existing Google Doc...
# ✅ Updated Google Doc: https://docs.google.com/document/d/ABC123/edit
```

---

## Tips for Louie

### ✅ Best Practices

1. **Use Suggesting Mode** - Makes it easy to see what changed
2. **Add Comments** - If something needs context, add a comment
3. **Don't Edit Frontmatter** - The frontmatter (title, description, etc.) is preserved automatically
4. **Save Often** - Google Docs auto-saves, but you can manually save too

### ⚠️ Things to Avoid

1. **Don't Delete Everything** - The script will overwrite the local file
2. **Don't Edit Metadata** - Frontmatter is handled separately
3. **Don't Use Complex Formatting** - Stick to headings, bold, italic, lists

### 💡 Pro Tips

- **Review Before Syncing** - Check the Google Doc before saying "ready to sync"
- **Use Comments** - Add comments for questions or context
- **Version Control** - The script creates backups, but you can also version in Google Docs

---

## Troubleshooting

### "Could not import GoogleDriveIntegration"
- Make sure you're in the correct directory
- Check that `Jay Article Writer/tools/google_drive_integration.py` exists
- Install dependencies: `pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib`

### "No Google Doc ID found in metadata"
- Run `upload` command first to create the Google Doc

### "Credentials file not found"
- Download `credentials.json` from Google Cloud Console
- Place it in the `Jay Article Writer` directory

### Content looks wrong after download
- Check the backup file (`.backup` extension)
- The script preserves frontmatter but may need manual cleanup
- Google Docs formatting may not translate perfectly to markdown

---

## Alternative: Manual Workflow

If the script doesn't work, you can manually:

1. **Copy article content** from markdown file
2. **Paste into Google Doc** (create new doc)
3. **Share with Louie** for editing
4. **Copy edited content** back
5. **Paste into markdown file** (preserving frontmatter)

But the script is much easier! 🚀

