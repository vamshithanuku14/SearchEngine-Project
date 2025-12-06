#!/usr/bin/env python3
"""
Enhance the existing HTML files with better content extraction and fix metadata.
"""

import os
import json
import pickle
from bs4 import BeautifulSoup
from common.config import Config
from common.logger import setup_logger

logger = setup_logger(__name__)

def enhance_html_files():
    """Add better content extraction to existing HTML files."""
    config = Config()
    raw_html_dir = config.get('paths.data_raw')
    index_path = os.path.join(config.get('paths.data_index'), 'inverted_index.json')
    tfidf_path = os.path.join(config.get('paths.data_index'), 'tfidf_vectors.pkl')
    
    if not os.path.exists(index_path):
        print(" Index file not found")
        return
    
    # Load the index
    with open(index_path, 'r', encoding='utf-8') as f:
        index_data = json.load(f)
    
    print(" Enhancing content extraction and fixing metadata...")
    enhanced_count = 0
    
    for filename in os.listdir(raw_html_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(raw_html_dir, filename)
            document_id = filename.replace('.html', '')
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # Parse HTML with BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Extract title if not present
                title = soup.find('title')
                title_text = title.get_text().strip() if title else f"Document {document_id}"
                
                # Remove unwanted elements
                for element in soup(["script", "style", "nav", "header", "footer", "aside", "meta", "link"]):
                    element.decompose()
                
                # Try to find main content
                article = (soup.find('article') or 
                          soup.find('div', class_=['content', 'main', 'body', 'mw-body']) or
                          soup.find('div', id=['content', 'main', 'body', 'mw-content-text']))
                
                if article:
                    content = article.get_text()
                else:
                    # Fallback to body content
                    body = soup.find('body')
                    content = body.get_text() if body else soup.get_text()
                
                # Clean up the text
                lines = (line.strip() for line in content.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                clean_content = ' '.join(chunk for chunk in chunks if chunk)
                
                # Update metadata in index
                if document_id in index_data['document_metadata']:
                    # Fix URL
                    current_url = index_data['document_metadata'][document_id].get('url', '')
                    if not current_url or current_url.startswith('file://'):
                        # Create proper Wikipedia URL from title
                        if 'Wikipedia' in title_text:
                            topic = title_text.split(' - ')[0].lower().replace(' ', '_')
                            new_url = f"https://en.wikipedia.org/wiki/{topic}"
                        else:
                            new_url = f"https://example.com/document/{document_id}"
                        index_data['document_metadata'][document_id]['url'] = new_url
                    
                    # Update title if it's generic
                    if index_data['document_metadata'][document_id].get('title', '').startswith('Document'):
                        index_data['document_metadata'][document_id]['title'] = title_text
                    
                    # Add content
                    index_data['document_metadata'][document_id]['content'] = clean_content
                    index_data['document_metadata'][document_id]['enhanced'] = True
                    
                    enhanced_count += 1
                    print(f" Enhanced: {filename} -> {title_text}")
                
            except Exception as e:
                print(f" Error processing {filename}: {e}")
    
    # Save updated index
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
    
    print(f" Enhanced {enhanced_count} documents!")
    
    # Also update TF-IDF vectors if they exist
    if os.path.exists(tfidf_path):
        try:
            with open(tfidf_path, 'rb') as f:
                tfidf_data = pickle.load(f)
            
            # The TF-IDF vectors don't need updating, just confirm they exist
            print(f" TF-IDF vectors verified: {len(tfidf_data.get('document_vectors', {}))} documents")
            
        except Exception as e:
            print(f" Error with TF-IDF vectors: {e}")

def display_enhanced_results():
    """Show what the enhanced results will look like."""
    index_path = os.path.join('data', 'index', 'inverted_index.json')
    
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            index_data = json.load(f)
        
        print("\n ENHANCED DOCUMENTS PREVIEW:")
        print("=" * 60)
        
        for doc_id, metadata in list(index_data['document_metadata'].items())[:3]:  # Show first 3
            print(f"\n {metadata.get('title', 'Untitled')}")
            print(f"    URL: {metadata.get('url', 'N/A')}")
            print(f"    Content preview: {metadata.get('content', 'N/A')[:100]}...")
            print(f"    Word count: {metadata.get('word_count', 0)}")

if __name__ == "__main__":
    print(" ENHANCING SEARCH ENGINE CONTENT")
    print("=" * 60)
    
    enhance_html_files()
    display_enhanced_results()
    
    print("\n Next steps:")
    print("1. Restart the search engine: python run_processor.py")
    print("2. Test searches with improved content and proper URLs")
    print("3. Enjoy your fully functional search engine! 🎉")
