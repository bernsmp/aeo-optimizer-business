"""
Re-analyze files that failed during initial ingestion.
"""

import json
import os
import time
from tools.content_reader import read_file_content, get_file_metadata
from agents.content_analyzer import ContentAnalyzer
from ingest_content import categorize_content

def reanalyze_failed_files(kb_path: str = "data/ingested_content/knowledge_base.json"):
    """Re-analyze files that had errors."""
    
    # Load knowledge base
    with open(kb_path, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    # Find failed files
    failed_files = []
    for item in kb['content_index']:
        if 'error' in item.get('analysis', {}):
            failed_files.append(item)
    
    if not failed_files:
        print("✅ No failed files found!")
        return
    
    print(f"🔄 Re-analyzing {len(failed_files)} failed files...\n")
    
    analyzer = ContentAnalyzer()
    
    for i, item in enumerate(failed_files, 1):
        file_path = item['file_path']
        file_id = item['file_id']
        
        print(f"[{i}/{len(failed_files)}] Processing: {os.path.basename(file_path)}")
        
        # Read content
        content = read_file_content(file_path)
        if not content:
            print(f"  ⚠️  Could not read file content\n")
            continue
        
        # Get metadata
        metadata = get_file_metadata(file_path)
        
        # Analyze with retry logic
        try:
            analysis = analyzer.analyze_content(content, metadata)
            
            # Update the item
            category = categorize_content(analysis)
            item['category'] = category
            item['analysis'] = analysis
            item['content_preview'] = content[:500]
            
            # Update categories
            if category not in kb['categories']:
                kb['categories'][category] = []
            
            # Remove from old category if it exists
            for cat, items in kb['categories'].items():
                kb['categories'][cat] = [it for it in items if it['file_id'] != file_id]
            
            # Add to new category
            kb['categories'][category].append(item)
            
            # Extract frameworks
            frameworks = analysis.get('frameworks', [])
            for framework in frameworks:
                framework['source_file'] = file_path
                framework['source_file_id'] = file_id
                # Remove old frameworks from this file
                kb['frameworks'] = [f for f in kb['frameworks'] if f.get('source_file_id') != file_id]
                kb['frameworks'].append(framework)
            
            # Extract case studies
            case_studies = analysis.get('case_studies', [])
            for case_study in case_studies:
                case_study['source_file'] = file_path
                case_study['source_file_id'] = file_id
                # Remove old case studies from this file
                kb['case_studies'] = [c for c in kb['case_studies'] if c.get('source_file_id') != file_id]
                kb['case_studies'].append(case_study)
            
            print(f"  ✅ Successfully analyzed\n")
            
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                print(f"  ⏳ Rate limit hit, waiting 60 seconds...")
                time.sleep(60)
                try:
                    analysis = analyzer.analyze_content(content, metadata)
                    category = categorize_content(analysis)
                    item['category'] = category
                    item['analysis'] = analysis
                    item['content_preview'] = content[:500]
                    print(f"  ✅ Successfully analyzed after retry\n")
                except Exception as e2:
                    print(f"  ❌ Still failed: {e2}\n")
            else:
                print(f"  ❌ Error: {e}\n")
        
        # Delay to avoid rate limits
        if i < len(failed_files):
            time.sleep(3)
    
    # Save updated knowledge base
    with open(kb_path, 'w', encoding='utf-8') as f:
        json.dump(kb, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Updated knowledge base saved!")
    print(f"   Total frameworks: {len(kb['frameworks'])}")
    print(f"   Total case studies: {len(kb['case_studies'])}")

if __name__ == "__main__":
    reanalyze_failed_files()

