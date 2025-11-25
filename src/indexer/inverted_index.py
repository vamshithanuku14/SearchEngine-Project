import os
import json
import pickle
from collections import defaultdict, Counter
from typing import Dict, List, Set, Any
from common.config import Config
from common.logger import setup_logger
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

logger = setup_logger(__name__)

class InvertedIndex:
    """Advanced inverted index with positional indexing and TF-IDF support."""
    
    def __init__(self):
        self.config = Config()
        self.index = defaultdict(dict)  # term -> {doc_id: [positions]}
        self.document_metadata = {}     # doc_id -> {url, title, word_count, etc.}
        self.vocabulary = set()
        self.total_documents = 0
        
        # Initialize NLP tools
        self._initialize_nlp()
    
    def _initialize_nlp(self):
        """Initialize NLP tools and download required data."""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet=True)
        
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
    
    def preprocess_text(self, text: str) -> List[str]:
        """Preprocess text: tokenize, remove stopwords, and stem."""
        if not text:
            return []
        
        try:
            # Tokenize
            tokens = word_tokenize(text.lower())
            
            # Filter and process tokens
            processed_tokens = []
            for token in tokens:
                # Remove non-alphanumeric characters and short/long tokens
                if (len(token) >= self.config.get('indexer.min_word_length', 2) and
                    len(token) <= self.config.get('indexer.max_word_length', 25) and
                    token.isalnum() and
                    token not in self.stop_words):
                    
                    # Stem the token
                    stemmed_token = self.stemmer.stem(token)
                    processed_tokens.append(stemmed_token)
            
            return processed_tokens
            
        except Exception as e:
            logger.error(f"Error preprocessing text: {str(e)}")
            return []
    
    def add_document(self, document_id: str, content: str, metadata: Dict[str, Any] = None):
        """Add a document to the inverted index."""
        if not content:
            logger.warning(f"Empty content for document {document_id}")
            return
        
        # Preprocess content
        tokens = self.preprocess_text(content)
        
        if not tokens:
            logger.warning(f"No valid tokens found for document {document_id}")
            return
        
        # Update document metadata
        self.document_metadata[document_id] = {
            'url': metadata.get('url', '') if metadata else '',
            'title': metadata.get('title', '') if metadata else '',
            'word_count': len(tokens),
            'token_count': len(tokens)
        }
        
        # Update index with positional information
        term_positions = defaultdict(list)
        for position, token in enumerate(tokens):
            term_positions[token].append(position)
        
        for term, positions in term_positions.items():
            self.index[term][document_id] = positions
            self.vocabulary.add(term)
        
        self.total_documents += 1
        logger.debug(f"Added document {document_id} with {len(tokens)} tokens")
    
    def get_document_frequency(self, term: str) -> int:
        """Get the number of documents containing the term."""
        return len(self.index.get(term, {}))
    
    def get_term_frequency(self, term: str, document_id: str) -> int:
        """Get the frequency of a term in a specific document."""
        return len(self.index.get(term, {}).get(document_id, []))
    
    def search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Search the index for a query (basic boolean search)."""
        query_terms = self.preprocess_text(query)
        
        if not query_terms:
            return []
        
        # Find documents containing all query terms
        relevant_docs = set()
        for term in query_terms:
            if term in self.index:
                if not relevant_docs:
                    relevant_docs = set(self.index[term].keys())
                else:
                    relevant_docs = relevant_docs.intersection(self.index[term].keys())
        
        # Calculate simple score based on term frequency
        results = []
        for doc_id in relevant_docs:
            score = sum(self.get_term_frequency(term, doc_id) for term in query_terms)
            results.append({
                'document_id': doc_id,
                'score': score,
                'metadata': self.document_metadata.get(doc_id, {})
            })
        
        # Sort by score and return top K
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]
    
    def save_index(self, filepath: str):
        """Save the inverted index to a JSON file."""
        try:
            # Convert defaultdict to regular dict for JSON serialization
            index_serializable = {term: dict(docs) for term, docs in self.index.items()}
            
            index_data = {
                'index': index_serializable,
                'document_metadata': self.document_metadata,
                'vocabulary': list(self.vocabulary),
                'total_documents': self.total_documents
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Index saved to {filepath} with {self.total_documents} documents")
            
        except Exception as e:
            logger.error(f"Error saving index to {filepath}: {str(e)}")
            raise
    
    def load_index(self, filepath: str):
        """Load the inverted index from a JSON file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
            
            # Convert back to defaultdict
            self.index = defaultdict(dict)
            for term, docs in index_data['index'].items():
                self.index[term] = docs
            
            self.document_metadata = index_data['document_metadata']
            self.vocabulary = set(index_data['vocabulary'])
            self.total_documents = index_data['total_documents']
            
            logger.info(f"Index loaded from {filepath} with {self.total_documents} documents")
            
        except Exception as e:
            logger.error(f"Error loading index from {filepath}: {str(e)}")
            raise
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get index statistics."""
        total_terms = sum(len(docs) for docs in self.index.values())
        avg_doc_length = sum(meta.get('word_count', 0) for meta in self.document_metadata.values()) / max(1, self.total_documents)
        
        return {
            'total_documents': self.total_documents,
            'vocabulary_size': len(self.vocabulary),
            'total_terms': total_terms,
            'average_document_length': avg_doc_length
        }