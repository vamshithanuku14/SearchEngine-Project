# 🔍 Search Engine Project

A comprehensive, production-ready search engine implementation featuring advanced web crawling, intelligent indexing with TF-IDF scoring, and a modern web interface. Built with Python, Scrapy, Scikit-learn, and Flask.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Scrapy](https://img.shields.io/badge/Scrapy-2.13-green)
![Flask](https://img.shields.io/badge/Flask-3.0-red)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

## ✨ Features

### 🕷️ Advanced Web Crawling
- **Polite Crawling**: Respects robots.txt with configurable delays
- **Domain Control**: Restricted crawling with allowed domains
- **Depth Management**: Configurable crawl depth and page limits
- **Content Extraction**: HTML parsing with BeautifulSoup

### 📊 Intelligent Indexing
- **TF-IDF Scoring**: Term frequency-inverse document frequency
- **Cosine Similarity**: Advanced vector space model ranking
- **Positional Indexing**: Exact term positioning for phrase queries
- **NLP Processing**: Tokenization, stemming, stopword removal

### 🔍 Smart Search
- **Spell Checking**: Automatic query correction
- **Query Expansion**: Synonym expansion using WordNet
- **Relevance Ranking**: Multiple ranking algorithms
- **Real-time Suggestions**: Autocomplete and search suggestions

### 🎨 Modern Interface
- **Responsive Design**: Works on all devices
- **Real-time Results**: Instant search as you type
- **Batch Processing**: CSV upload for multiple queries
- **REST API**: Full API support for integration

## 🚀 Quick Start

### Prerequisites
- Python 3.11+ (Recommended for compatibility)
- 8GB RAM minimum
- 2GB free disk space

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd SearchEngine-Project

# Create virtual environment
python -m venv venv

# Activate environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"

Full Pipeline
bash
# Step 1: Crawl web pages
python run_crawler.py
# Enter seed URLs and page limits when prompted

# Step 2: Build search index
python run_indexer.py

# Step 3: Start search engine
python run_processor.py

Testing
Run the comprehensive test suite:

bash
# Run all tests with coverage
pytest --cov=src

# Run specific test categories
pytest tests/test_crawler/    # Crawler tests
pytest tests/test_indexer/    # Indexer tests
pytest tests/test_processor/  # Processor tests

# Generate HTML coverage report
pytest --cov=src --cov-report=html