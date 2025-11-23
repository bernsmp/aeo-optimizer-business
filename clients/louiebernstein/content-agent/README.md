# Louie Bernstein Content Agent

A comprehensive content ingestion and analysis system for organizing, categorizing, and searching Louie's content library.

## Features

- **Google Drive Integration** - Automatically downloads and processes content from Google Drive folders
- **Content Categorization** - Automatically categorizes content (frameworks, case studies, training materials, etc.)
- **Framework Extraction** - Identifies and extracts all frameworks, methodologies, and structured systems
- **Case Study Tracking** - Extracts case studies, examples, and results
- **Tone Analysis** - Analyzes writing style and tone of voice
- **Semantic Search** - Optimized for finding content by topic, framework, or concept
- **Knowledge Base** - Creates a searchable knowledge base of all content

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Google Drive API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable the **Google Drive API**
4. Create OAuth 2.0 credentials (Desktop app)
5. Download `credentials.json` and place in the `content-agent` directory

### 3. Environment Variables

Create a `.env` file:

```bash
GOOGLE_API_KEY=your_gemini_api_key_here
```

## Usage

### Basic Ingestion

```bash
# Ingest from a folder by name
python ingest_content.py "Louie Content"

# Ingest from a folder by ID
python ingest_content.py "1a2b3c4d5e6f7g8h9i0j"

# Specify output directory
python ingest_content.py "Louie Content" data/my_content
```

### What It Does

1. **Downloads** all files from the Google Drive folder (PDFs, Word docs, text files)
2. **Reads** content from each file
3. **Analyzes** each piece of content for:
   - Content type
   - Key topics
   - Frameworks
   - Case studies
   - Tone of voice
   - Key messages
   - Actionable insights
4. **Categorizes** content automatically
5. **Creates** a searchable knowledge base

### Output Structure

```
data/ingested_content/
├── raw_files/              # Original downloaded files
├── knowledge_base.json     # Complete knowledge base (JSON)
└── SUMMARY_REPORT.md       # Human-readable summary
```

## Knowledge Base Structure

The `knowledge_base.json` file contains:

```json
{
  "total_files": 150,
  "categories": {
    "frameworks": [...],
    "case_studies": [...],
    "training_materials": [...],
    "sales_materials": [...],
    "articles": [...]
  },
  "frameworks": [
    {
      "name": "Framework Name",
      "type": "process/methodology/model",
      "description": "...",
      "components": ["step1", "step2"],
      "source_file": "path/to/file.pdf"
    }
  ],
  "case_studies": [
    {
      "description": "...",
      "result": "...",
      "source_file": "path/to/file.pdf"
    }
  ],
  "content_index": [
    {
      "file_id": "...",
      "category": "frameworks",
      "analysis": {...},
      "content_preview": "..."
    }
  ]
}
```

## Searching the Knowledge Base

### Find Frameworks

```python
import json

with open('data/ingested_content/knowledge_base.json') as f:
    kb = json.load(f)

# Find all frameworks
for framework in kb['frameworks']:
    print(f"{framework['name']}: {framework['description']}")
```

### Find Content by Topic

```python
# Search for content containing a topic
topic = "sales process"
for item in kb['content_index']:
    topics = item['analysis'].get('key_topics', [])
    if any(topic.lower() in t.lower() for t in topics):
        print(f"Found in: {item['file_metadata']['filename']}")
```

### Find Case Studies

```python
# Find all case studies
for case_study in kb['case_studies']:
    print(f"{case_study['description']}")
    if case_study.get('result'):
        print(f"  Result: {case_study['result']}")
```

## Next Steps

1. **Semantic Search** - Add embeddings for better semantic search
2. **Content Recommendations** - Suggest related content
3. **Framework Library** - Build a searchable framework library
4. **Tone Consistency** - Analyze tone across all content for consistency
5. **Content Gaps** - Identify missing topics or frameworks

## Troubleshooting

### "Credentials file not found"
- Make sure `credentials.json` is in the `content-agent` directory
- Download it from Google Cloud Console

### "Folder not found"
- Check the folder name is correct
- Or use the folder ID directly

### "Error reading file"
- Some files may be corrupted or in unsupported formats
- The script will skip these and continue

## Support

For issues or questions, check the error messages in the console output.

