"""
Query handling and processing utilities.
"""

import re
from typing import Dict, List, Any, Tuple
from common.logger import setup_logger

logger = setup_logger(__name__)

class QueryParser:
    """Advanced query parser with syntax support."""
    
    def __init__(self):
        self.operators = {'AND', 'OR', 'NOT'}
        self.special_chars = {'"', '(', ')', ':', '-'}
    
    def parse_advanced_query(self, query: str) -> Dict[str, Any]:
        """
        Parse advanced query with boolean operators and phrases.
        
        Args:
            query: Input query string
            
        Returns:
            Parsed query structure
        """
        try:
            # Clean query
            query = query.strip()
            
            # Handle phrase queries (quoted text)
            phrases = self._extract_phrases(query)
            query_without_phrases = self._remove_phrases(query)
            
            # Parse boolean expressions
            terms = self._parse_boolean_expression(query_without_phrases)
            
            # Handle field-specific queries (title:search, url:example.com)
            field_queries = self._extract_field_queries(terms)
            
            return {
                'original_query': query,
                'terms': terms,
                'phrases': phrases,
                'field_queries': field_queries,
                'is_advanced': bool(phrases or field_queries or any(op in query.upper() for op in self.operators))
            }
            
        except Exception as e:
            logger.error(f"Error parsing query '{query}': {str(e)}")
            return {
                'original_query': query,
                'terms': query.split(),
                'phrases': [],
                'field_queries': {},
                'is_advanced': False
            }
    
    def _extract_phrases(self, query: str) -> List[str]:
        """Extract quoted phrases from query."""
        phrases = re.findall(r'"([^"]*)"', query)
        return [phrase.strip() for phrase in phrases if phrase.strip()]
    
    def _remove_phrases(self, query: str) -> str:
        """Remove quoted phrases from query."""
        return re.sub(r'"[^"]*"', '', query).strip()
    
    def _parse_boolean_expression(self, query: str) -> List[Dict[str, Any]]:
        """Parse boolean expression into structured terms."""
        tokens = query.split()
        parsed_terms = []
        
        i = 0
        while i < len(tokens):
            token = tokens[i].upper()
            
            if token in self.operators:
                parsed_terms.append({'type': 'operator', 'value': token})
            else:
                # Handle NOT operator (special case)
                if token == 'NOT' and i + 1 < len(tokens):
                    parsed_terms.append({
                        'type': 'term',
                        'value': tokens[i + 1],
                        'operator': 'NOT'
                    })
                    i += 1  # Skip next token
                else:
                    parsed_terms.append({
                        'type': 'term',
                        'value': tokens[i],
                        'operator': 'AND'  # Default operator
                    })
            
            i += 1
        
        return parsed_terms
    
    def _extract_field_queries(self, terms: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Extract field-specific queries (e.g., title:search)."""
        field_queries = {}
        
        for term in terms:
            if term['type'] == 'term':
                value = term['value']
                if ':' in value:
                    field, field_value = value.split(':', 1)
                    if field in ['title', 'url', 'content']:
                        if field not in field_queries:
                            field_queries[field] = []
                        field_queries[field].append(field_value)
        
        return field_queries

class QueryExpander:
    """Query expansion using semantic relationships."""
    
    def __init__(self):
        self.synonym_cache = {}
    
    def expand_query(self, query: str, expansion_type: str = "synonyms") -> str:
        """
        Expand query with related terms.
        
        Args:
            query: Original query
            expansion_type: Type of expansion (synonyms, related, etc.)
            
        Returns:
            Expanded query
        """
        try:
            if expansion_type == "synonyms":
                return self._expand_with_synonyms(query)
            elif expansion_type == "related":
                return self._expand_with_related_terms(query)
            else:
                return query
                
        except Exception as e:
            logger.error(f"Error expanding query: {str(e)}")
            return query
    
    def _expand_with_synonyms(self, query: str) -> str:
        """Expand query with synonyms."""
        import nltk
        from nltk.corpus import wordnet
        
        words = query.split()
        expanded_words = set(words)
        
        for word in words:
            if word in self.synonym_cache:
                expanded_words.update(self.synonym_cache[word])
            else:
                synonyms = set()
                for syn in wordnet.synsets(word):
                    for lemma in syn.lemmas():
                        synonym = lemma.name().replace('_', ' ')
                        if synonym != word and len(synonym.split()) == 1:
                            synonyms.add(synonym)
                
                self.synonym_cache[word] = synonyms
                expanded_words.update(synonyms)
        
        return ' '.join(words + list(expanded_words - set(words)))
    
    def _expand_with_related_terms(self, query: str) -> str:
        """Expand query with semantically related terms."""
        # This could use word embeddings or knowledge graphs
        # For now, return the original query
        return query