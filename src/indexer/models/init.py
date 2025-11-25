"""
Data models for the indexer component.
"""

from dataclasses import dataclass
from typing import List, Dict, Any
import numpy as np

@dataclass
class Document:
    """Document model for indexing."""
    
    document_id: str
    url: str
    title: str
    content: str
    html_content: str = ""
    word_count: int = 0
    token_count: int = 0
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        self.word_count = len(self.content.split())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert document to dictionary."""
        return {
            'document_id': self.document_id,
            'url': self.url,
            'title': self.title,
            'content': self.content,
            'html_content': self.html_content,
            'word_count': self.word_count,
            'token_count': self.token_count,
            'metadata': self.metadata
        }

@dataclass
class SearchResult:
    """Search result model."""
    
    document_id: str
    score: float
    similarity_score: float
    title: str
    url: str
    snippet: str
    word_count: int
    execution_time: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            'document_id': self.document_id,
            'score': self.score,
            'similarity_score': self.similarity_score,
            'title': self.title,
            'url': self.url,
            'snippet': self.snippet,
            'word_count': self.word_count,
            'execution_time': self.execution_time
        }

@dataclass
class IndexStatistics:
    """Index statistics model."""
    
    total_documents: int
    vocabulary_size: int
    total_terms: int
    average_document_length: float
    index_size_bytes: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert statistics to dictionary."""
        return {
            'total_documents': self.total_documents,
            'vocabulary_size': self.vocabulary_size,
            'total_terms': self.total_terms,
            'average_document_length': self.average_document_length,
            'index_size_bytes': self.index_size_bytes
        }