"""
Text preprocessing utilities for the indexer.
"""

import re
import string
from typing import List, Callable
from common.logger import setup_logger

logger = setup_logger(__name__)

class TextPreprocessor:
    """Advanced text preprocessing pipeline."""
    
    def __init__(self, min_word_length: int = 2, max_word_length: int = 25):
        self.min_word_length = min_word_length
        self.max_word_length = max_word_length
        self.pipeline = []
        
        # Build default pipeline
        self._build_default_pipeline()
    
    def _build_default_pipeline(self):
        """Build default preprocessing pipeline."""
        self.pipeline = [
            self.lowercase,
            self.remove_punctuation,
            self.remove_numbers,
            self.remove_extra_whitespace,
            self.tokenize,
            self.filter_short_long_tokens,
            self.remove_stopwords,
            self.stem_tokens
        ]
    
    def add_step(self, step: Callable, position: int = None):
        """
        Add a step to the preprocessing pipeline.
        
        Args:
            step: Processing function
            position: Position in pipeline (None for end)
        """
        if position is None:
            self.pipeline.append(step)
        else:
            self.pipeline.insert(position, step)
    
    def process(self, text: str) -> List[str]:
        """
        Process text through the pipeline.
        
        Args:
            text: Input text
            
        Returns:
            List of processed tokens
        """
        if not text:
            return []
        
        try:
            current_text = text
            for step in self.pipeline:
                current_text = step(current_text)
            
            return current_text
            
        except Exception as e:
            logger.error(f"Error in text preprocessing: {str(e)}")
            return []
    
    def lowercase(self, text: str) -> str:
        """Convert text to lowercase."""
        return text.lower()
    
    def remove_punctuation(self, text: str) -> str:
        """Remove punctuation from text."""
        return text.translate(str.maketrans('', '', string.punctuation))
    
    def remove_numbers(self, text: str) -> str:
        """Remove numbers from text."""
        return re.sub(r'\d+', '', text)
    
    def remove_extra_whitespace(self, text: str) -> str:
        """Remove extra whitespace from text."""
        return ' '.join(text.split())
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into words."""
        return text.split()
    
    def filter_short_long_tokens(self, tokens: List[str]) -> List[str]:
        """Filter tokens by length."""
        return [
            token for token in tokens 
            if self.min_word_length <= len(token) <= self.max_word_length
        ]
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """Remove stopwords from tokens."""
        try:
            from nltk.corpus import stopwords
            stop_words = set(stopwords.words('english'))
            return [token for token in tokens if token not in stop_words]
        except ImportError:
            logger.warning("NLTK not available, skipping stopword removal")
            return tokens
    
    def stem_tokens(self, tokens: List[str]) -> List[str]:
        """Stem tokens using Porter stemmer."""
        try:
            from nltk.stem import PorterStemmer
            stemmer = PorterStemmer()
            return [stemmer.stem(token) for token in tokens]
        except ImportError:
            logger.warning("NLTK not available, skipping stemming")
            return tokens

# Global preprocessor instance
default_preprocessor = TextPreprocessor()