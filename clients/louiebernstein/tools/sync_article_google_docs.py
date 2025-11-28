#!/usr/bin/env python3
"""
Sync Louie Bernstein articles with Google Docs for easy editing.

Usage:
    # Upload article to Google Docs (creates new doc or updates existing)
    python sync_article_google_docs.py upload articles/135-percent-quota-pip-article.md
    
    # Download changes from Google Docs back to markdown
    python sync_article_google_docs.py download articles/135-percent-quota-pip-article.md
    
    # Or use the article slug
    python sync_article_google_docs.py upload 135-percent-quota-pip-article
    python sync_article_google_docs.py download 135-percent-quota-pip-article
"""

import sys
import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple

# Add parent directories to path
# Calculate path to Jay Article Writer project
current_file = Path(__file__).resolve()
# Go up from: .../clients/louiebernstein/tools/sync_article_google_docs.py
# To: .../Vibe Projects/
vibe_projects = current_file.parent.parent.parent.parent.parent
jay_writer_path = vibe_projects / "Jay Article Writer"
sys.path.insert(0, str(jay_writer_path))

try:
    from tools.google_drive_integration import GoogleDriveIntegration
except ImportError:
    print("❌ Error: Could not import GoogleDriveIntegration")
    print("   Make sure you're in the correct directory and dependencies are installed")
    sys.exit(1)


def get_article_path(article_identifier: str) -> Optional[Path]:
    """
    Get the full path to an article file.
    
    Args:
        article_identifier: Either a full path, relative path, or slug (filename without .md)
    
    Returns:
        Path object or None if not found
    """
    # If it's already a full path or relative path with .md extension
    if article_identifier.endswith('.md'):
        path = Path(article_identifier)
        if path.is_absolute():
            return path if path.exists() else None
        # Try relative to current directory
        if path.exists():
            return path
        # Try relative to articles directory
        articles_dir = Path(__file__).parent.parent / "articles"
        article_path = articles_dir / article_identifier
        if article_path.exists():
            return article_path
    
    # It's a slug - try to find the file
    articles_dir = Path(__file__).parent.parent / "articles"
    article_path = articles_dir / f"{article_identifier}.md"
    if article_path.exists():
        return article_path
    
    # Try with different variations
    for file in articles_dir.glob(f"{article_identifier}*.md"):
        return file
    
    return None


def get_metadata_path(article_path: Path) -> Path:
    """Get the path to the metadata file for an article."""
    return article_path.parent / f".{article_path.stem}_metadata.json"


def load_metadata(metadata_path: Path) -> dict:
    """Load metadata from file, or return empty dict."""
    if metadata_path.exists():
        with open(metadata_path, 'r') as f:
            return json.load(f)
    return {}


def save_metadata(metadata_path: Path, metadata: dict):
    """Save metadata to file."""
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)


def parse_frontmatter(content: str) -> Tuple[dict, str]:
    """
    Parse frontmatter from markdown content.
    
    Returns:
        Tuple of (frontmatter_dict, content_without_frontmatter)
    """
    frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(frontmatter_pattern, content, re.DOTALL)
    
    if match:
        frontmatter_text = match.group(1)
        body_content = match.group(2)
        
        # Parse YAML-like frontmatter
        frontmatter = {}
        for line in frontmatter_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip().strip('"').strip("'")
        
        return frontmatter, body_content
    
    return {}, content


def combine_frontmatter_and_content(frontmatter: dict, content: str) -> str:
    """Combine frontmatter and content back into markdown format."""
    frontmatter_lines = ['---']
    for key, value in frontmatter.items():
        frontmatter_lines.append(f"{key}: {value}")
    frontmatter_lines.append('---')
    frontmatter_lines.append('')
    
    return '\n'.join(frontmatter_lines) + '\n' + content


def upload_article_to_google_docs(article_path: Path, folder_id: Optional[str] = None) -> bool:
    """
    Upload an article to Google Docs.
    
    Args:
        article_path: Path to the markdown article file
        folder_id: Optional Google Drive folder ID
    
    Returns:
        True if successful, False otherwise
    """
    print(f"📤 Uploading article to Google Docs: {article_path.name}")
    
    # Read article content
    with open(article_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse frontmatter and body
    frontmatter, body_content = parse_frontmatter(content)
    
    # Initialize Google Drive integration
    # Use credentials from Jay Article Writer directory
    try:
        credentials_file = str(jay_writer_path / "credentials.json")
        token_file = str(jay_writer_path / "token.json")
        drive = GoogleDriveIntegration(
            credentials_file=credentials_file,
            token_file=token_file
        )
    except Exception as e:
        print(f"❌ Error initializing Google Drive: {e}")
        print("   Make sure credentials.json is set up correctly")
        return False
    
    # Get or create folder
    if not folder_id:
        folder_id = os.environ.get('LOUIE_GOOGLE_DRIVE_FOLDER_ID')
        if not folder_id:
            # Try to get/create a "Louie Bernstein Articles" folder
            folder_id = drive.get_or_create_folder("Louie Bernstein Articles")
    
    # Get article title for doc name
    doc_name = frontmatter.get('title', article_path.stem)
    if len(doc_name) > 100:
        doc_name = doc_name[:97] + "..."
    
    # Check if we already have a doc ID in metadata
    metadata_path = get_metadata_path(article_path)
    metadata = load_metadata(metadata_path)
    existing_doc_id = metadata.get('google_doc_id')
    
    if existing_doc_id:
        # Update existing doc
        print(f"📝 Updating existing Google Doc...")
        doc_link = drive.update_google_doc(
            existing_doc_id,
            body_content,  # Just the body, not frontmatter
            doc_name=doc_name,
            add_version=False
        )
        
        if doc_link:
            metadata['google_doc_link'] = doc_link
            metadata['last_upload'] = datetime.now().isoformat()
            save_metadata(metadata_path, metadata)
            print(f"✅ Updated Google Doc: {doc_link}")
            return True
        else:
            print("❌ Failed to update Google Doc")
            return False
    else:
        # Create new doc
        print(f"📄 Creating new Google Doc...")
        result = drive.create_google_doc(body_content, doc_name, folder_id)
        
        if result:
            doc_id, doc_link = result
            metadata['google_doc_id'] = doc_id
            metadata['google_doc_link'] = doc_link
            metadata['article_path'] = str(article_path)
            metadata['last_upload'] = datetime.now().isoformat()
            save_metadata(metadata_path, metadata)
            print(f"✅ Created Google Doc: {doc_link}")
            print(f"\n💡 Louie can now edit this doc. When ready, run:")
            print(f"   python sync_article_google_docs.py download {article_path.stem}")
            return True
        else:
            print("❌ Failed to create Google Doc")
            return False


def download_article_from_google_docs(article_path: Path) -> bool:
    """
    Download changes from Google Docs and merge with local markdown file.
    
    Args:
        article_path: Path to the markdown article file
    
    Returns:
        True if successful, False otherwise
    """
    print(f"📥 Downloading article from Google Docs: {article_path.name}")
    
    # Load metadata to get doc ID
    metadata_path = get_metadata_path(article_path)
    metadata = load_metadata(metadata_path)
    
    doc_id = metadata.get('google_doc_id')
    if not doc_id:
        print("❌ No Google Doc ID found in metadata")
        print("   Run 'upload' command first to create the Google Doc")
        return False
    
    # Read current article to preserve frontmatter
    with open(article_path, 'r', encoding='utf-8') as f:
        current_content = f.read()
    
    frontmatter, _ = parse_frontmatter(current_content)
    
    # Initialize Google Drive integration
    # Use credentials from Jay Article Writer directory
    try:
        current_file = Path(__file__).resolve()
        vibe_projects = current_file.parent.parent.parent.parent.parent
        jay_writer_path = vibe_projects / "Jay Article Writer"
        credentials_file = str(jay_writer_path / "credentials.json")
        token_file = str(jay_writer_path / "token.json")
        drive = GoogleDriveIntegration(
            credentials_file=credentials_file,
            token_file=token_file
        )
    except Exception as e:
        print(f"❌ Error initializing Google Drive: {e}")
        return False
    
    # Download content from Google Docs
    print(f"📥 Pulling content from Google Doc...")
    doc_content = drive.read_file(doc_id)
    
    if not doc_content:
        print("❌ Failed to download content from Google Docs")
        return False
    
    # Clean up the content (remove excessive line breaks, etc.)
    cleaned_content = clean_google_doc_content(doc_content)
    
    # Combine with frontmatter
    updated_content = combine_frontmatter_and_content(frontmatter, cleaned_content)
    
    # Backup original file
    backup_path = article_path.with_suffix('.md.backup')
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(current_content)
    print(f"💾 Backup saved to: {backup_path.name}")
    
    # Write updated content
    with open(article_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    # Update metadata
    metadata['last_download'] = datetime.now().isoformat()
    save_metadata(metadata_path, metadata)
    
    print(f"✅ Downloaded and merged changes to: {article_path.name}")
    print(f"   Content length: {len(cleaned_content)} characters")
    
    return True


def clean_google_doc_content(content: str) -> str:
    """
    Clean up content downloaded from Google Docs.
    Removes excessive line breaks and restores markdown structure.
    """
    lines = content.split('\n')
    cleaned_lines = []
    prev_empty = False
    
    for line in lines:
        stripped = line.strip()
        
        # Skip excessive empty lines
        if not stripped:
            if not prev_empty:
                cleaned_lines.append('')
                prev_empty = True
            continue
        
        prev_empty = False
        cleaned_lines.append(stripped)
    
    # Join lines and clean up
    cleaned = '\n'.join(cleaned_lines)
    
    # Remove excessive blank lines (more than 2 consecutive)
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    
    return cleaned.strip()


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1].lower()
    article_identifier = sys.argv[2]
    
    # Get article path
    article_path = get_article_path(article_identifier)
    if not article_path:
        print(f"❌ Article not found: {article_identifier}")
        print("   Make sure the file exists in the articles directory")
        sys.exit(1)
    
    if command == 'upload':
        folder_id = sys.argv[3] if len(sys.argv) > 3 else None
        success = upload_article_to_google_docs(article_path, folder_id)
        sys.exit(0 if success else 1)
    
    elif command == 'download':
        success = download_article_from_google_docs(article_path)
        sys.exit(0 if success else 1)
    
    else:
        print(f"❌ Unknown command: {command}")
        print("   Use 'upload' or 'download'")
        sys.exit(1)


if __name__ == "__main__":
    main()

