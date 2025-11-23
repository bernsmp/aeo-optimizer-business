# Quick Start Guide

## Setup (5 minutes)

### 1. Install Dependencies

```bash
cd content-agent
pip install -r requirements.txt
```

### 2. Google Drive API Setup

1. Go to https://console.cloud.google.com/
2. Create/select a project
3. Enable "Google Drive API"
4. Create OAuth 2.0 credentials:
   - Type: Desktop app
   - Name: "Louie Content Agent"
5. Download `credentials.json` → save to `content-agent/` folder

### 3. Get Gemini API Key

1. Go to https://aistudio.google.com/app/apikey
2. Create API key
3. Add to `.env` file:

```bash
GOOGLE_API_KEY=your_key_here
```

## Usage

### Find Your Google Drive Folder

1. Open Google Drive
2. Find the folder with Louie's content
3. Right-click → "Get link" → Copy the folder ID (the long string)
   OR just use the folder name

### Run Ingestion

```bash
# Option 1: Use folder name
python ingest_content.py "Louie's Content Folder"

# Option 2: Use folder ID
python ingest_content.py "1a2b3c4d5e6f7g8h9i0j"
```

### First Run

- Browser will open for Google authentication
- Grant permissions
- Token saved for future runs

## Output

After ingestion, you'll have:

- `data/ingested_content/knowledge_base.json` - Complete searchable database
- `data/ingested_content/SUMMARY_REPORT.md` - Human-readable summary
- `data/ingested_content/raw_files/` - All downloaded files

## What Gets Extracted

✅ **Frameworks** - All methodologies, processes, systems  
✅ **Case Studies** - Client stories, examples, results  
✅ **Tone of Voice** - Writing style analysis  
✅ **Key Topics** - Main subjects covered  
✅ **Actionable Insights** - Specific advice and steps  
✅ **Data/Statistics** - Numbers and metrics  

## Next: Search & Use

See `README.md` for examples of searching the knowledge base.

