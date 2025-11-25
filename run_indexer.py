#!/usr/bin/env python3
"""
Main script to run the indexer.
"""

import os
import sys
import json
import logging

# Add src to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

try:
    from common.config import Config
    from common.logger import setup_logger
    from src.indexer.inverted_index import InvertedIndex
    from src.indexer.tfidf_calculator import TFIDFCalculator
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all dependencies are installed and the project structure is correct.")
    sys.exit(1)

logger = setup_logger(__name__)

def load_documents_from_raw_html(data_dir: str):
    """Load documents from raw HTML files."""
    documents = []
    
    if not os.path.exists(data_dir):
        logger.warning(f"Raw HTML directory not found: {data_dir}")
        return documents
    
    for filename in os.listdir(data_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(data_dir, filename)
            document_id = filename.replace('.html', '')
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # Extract title from HTML
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')
                title = soup.find('title')
                title_text = title.get_text().strip() if title else f"Document {document_id}"
                
                # Extract clean text
                for script in soup(["script", "style"]):
                    script.decompose()
                text_content = soup.get_text()
                lines = (line.strip() for line in text_content.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                clean_content = ' '.join(chunk for chunk in chunks if chunk)
                
                documents.append({
                    'document_id': document_id,
                    'content': clean_content,
                    'metadata': {
                        'url': f"file://{filepath}",
                        'title': title_text,
                        'filename': filename
                    }
                })
                
                logger.debug(f"Loaded document: {document_id} - {title_text}")
                
            except Exception as e:
                logger.error(f"Error reading {filepath}: {str(e)}")
    
    return documents

def main():
    """Main function to run the indexer."""
    try:
        config = Config()
        
        # Initialize indexer
        inverted_index = InvertedIndex()
        
        # Load documents from raw HTML
        raw_html_dir = config.get('paths.data_raw')
        logger.info(f"Loading documents from {raw_html_dir}...")
        
        documents = load_documents_from_raw_html(raw_html_dir)
        
        if not documents:
            logger.warning("No documents found to index")
            print("No HTML documents found in data/raw_html/")
            print("Please run the crawler first to download web pages.")
            return
        
        # Add documents to index
        logger.info(f"Indexing {len(documents)} documents...")
        
        for doc in documents:
            inverted_index.add_document(
                doc['document_id'],
                doc['content'],
                doc['metadata']
            )
        
        # Calculate statistics
        stats = inverted_index.get_statistics()
        logger.info(f"Indexing completed: {stats}")
        
        # Save inverted index
        index_path = os.path.join(config.get('paths.data_index'), 'inverted_index.json')
        inverted_index.save_index(index_path)
        print(f"Inverted index saved to: {index_path}")
        
        # Calculate and save TF-IDF vectors
        logger.info("Calculating TF-IDF vectors...")
        tfidf_calculator = TFIDFCalculator(inverted_index)
        tfidf_calculator.calculate_tfidf()
        
        tfidf_path = os.path.join(config.get('paths.data_index'), 'tfidf_vectors.pkl')
        tfidf_calculator.save_tfidf_vectors(tfidf_path)
        print(f"TF-IDF vectors saved to: {tfidf_path}")
        
        print(f"\nIndexing completed successfully!")
        print(f"Documents indexed: {stats['total_documents']}")
        print(f"Vocabulary size: {stats['vocabulary_size']}")
        print(f"Total terms: {stats['total_terms']}")
        
    except Exception as e:
        logger.error(f"Error running indexer: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()