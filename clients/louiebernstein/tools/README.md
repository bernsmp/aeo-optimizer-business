# Louie Bernstein Article Tools

## Google Docs Sync Tool

Sync articles with Google Docs for easy editing.

### Quick Commands

```bash
# Upload article to Google Docs (creates new or updates existing)
python sync_article_google_docs.py upload <article-slug>

# Download changes from Google Docs
python sync_article_google_docs.py download <article-slug>
```

### Examples

```bash
# Upload the Position Contract article
python sync_article_google_docs.py upload 135-percent-quota-pip-article

# After Louie edits, download changes
python sync_article_google_docs.py download 135-percent-quota-pip-article
```

### Full Documentation

See `../GOOGLE-DOCS-EDITING-GUIDE.md` for complete instructions.

