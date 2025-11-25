#!/usr/bin/env python3
"""
Check the current status of the search engine project.
"""

import os
import json

def check_data_files():
    """Check what data files exist."""
    print("📁 Data File Status")
    print("=" * 40)
    
    # Check raw HTML files
    raw_html_dir = 'data/raw_html'
    if os.path.exists(raw_html_dir):
        html_files = [f for f in os.listdir(raw_html_dir) if f.endswith('.html')]
        print(f"Raw HTML files: {len(html_files)}")
        for file in html_files[:5]:  # Show first 5 files
            filepath = os.path.join(raw_html_dir, file)
            file_size = os.path.getsize(filepath)
            print(f"  📄 {file} ({file_size} bytes)")
        if len(html_files) > 5:
            print(f"  ... and {len(html_files) - 5} more")
    else:
        print("Raw HTML directory: ❌ Not found")
    
    # Check index files
    index_dir = 'data/index'
    if os.path.exists(index_dir):
        index_files = os.listdir(index_dir)
        print(f"Index files: {len(index_files)}")
        for file in index_files:
            filepath = os.path.join(index_dir, file)
            file_size = os.path.getsize(filepath)
            print(f"  📊 {file} ({file_size} bytes)")
    else:
        print("Index directory: ❌ Not found")

def check_index_content():
    """Check if the index has content."""
    index_path = 'data/index/inverted_index.json'
    if os.path.exists(index_path):
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
            
            print(f"\n📊 Index Statistics")
            print("=" * 40)
            print(f"Total documents: {index_data.get('total_documents', 0)}")
            print(f"Vocabulary size: {len(index_data.get('vocabulary', []))}")
            
            # Show sample terms
            vocabulary = index_data.get('vocabulary', [])
            if vocabulary:
                print(f"Sample terms: {', '.join(vocabulary[:10])}")
            
            # Show document titles
            print(f"\n📄 Documents in index:")
            for doc_id, metadata in index_data.get('document_metadata', {}).items():
                title = metadata.get('title', 'Unknown')
                print(f"  - {doc_id}: {title}")
            
        except Exception as e:
            print(f"Error reading index: {e}")
    else:
        print("\n❌ No index file found")

if __name__ == "__main__":
    print("🔍 Search Engine Project Status")
    print("=" * 50)
    
    check_data_files()
    check_index_content()
    
    print("\n🎯 Next Steps:")
    raw_html_dir = 'data/raw_html'
    if os.path.exists(raw_html_dir) and len([f for f in os.listdir(raw_html_dir) if f.endswith('.html')]) > 0:
        print("1. ✅ HTML files exist - Ready for indexing")
        index_path = 'data/index/inverted_index.json'
        if os.path.exists(index_path):
            print("2. ✅ Index exists - Ready to start search engine")
            print("3. Run: python run_processor.py")
        else:
            print("2. ❌ No index - Run: python run_indexer.py")
    else:
        print("1. ❌ No HTML files - Run crawler or create samples")
        print("   Option A: python run_crawler.py")
        print("   Option B: python create_guaranteed_samples.py")