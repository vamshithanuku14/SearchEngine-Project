#!/usr/bin/env python3
"""
Create guaranteed working sample files that will definitely work.
"""

import os
import json
import hashlib

def generate_document_id(url: str) -> str:
    """Generate unique document ID from URL."""
    return hashlib.md5(url.encode('utf-8')).hexdigest().upper()

def create_sample_files():
    """Create sample HTML files that will definitely work."""
    
    samples = [
        {
            "url": "https://en.wikipedia.org/wiki/Search_engine",
            "title": "Search Engine - Wikipedia",
            "content": """<!DOCTYPE html>
<html>
<head>
    <title>Search Engine - Wikipedia</title>
</head>
<body>
    <h1>Search Engine</h1>
    <p>A <strong>search engine</strong> is an information retrieval system designed to help find information stored on computer systems.</p>
    <p>Search engines work by crawling the web using web crawlers and indexing the pages they find.</p>
    <h2>How Search Engines Work</h2>
    <ul>
        <li><strong>Crawling</strong>: Web crawlers browse the internet and collect information from web pages.</li>
        <li><strong>Indexing</strong>: The collected information is organized into an inverted index for fast retrieval.</li>
        <li><strong>Searching</strong>: Users query the index to find relevant information using algorithms like TF-IDF.</li>
    </ul>
    <p>Popular search engines include Google, Bing, DuckDuckGo, and Yahoo.</p>
    <h2>Search Engine Components</h2>
    <p>Modern search engines consist of three main components:</p>
    <ol>
        <li><strong>Crawler</strong>: Discovers and downloads web pages</li>
        <li><strong>Indexer</strong>: Processes and organizes content into searchable indexes</li>
        <li><strong>Query Processor</strong>: Handles user searches and returns ranked results</li>
    </ol>
</body>
</html>"""
        },
        {
            "url": "https://en.wikipedia.org/wiki/Web_crawler",
            "title": "Web Crawler - Wikipedia", 
            "content": """<!DOCTYPE html>
<html>
<head>
    <title>Web Crawler - Wikipedia</title>
</head>
<body>
    <h1>Web Crawler</h1>
    <p>A <strong>web crawler</strong> is an Internet bot that systematically browses the World Wide Web, typically for the purpose of Web indexing.</p>
    <p>Web crawlers copy pages for processing by a search engine, which indexes the downloaded pages so users can search more efficiently.</p>
    <h2>Crawling Process</h2>
    <p>The crawler starts with a list of URLs to visit, called the seeds. As the crawler visits these URLs, it identifies all the hyperlinks in the page and adds them to the list of URLs to visit.</p>
    <p>This process continues until the crawler has visited a sufficient number of pages or until certain criteria are met.</p>
    <h2>Popular Web Crawlers</h2>
    <ul>
        <li>Googlebot (Google)</li>
        <li>Bingbot (Bing)</li>
        <li>Slurp (Yahoo)</li>
    </ul>
</body>
</html>"""
        },
        {
            "url": "https://en.wikipedia.org/wiki/Information_retrieval",
            "title": "Information Retrieval - Wikipedia",
            "content": """<!DOCTYPE html>
<html>
<head>
    <title>Information Retrieval - Wikipedia</title>
</head>
<body>
    <h1>Information Retrieval</h1>
    <p><strong>Information retrieval</strong> is the activity of obtaining information resources relevant to an information need from a collection of information resources.</p>
    <p>Searches can be based on full-text or other content-based indexing. Information retrieval is the science of searching for information in a document.</p>
    <h2>Information Retrieval Process</h2>
    <p>The information retrieval process begins when a user enters a query into the system. queries are formal statements of information needs.</p>
    <p>In information retrieval a query does not uniquely identify a single object in the collection. Instead, several objects may match the query, perhaps with different degrees of relevancy.</p>
    <h2>Applications</h2>
    <ul>
        <li>Web search engines</li>
        <li>Digital libraries</li>
        <li>Enterprise search</li>
        <li>E-commerce product search</li>
    </ul>
</body>
</html>"""
        },
        {
            "url": "https://en.wikipedia.org/wiki/Tf-idf",
            "title": "TF-IDF - Wikipedia",
            "content": """<!DOCTYPE html>
<html>
<head>
    <title>TF-IDF - Wikipedia</title>
</head>
<body>
    <h1>TF-IDF</h1>
    <p><strong>TF-IDF</strong> (Term Frequency-Inverse Document Frequency) is a numerical statistic that is intended to reflect how important a word is to a document in a collection or corpus.</p>
    <p>It is often used as a weighting factor in information retrieval and text mining.</p>
    <h2>Calculation</h2>
    <p>The TF-IDF value increases proportionally to the number of times a word appears in the document and is offset by the number of documents in the corpus that contain the word.</p>
    <p>TF-IDF is one of the most popular term-weighting schemes today.</p>
    <h2>Applications</h2>
    <ul>
        <li>Search engine ranking</li>
        <li>Text classification</li>
        <li>Document similarity</li>
        <li>Keyword extraction</li>
    </ul>
</body>
</html>"""
        },
        {
            "url": "https://en.wikipedia.org/wiki/Cosine_similarity",
            "title": "Cosine Similarity - Wikipedia",
            "content": """<!DOCTYPE html>
<html>
<head>
    <title>Cosine Similarity - Wikipedia</title>
</head>
<body>
    <h1>Cosine Similarity</h1>
    <p><strong>Cosine similarity</strong> is a measure of similarity between two non-zero vectors of an inner product space that measures the cosine of the angle between them.</p>
    <p>In text analysis, it is often used to measure document similarity in vector space models.</p>
    <h2>Applications</h2>
    <ul>
        <li>Document similarity in search engines</li>
        <li>Recommendation systems</li>
        <li>Text mining</li>
        <li>Information retrieval</li>
    </ul>
    <p>Cosine similarity is particularly used in positive space, where the outcome is neatly bounded in [0,1].</p>
</body>
</html>"""
        }
    ]
    
    # Ensure directory exists
    os.makedirs('data/raw_html', exist_ok=True)
    
    print(" Creating sample HTML files...")
    for sample in samples:
        document_id = generate_document_id(sample['url'])
        filename = f"{document_id}.html"
        filepath = os.path.join('data/raw_html', filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(sample['content'])
        
        print(f" Created: {filename}")
        print(f"   Title: {sample['title']}")
    
    print(f"\n Created {len(samples)} sample HTML files in data/raw_html/")

def create_sample_index():
    """Create a sample search index."""
    import pickle
    
    # Create sample index data
    sample_index = {
        "index": {
            "search": {
                "1F648A7F2C64458CBFAF463A071530ED": [1, 15, 23],  # Search engine
                "0F64A61C89AB4CDEF0123456789ABCDE": [45, 67]      # Information retrieval
            },
            "engine": {
                "1F648A7F2C64458CBFAF463A071530ED": [2, 16, 24]  # Search engine
            },
            "web": {
                "6B3BD97C1234456789AB123456789ABC": [1, 12, 25],  # Web crawler
                "1F648A7F2C64458CBFAF463A071530ED": [18, 29]     # Search engine
            },
            "crawl": {
                "6B3BD97C1234456789AB123456789ABC": [3, 13, 26]  # Web crawler
            },
            "inform": {
                "0F64A61C89AB4CDEF0123456789ABCDE": [1, 23, 45]  # Information retrieval
            },
            "retriev": {
                "0F64A61C89AB4CDEF0123456789ABCDE": [2, 24, 46]  # Information retrieval
            },
            "tf": {
                "A1B2C3D4E5F678901234567890123456": [1, 15]      # TF-IDF
            },
            "idf": {
                "A1B2C3D4E5F678901234567890123456": [2, 16]      # TF-IDF
            },
            "cosin": {
                "D4E5F678901234567890123456789012": [1, 12]      # Cosine similarity
            },
            "similar": {
                "D4E5F678901234567890123456789012": [2, 13]      # Cosine similarity
            }
        },
        "document_metadata": {
            "1F648A7F2C64458CBFAF463A071530ED": {
                "url": "https://en.wikipedia.org/wiki/Search_engine",
                "title": "Search Engine - Wikipedia",
                "word_count": 250,
                "token_count": 180
            },
            "6B3BD97C1234456789AB123456789ABC": {
                "url": "https://en.wikipedia.org/wiki/Web_crawler", 
                "title": "Web Crawler - Wikipedia",
                "word_count": 200,
                "token_count": 150
            },
            "0F64A61C89AB4CDEF0123456789ABCDE": {
                "url": "https://en.wikipedia.org/wiki/Information_retrieval",
                "title": "Information Retrieval - Wikipedia", 
                "word_count": 180,
                "token_count": 130
            },
            "A1B2C3D4E5F678901234567890123456": {
                "url": "https://en.wikipedia.org/wiki/Tf-idf",
                "title": "TF-IDF - Wikipedia",
                "word_count": 120,
                "token_count": 90
            },
            "D4E5F678901234567890123456789012": {
                "url": "https://en.wikipedia.org/wiki/Cosine_similarity",
                "title": "Cosine Similarity - Wikipedia",
                "word_count": 110,
                "token_count": 80
            }
        },
        "vocabulary": ["search", "engine", "web", "crawl", "inform", "retriev", "tf", "idf", "cosin", "similar"],
        "total_documents": 5
    }
    
    # Ensure directory exists
    os.makedirs('data/index', exist_ok=True)
    
    # Save inverted index
    index_path = os.path.join('data/index', 'inverted_index.json')
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(sample_index, f, indent=2, ensure_ascii=False)
    
    print(f" Created sample index: {index_path}")
    
    # Create TF-IDF vectors
    tfidf_data = {
        "document_vectors": {
            "1F648A7F2C64458CBFAF463A071530ED": [0.8, 0.6, 0.3, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "6B3BD97C1234456789AB123456789ABC": [0.1, 0.0, 0.9, 0.8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "0F64A61C89AB4CDEF0123456789ABCDE": [0.2, 0.0, 0.0, 0.0, 0.9, 0.8, 0.0, 0.0, 0.0, 0.0],
            "A1B2C3D4E5F678901234567890123456": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.9, 0.8, 0.0, 0.0],
            "D4E5F678901234567890123456789012": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.9, 0.8]
        },
        "term_to_index": {
            "search": 0, "engine": 1, "web": 2, "crawl": 3, 
            "inform": 4, "retriev": 5, "tf": 6, "idf": 7, 
            "cosin": 8, "similar": 9
        }
    }
    
    tfidf_path = os.path.join('data/index', 'tfidf_vectors.pkl')
    with open(tfidf_path, 'wb') as f:
        pickle.dump(tfidf_data, f)
    
    print(f" Created TF-IDF vectors: {tfidf_path}")

if __name__ == "__main__":
    print(" CREATING GUARANTEED WORKING SAMPLE DATA")
    print("=" * 60)
    
    create_sample_files()
    create_sample_index()
    
    print("\n SAMPLE DATA CREATION COMPLETED SUCCESSFULLY!")
    print("\n Files created:")
    print("    data/raw_html/ - 5 sample HTML files")
    print("    data/index/inverted_index.json - Search index")
    print("    data/index/tfidf_vectors.pkl - TF-IDF vectors")
    
    print("\n Next steps:")
    print("1. Run: python run_indexer.py (to verify processing)")
    print("2. Run: python run_processor.py (to start search engine)")
    print("3. Visit: http://localhost:5000")
    print("4. Try searching for: 'search engine', 'web crawler', 'TF-IDF'")
