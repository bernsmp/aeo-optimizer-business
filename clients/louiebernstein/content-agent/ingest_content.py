"""
Main content ingestion script for Louie Bernstein's Google Drive content.

Usage:
    python ingest_content.py <google_drive_folder_id_or_name> [output_dir]
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List
from tqdm import tqdm

from tools.google_drive_integration import GoogleDriveIntegration
from tools.content_reader import read_file_content, get_file_metadata
from agents.content_analyzer import ContentAnalyzer

def categorize_content(analysis: Dict) -> str:
    """Categorize content based on analysis."""
    content_type = analysis.get("content_type", "").lower()
    
    if "framework" in content_type or analysis.get("frameworks"):
        return "frameworks"
    elif "case study" in content_type or "example" in content_type or analysis.get("case_studies"):
        return "case_studies"
    elif "training" in content_type or "guide" in content_type:
        return "training_materials"
    elif "script" in content_type or "email" in content_type:
        return "sales_materials"
    elif "article" in content_type or "blog" in content_type:
        return "articles"
    else:
        return "general"

def ingest_from_drive(folder_id_or_name: str, output_dir: str = "data/ingested_content"):
    """
    Ingest content from Google Drive folder.
    
    Args:
        folder_id_or_name: Google Drive folder ID or name
        output_dir: Local directory to save ingested content
    """
    print(f"🚀 Starting content ingestion from: {folder_id_or_name}")
    
    # Initialize components
    drive = GoogleDriveIntegration()
    analyzer = ContentAnalyzer()
    
    # Find folder
    if len(folder_id_or_name) > 30:  # Likely a folder ID
        folder_id = folder_id_or_name
    else:
        folder_id = drive.find_folder(folder_id_or_name)
        if not folder_id:
            print(f"❌ Folder not found: {folder_id_or_name}")
            return
    
    print(f"✅ Found folder: {folder_id}")
    
    # Download files
    download_dir = os.path.join(output_dir, "raw_files")
    print(f"📥 Downloading files to: {download_dir}")
    
    downloaded_files = drive.download_folder(
        folder_id=folder_id,
        local_path=download_dir,
        file_filter=['.pdf', '.docx', '.txt', '.md']
    )
    
    print(f"✅ Downloaded {len(downloaded_files)} files")
    
    # Process and analyze files
    print("\n📊 Analyzing content...")
    
    knowledge_base = {
        "ingested_at": str(Path().cwd()),
        "total_files": len(downloaded_files),
        "categories": {},
        "frameworks": [],
        "case_studies": [],
        "content_index": []
    }
    
    for file_id, file_path in tqdm(downloaded_files.items(), desc="Processing files"):
        # Read content
        content = read_file_content(file_path)
        if not content:
            continue
        
        # Get metadata
        metadata = get_file_metadata(file_path)
        
        # Analyze content with rate limiting
        import time
        try:
            analysis = analyzer.analyze_content(content, metadata)
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                print(f"\n⏳ Rate limit hit, waiting 60 seconds...")
                time.sleep(60)
                analysis = analyzer.analyze_content(content, metadata)
            else:
                raise
        
        # Small delay to avoid rate limits
        time.sleep(2)
        
        # Categorize
        category = categorize_content(analysis)
        
        # Store in knowledge base
        content_entry = {
            "file_id": file_id,
            "file_path": file_path,
            "category": category,
            "analysis": analysis,
            "content_preview": content[:500]  # First 500 chars
        }
        
        knowledge_base["content_index"].append(content_entry)
        
        # Organize by category
        if category not in knowledge_base["categories"]:
            knowledge_base["categories"][category] = []
        knowledge_base["categories"][category].append(content_entry)
        
        # Extract frameworks
        frameworks = analysis.get("frameworks", [])
        for framework in frameworks:
            framework["source_file"] = file_path
            framework["source_file_id"] = file_id
            knowledge_base["frameworks"].append(framework)
        
        # Extract case studies
        case_studies = analysis.get("case_studies", [])
        for case_study in case_studies:
            case_study["source_file"] = file_path
            case_study["source_file_id"] = file_id
            knowledge_base["case_studies"].append(case_study)
    
    # Save knowledge base
    kb_path = os.path.join(output_dir, "knowledge_base.json")
    os.makedirs(os.path.dirname(kb_path), exist_ok=True)
    
    with open(kb_path, 'w', encoding='utf-8') as f:
        json.dump(knowledge_base, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Knowledge base saved to: {kb_path}")
    print(f"\n📊 Summary:")
    print(f"   Total files: {knowledge_base['total_files']}")
    print(f"   Categories: {list(knowledge_base['categories'].keys())}")
    print(f"   Frameworks found: {len(knowledge_base['frameworks'])}")
    print(f"   Case studies found: {len(knowledge_base['case_studies'])}")
    
    # Generate summary report
    generate_summary_report(knowledge_base, output_dir)
    
    return knowledge_base

def generate_summary_report(kb: Dict, output_dir: str):
    """Generate a human-readable summary report."""
    report_path = os.path.join(output_dir, "SUMMARY_REPORT.md")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Content Ingestion Summary Report\n\n")
        f.write(f"**Generated:** {kb.get('ingested_at', 'Unknown')}\n\n")
        
        f.write("## Overview\n\n")
        f.write(f"- **Total Files Processed:** {kb['total_files']}\n")
        f.write(f"- **Frameworks Found:** {len(kb['frameworks'])}\n")
        f.write(f"- **Case Studies Found:** {len(kb['case_studies'])}\n\n")
        
        f.write("## Content Categories\n\n")
        for category, items in kb['categories'].items():
            f.write(f"### {category.replace('_', ' ').title()}\n")
            f.write(f"- **Count:** {len(items)}\n")
            f.write(f"- **Files:**\n")
            for item in items[:10]:  # Show first 10
                filename = item.get('file_metadata', {}).get('filename', item.get('file_path', 'Unknown'))
                f.write(f"  - {filename}\n")
            if len(items) > 10:
                f.write(f"  - ... and {len(items) - 10} more\n")
            f.write("\n")
        
        f.write("## Frameworks\n\n")
        for i, framework in enumerate(kb['frameworks'][:20], 1):  # Show first 20
            f.write(f"### {i}. {framework.get('name', 'Unnamed Framework')}\n")
            f.write(f"- **Type:** {framework.get('type', 'N/A')}\n")
            f.write(f"- **Description:** {framework.get('description', 'N/A')}\n")
            if framework.get('components'):
                f.write(f"- **Components:** {', '.join(framework['components'])}\n")
            f.write(f"- **Source:** {framework.get('source_file', 'N/A')}\n\n")
        
        if len(kb['frameworks']) > 20:
            f.write(f"... and {len(kb['frameworks']) - 20} more frameworks\n\n")
        
        f.write("## Case Studies\n\n")
        for i, case_study in enumerate(kb['case_studies'][:20], 1):  # Show first 20
            f.write(f"### {i}. {case_study.get('description', 'Unnamed Case Study')}\n")
            if case_study.get('result'):
                f.write(f"- **Result:** {case_study['result']}\n")
            f.write(f"- **Source:** {case_study.get('source_file', 'N/A')}\n\n")
        
        if len(kb['case_studies']) > 20:
            f.write(f"... and {len(kb['case_studies']) - 20} more case studies\n\n")
    
    print(f"✅ Summary report saved to: {report_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ingest_content.py <google_drive_folder_id_or_name> [output_dir]")
        print("\nExample:")
        print("  python ingest_content.py 'Louie Content'")
        print("  python ingest_content.py '1a2b3c4d5e6f7g8h9i0j' data/my_content")
        sys.exit(1)
    
    folder_id_or_name = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "data/ingested_content"
    
    ingest_from_drive(folder_id_or_name, output_dir)

