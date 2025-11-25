import numpy as np
from typing import Dict, List, Any
from common.config import Config
from common.logger import setup_logger
from .inverted_index import InvertedIndex

logger = setup_logger(__name__)

class TFIDFCalculator:
    """TF-IDF calculator for document ranking."""
    
    def __init__(self, inverted_index: InvertedIndex):
        self.index = inverted_index
        self.config = Config()
        self.tfidf_vectors = {}  # doc_id -> {term: tfidf_score}
        self.term_to_index = {}  # term -> index in vector
        self.document_vectors = {}  # doc_id -> numpy array
    
    def calculate_tfidf(self):
        """Calculate TF-IDF scores for all documents and terms."""
        logger.info("Calculating TF-IDF scores...")
        
        # Create term to index mapping
        self.term_to_index = {term: idx for idx, term in enumerate(self.index.vocabulary)}
        vocabulary_size = len(self.index.vocabulary)
        
        # Calculate TF-IDF for each document
        for doc_id in self.index.document_metadata.keys():
            tfidf_vector = np.zeros(vocabulary_size)
            doc_word_count = self.index.document_metadata[doc_id].get('word_count', 1)
            
            for term, idx in self.term_to_index.items():
                if doc_id in self.index.index.get(term, {}):
                    # Term Frequency (TF)
                    tf = len(self.index.index[term][doc_id]) / doc_word_count
                    
                    # Inverse Document Frequency (IDF)
                    doc_freq = len(self.index.index[term])
                    idf = np.log((self.index.total_documents + 1) / (doc_freq + 1)) + 1
                    
                    # TF-IDF
                    tfidf_score = tf * idf
                    tfidf_vector[idx] = tfidf_score
            
            self.tfidf_vectors[doc_id] = tfidf_vector
            self.document_vectors[doc_id] = tfidf_vector
        
        logger.info(f"TF-IDF calculation completed for {len(self.tfidf_vectors)} documents")
    
    def get_query_vector(self, query_terms: List[str]) -> np.ndarray:
        """Convert query terms to TF-IDF vector."""
        vocabulary_size = len(self.index.vocabulary)
        query_vector = np.zeros(vocabulary_size)
        
        if not query_terms:
            return query_vector
        
        # Calculate TF for query (IDF uses collection statistics)
        term_freq = {}
        for term in query_terms:
            term_freq[term] = term_freq.get(term, 0) + 1
        
        query_length = len(query_terms)
        
        for term, freq in term_freq.items():
            if term in self.term_to_index:
                idx = self.term_to_index[term]
                
                # TF for query
                tf = freq / query_length
                
                # IDF from collection
                doc_freq = len(self.index.index.get(term, {}))
                idf = np.log((self.index.total_documents + 1) / (doc_freq + 1)) + 1
                
                query_vector[idx] = tf * idf
        
        return query_vector
    
    def get_document_scores(self, query_vector: np.ndarray) -> List[Dict[str, Any]]:
        """Get TF-IDF scores for documents against query vector."""
        scores = []
        
        for doc_id, doc_vector in self.document_vectors.items():
            # Calculate cosine similarity
            dot_product = np.dot(query_vector, doc_vector)
            query_norm = np.linalg.norm(query_vector)
            doc_norm = np.linalg.norm(doc_vector)
            
            if query_norm == 0 or doc_norm == 0:
                similarity = 0.0
            else:
                similarity = dot_product / (query_norm * doc_norm)
            
            scores.append({
                'document_id': doc_id,
                'score': similarity,
                'metadata': self.index.document_metadata.get(doc_id, {})
            })
        
        return scores
    
    def save_tfidf_vectors(self, filepath: str):
        """Save TF-IDF vectors to file."""
        import pickle
        
        tfidf_data = {
            'tfidf_vectors': self.tfidf_vectors,
            'term_to_index': self.term_to_index,
            'document_vectors': self.document_vectors
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(tfidf_data, f)
        
        logger.info(f"TF-IDF vectors saved to {filepath}")
    
    def load_tfidf_vectors(self, filepath: str):
        """Load TF-IDF vectors from file."""
        import pickle
        
        with open(filepath, 'rb') as f:
            tfidf_data = pickle.load(f)
        
        self.tfidf_vectors = tfidf_data['tfidf_vectors']
        self.term_to_index = tfidf_data['term_to_index']
        self.document_vectors = tfidf_data['document_vectors']
        
        logger.info(f"TF-IDF vectors loaded from {filepath}")