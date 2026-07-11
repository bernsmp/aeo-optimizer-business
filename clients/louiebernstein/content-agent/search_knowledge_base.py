"""
Search utility for the knowledge base.

Usage:
    python search_knowledge_base.py "sales process"
    python search_knowledge_base.py --framework "5-step"
    python search_knowledge_base.py --case-study
    python search_knowledge_base.py --category frameworks
"""

import json
import sys
import os
from typing import List, Dict

def load_knowledge_base(kb_path: str = "data/ingested_content/knowledge_base.json") -> Dict:
    """Load the knowledge base."""
    if not os.path.exists(kb_path):
        print(f"❌ Knowledge base not found at: {kb_path}")
        print("   Run ingest_content.py first to create the knowledge base.")
        sys.exit(1)
    
    with open(kb_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def search_by_topic(kb: Dict, query: str) -> List[Dict]:
    """Search content by topic."""
    results = []
    query_lower = query.lower()
    
    for item in kb.get('content_index', []):
        analysis = item.get('analysis', {})
        topics = analysis.get('key_topics', [])
        summary = analysis.get('summary', '')
        
        # Check if query matches topics or summary
        if any(query_lower in topic.lower() for topic in topics) or query_lower in summary.lower():
            results.append(item)
    
    return results

def search_frameworks(kb: Dict, query: str = None) -> List[Dict]:
    """Search frameworks."""
    frameworks = kb.get('frameworks', [])
    
    if not query:
        return frameworks
    
    query_lower = query.lower()
    results = []
    
    for framework in frameworks:
        name = framework.get('name', '').lower()
        description = framework.get('description', '').lower()
        
        if query_lower in name or query_lower in description:
            results.append(framework)
    
    return results

def search_case_studies(kb: Dict, query: str = None) -> List[Dict]:
    """Search case studies."""
    case_studies = kb.get('case_studies', [])
    
    if not query:
        return case_studies
    
    query_lower = query.lower()
    results = []
    
    for case_study in case_studies:
        description = case_study.get('description', '').lower()
        result = case_study.get('result', '').lower()
        
        if query_lower in description or query_lower in result:
            results.append(case_study)
    
    return results

def search_by_category(kb: Dict, category: str) -> List[Dict]:
    """Search content by category."""
    return kb.get('categories', {}).get(category, [])

def print_search_results(results: List[Dict], result_type: str = "content"):
    """Print search results in a readable format."""
    if not results:
        print(f"\n❌ No {result_type} found.")
        return
    
    print(f"\n✅ Found {len(results)} {result_type}(s):\n")
    
    for i, result in enumerate(results[:20], 1):  # Show first 20
        print(f"{'='*60}")
        print(f"{i}. ", end="")
        
        if result_type == "frameworks":
            print(f"{result.get('name', 'Unnamed Framework')}")
            print(f"   Type: {result.get('type', 'N/A')}")
            print(f"   Description: {result.get('description', 'N/A')[:200]}")
            if result.get('components'):
                print(f"   Components: {', '.join(result['components'][:5])}")
            print(f"   Source: {result.get('source_file', 'N/A')}")
        
        elif result_type == "case_studies":
            print(f"{result.get('description', 'Unnamed Case Study')[:200]}")
            if result.get('result'):
                print(f"   Result: {result['result']}")
            print(f"   Source: {result.get('source_file', 'N/A')}")
        
        else:  # content
            filename = result.get('file_metadata', {}).get('filename', 'Unknown')
            print(f"{filename}")
            analysis = result.get('analysis', {})
            if analysis.get('summary'):
                print(f"   Summary: {analysis['summary'][:200]}")
            if analysis.get('key_topics'):
                print(f"   Topics: {', '.join(analysis['key_topics'][:5])}")
            print(f"   Category: {result.get('category', 'N/A')}")
            print(f"   File: {result.get('file_path', 'N/A')}")
        
        print()
    
    if len(results) > 20:
        print(f"... and {len(results) - 20} more results\n")

def main():
    """Main search function."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python search_knowledge_base.py <query>")
        print("  python search_knowledge_base.py --framework [query]")
        print("  python search_knowledge_base.py --case-study [query]")
        print("  python search_knowledge_base.py --category <category>")
        print("\nCategories: frameworks, case_studies, training_materials, sales_materials, articles, general")
        sys.exit(1)
    
    # Load knowledge base
    kb = load_knowledge_base()
    
    # Parse arguments
    if sys.argv[1] == "--framework":
        query = sys.argv[2] if len(sys.argv) > 2 else None
        results = search_frameworks(kb, query)
        print_search_results(results, "frameworks")
    
    elif sys.argv[1] == "--case-study":
        query = sys.argv[2] if len(sys.argv) > 2 else None
        results = search_case_studies(kb, query)
        print_search_results(results, "case_studies")
    
    elif sys.argv[1] == "--category":
        if len(sys.argv) < 3:
            print("❌ Please specify a category")
            sys.exit(1)
        category = sys.argv[2]
        results = search_by_category(kb, category)
        print_search_results(results, f"content in '{category}'")
    
    else:
        # General topic search
        query = " ".join(sys.argv[1:])
        results = search_by_topic(kb, query)
        print_search_results(results, "content")

if __name__ == "__main__":
    main()

