"""
Content Reader - Handles reading various file formats
"""

import os
import docx
import pypdf
from typing import Optional, Dict

def read_file_content(filepath: str) -> Optional[str]:
    """
    Smart reader for .docx, .pdf, .txt, .md files.
    
    Args:
        filepath: Path to the file
    
    Returns:
        File content as string, or None if error
    """
    if not os.path.exists(filepath):
        print(f"⚠️ File not found: {filepath}")
        return None
    
    ext = os.path.splitext(filepath)[1].lower()
    
    try:
        if ext == '.docx':
            doc = docx.Document(filepath)
            return "\n".join([para.text for para in doc.paragraphs])
        elif ext == '.pdf':
            reader = pypdf.PdfReader(filepath)
            return "\n".join([page.extract_text() for page in reader.pages])
        elif ext in ['.txt', '.md']:
            with open(filepath, "r", encoding="utf-8", errors='ignore') as f:
                return f.read()
        else:
            print(f"⚠️ Unsupported file type: {ext}")
            return None
    except Exception as e:
        print(f"⚠️ Error reading {filepath}: {e}")
        return None

def get_file_metadata(filepath: str) -> Dict:
    """
    Get metadata about a file.
    
    Args:
        filepath: Path to the file
    
    Returns:
        Dictionary with file metadata
    """
    stat = os.stat(filepath)
    return {
        "filename": os.path.basename(filepath),
        "filepath": filepath,
        "size_bytes": stat.st_size,
        "extension": os.path.splitext(filepath)[1].lower(),
        "modified_time": stat.st_mtime
    }

