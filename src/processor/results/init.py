"""
Search results processing and formatting utilities.
"""

import time
from typing import List, Dict, Any
from common.logger import setup_logger

logger = setup_logger(__name__)

class ResultsFormatter:
    """Format and present search results."""
    
    def __init__(self, max_snippet_length: int = 200):
        self.max_snippet_length = max_snippet_length
    
    def format_results(self, results: List[Dict[str, Any]], query: str = "") -> List[Dict[str, Any]]:
        """
        Format search results for presentation.
        
        Args:
            results: Raw search results
            query: Original query for highlighting
            
        Returns:
            Formatted results
        """
        formatted_results = []
        
        for i, result in enumerate(results):
            formatted_result = self._format_single_result(result, query, i + 1)
            formatted_results.append(formatted_result)
        
        return formatted_results
    
    def _format_single_result(self, result: Dict[str, Any], query: str, rank: int) -> Dict[str, Any]:
        """Format a single search result."""
        # Ensure all required fields are present with proper fallbacks
        formatted = {
            'document_id': result.get('document_id', ''),
            'title': result.get('title', 'Untitled Document'),
            'url': result.get('url', '#'),
            'score': round(result.get('score', 0), 4),
            'similarity_score': round(result.get('similarity_score', result.get('score', 0)), 4),
            'snippet': self._generate_snippet(result, query),
            'word_count': result.get('word_count', 0),
            'execution_time': result.get('execution_time', 0),
            'rank': rank
        }
        
        # Add content preview if available
        if result.get('content_preview'):
            formatted['content_preview'] = result['content_preview']
        
        return formatted
    
    def _generate_snippet(self, result: Dict[str, Any], query: str) -> str:
        """Generate a contextual snippet for the result."""
        content = result.get('content', '')
        title = result.get('title', '')
        
        if not content:
            # Create meaningful snippet from available data
            if title and title != 'Untitled Document':
                # Try to extract meaningful information from title
                if 'Wikipedia' in title:
                    topic = title.split(' - ')[0]
                    return f"Wikipedia article about {topic}. " + self._get_topic_description(topic)
                else:
                    return f"Document: {title}"
            else:
                return "Content preview not available"
        
        # Clean content
        content = ' '.join(content.split())
        
        # Look for query terms
        query_terms = [term.lower() for term in query.split() if len(term) > 2]
        
        if not query_terms:
            # No specific query terms, return beginning of content
            return content[:self.max_snippet_length] + "..." if len(content) > self.max_snippet_length else content
        
        # Find the best snippet containing query terms
        best_snippet = self._find_relevant_snippet(content, query_terms)
        
        return best_snippet
    
    def _find_relevant_snippet(self, content: str, query_terms: List[str]) -> str:
        """Find the most relevant snippet containing query terms."""
        content_lower = content.lower()
        
        # Look for each query term
        for term in query_terms:
            pos = content_lower.find(term)
            if pos >= 0:
                # Found a term, extract context around it
                start = max(0, pos - 50)
                end = min(len(content), pos + len(term) + 100)
                snippet = content[start:end]
                
                # Clean up to word boundaries
                if start > 0:
                    # Find the first space after start
                    first_space = snippet.find(' ')
                    if first_space > 0:
                        snippet = snippet[first_space:].strip()
                
                if len(snippet) > self.max_snippet_length:
                    snippet = snippet[:self.max_snippet_length] + "..."
                
                # Highlight the term
                snippet = snippet.replace(term, f"**{term}**")
                return snippet
        
        # Fallback: return beginning of content
        return content[:self.max_snippet_length] + "..." if len(content) > self.max_snippet_length else content
    
    def _get_topic_description(self, topic: str) -> str:
        """Get a generic description for common topics."""
        topic_lower = topic.lower()
        
        descriptions = {
            'search engine': 'A system for finding information on the web using web crawling and indexing.',
            'web crawler': 'An internet bot that systematically browses the web for search engine indexing.',
            'information retrieval': 'The science of searching for information in documents and databases.',
            'tf-idf': 'A statistical measure used to evaluate how important a word is to a document.',
            'cosine similarity': 'A measure of similarity between two vectors, commonly used in text analysis.'
        }
        
        for key, description in descriptions.items():
            if key in topic_lower:
                return description
        
        return f"Information and details about {topic}."

class ResultsRanker:
    """Advanced results ranking and re-ranking."""
    
    def __init__(self):
        self.ranking_factors = {
            'relevance': 0.6,
            'freshness': 0.2,
            'authority': 0.1,
            'popularity': 0.1
        }
    
    def rerank_results(self, results: List[Dict[str, Any]], 
                      user_context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Re-rank results based on multiple factors.
        
        Args:
            results: Initial results
            user_context: User context for personalization
            
        Returns:
            Re-ranked results
        """
        if not results:
            return []
        
        scored_results = []
        
        for result in results:
            score = self._calculate_composite_score(result, user_context)
            scored_results.append((result, score))
        
        # Sort by composite score
        scored_results.sort(key=lambda x: x[1], reverse=True)
        
        return [result for result, score in scored_results]
    
    def _calculate_composite_score(self, result: Dict[str, Any], 
                                 user_context: Dict[str, Any]) -> float:
        """Calculate composite score for result."""
        base_score = result.get('similarity_score', result.get('score', 0))
        
        # Apply ranking factors
        composite_score = base_score * self.ranking_factors['relevance']
        
        # Add freshness factor (if timestamp available)
        if 'timestamp' in result:
            freshness_score = self._calculate_freshness_score(result['timestamp'])
            composite_score += freshness_score * self.ranking_factors['freshness']
        
        # Add authority factor (based on domain)
        authority_score = self._calculate_authority_score(result.get('url', ''))
        composite_score += authority_score * self.ranking_factors['authority']
        
        # Add popularity factor (if available)
        popularity_score = result.get('popularity_score', 0.5)
        composite_score += popularity_score * self.ranking_factors['popularity']
        
        return composite_score
    
    def _calculate_freshness_score(self, timestamp: str) -> float:
        """Calculate freshness score based on timestamp."""
        try:
            from datetime import datetime
            doc_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            now = datetime.now()
            age_days = (now - doc_time).days
            
            # Score decreases with age (1.0 for today, 0.0 for >365 days)
            return max(0.0, 1.0 - (age_days / 365.0))
            
        except Exception:
            return 0.5  # Default score
    
    def _calculate_authority_score(self, url: str) -> float:
        """Calculate authority score based on domain."""
        try:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc.lower()
            
            # Simple authority scoring based on domain
            authority_domains = {
                'wikipedia.org': 1.0,
                'github.com': 0.9,
                'stackoverflow.com': 0.8,
                'medium.com': 0.6,
                'blogspot.com': 0.5
            }
            
            for auth_domain, score in authority_domains.items():
                if auth_domain in domain:
                    return score
            
            return 0.5  # Default score
            
        except Exception:
            return 0.5