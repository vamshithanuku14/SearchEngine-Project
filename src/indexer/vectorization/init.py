"""
Vectorization utilities for the indexer.
"""

import numpy as np
from typing import Dict, List, Any
from common.logger import setup_logger

logger = setup_logger(__name__)

class Vectorizer:
    """Base vectorizer class for document and query vectorization."""
    
    def __init__(self, vector_size: int = 300):
        self.vector_size = vector_size
        self.vocabulary = {}
        self.vector_cache = {}
    
    def fit(self, documents: List[str]):
        """
        Fit vectorizer on documents.
        
        Args:
            documents: List of document texts
        """
        raise NotImplementedError("Subclasses must implement fit method")
    
    def transform(self, text: str) -> np.ndarray:
        """
        Transform text to vector.
        
        Args:
            text: Input text
            
        Returns:
            Vector representation
        """
        raise NotImplementedError("Subclasses must implement transform method")
    
    def batch_transform(self, texts: List[str]) -> np.ndarray:
        """
        Transform multiple texts to vectors.
        
        Args:
            texts: List of input texts
            
        Returns:
            Matrix of vector representations
        """
        return np.array([self.transform(text) for text in texts])

class TFIDFVectorizer(Vectorizer):
    """TF-IDF based vectorizer."""
    
    def __init__(self):
        super().__init__()
        self.idf = {}
        self.doc_count = 0
    
    def fit(self, documents: List[str]):
        """Fit TF-IDF vectorizer on documents."""
        from collections import defaultdict
        import math
        
        # Build vocabulary and document frequency
        doc_freq = defaultdict(int)
        tokenized_docs = []
        
        for doc in documents:
            tokens = doc.lower().split()
            tokenized_docs.append(tokens)
            for token in set(tokens):
                doc_freq[token] += 1
        
        self.doc_count = len(documents)
        self.vocabulary = {token: idx for idx, token in enumerate(doc_freq.keys())}
        self.vector_size = len(self.vocabulary)
        
        # Calculate IDF
        for token, freq in doc_freq.items():
            self.idf[token] = math.log((self.doc_count + 1) / (freq + 1)) + 1
    
    def transform(self, text: str) -> np.ndarray:
        """Transform text to TF-IDF vector."""
        if text in self.vector_cache:
            return self.vector_cache[text]
        
        vector = np.zeros(self.vector_size)
        tokens = text.lower().split()
        
        if not tokens:
            return vector
        
        # Calculate term frequencies
        term_freq = {}
        for token in tokens:
            term_freq[token] = term_freq.get(token, 0) + 1
        
        # Build TF-IDF vector
        for token, freq in term_freq.items():
            if token in self.vocabulary:
                idx = self.vocabulary[token]
                tf = freq / len(tokens)
                idf = self.idf.get(token, 1.0)
                vector[idx] = tf * idf
        
        # Cache the vector
        self.vector_cache[text] = vector
        return vector

class EmbeddingVectorizer(Vectorizer):
    """Word embedding based vectorizer."""
    
    def __init__(self, embedding_model=None):
        super().__init__(vector_size=300)
        self.embedding_model = embedding_model
    
    def fit(self, documents: List[str]):
        """Fit embedding vectorizer (load pre-trained model)."""
        try:
            import gensim.downloader as api
            logger.info("Loading pre-trained word2vec model...")
            self.embedding_model = api.load('word2vec-google-news-300')
            logger.info("Word2vec model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading embedding model: {str(e)}")
            self.embedding_model = None
    
    def transform(self, text: str) -> np.ndarray:
        """Transform text to embedding vector."""
        if not self.embedding_model:
            return np.zeros(self.vector_size)
        
        if text in self.vector_cache:
            return self.vector_cache[text]
        
        tokens = text.lower().split()
        vectors = []
        
        for token in tokens:
            try:
                if token in self.embedding_model:
                    vectors.append(self.embedding_model[token])
            except KeyError:
                continue
        
        if not vectors:
            vector = np.zeros(self.vector_size)
        else:
            vector = np.mean(vectors, axis=0)
        
        # Cache the vector
        self.vector_cache[text] = vector
        return vector