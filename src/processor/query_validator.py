import re
import string
from typing import Dict, List, Any, Tuple
from common.config import Config
from common.logger import setup_logger
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.metrics import edit_distance
import heapq
from collections import defaultdict

logger = setup_logger(__name__)

class EnhancedQueryValidator:
    """Enhanced query validation with advanced spelling correction and expansion."""
    
    def __init__(self):
        self.config = Config()
        
        # Initialize common_queries BEFORE calling _initialize_enhanced_spell_checker
        self.common_queries = [
            "search engine", "web crawling", "information retrieval",
            "machine learning", "natural language processing", 
            "tf-idf scoring", "cosine similarity", "inverted index",
            "web scraping", "document ranking", "text mining",
            "vector space model", "relevance ranking", "search algorithm",
            "python programming", "flask web framework", "scrapy framework",
            "data mining", "big data", "artificial intelligence"
        ]
        
        self._initialize_nltk()
        
        # Enhanced validation rules
        self.max_query_length = 200
        self.min_query_length = 1
        self.allowed_chars = r'^[a-zA-Z0-9\s\.\,\-\?\!\"\'\:\;]+$'
        
        # Enhanced spell checking
        self.spell_checker = None
        self.vocabulary = set()
        self._initialize_enhanced_spell_checker()
        
        # Query expansion cache
        self.expansion_cache = {}
        
        # Query suggestion history (simulated)
        self.search_history = [
            "search engine", "web crawler", "information retrieval",
            "tf-idf", "cosine similarity", "python search engine",
            "flask web application", "scrapy tutorial", "machine learning"
        ]
    
    def _initialize_nltk(self):
        """Initialize NLTK resources with enhanced data."""
        required_packages = ['punkt', 'wordnet', 'stopwords', 'averaged_perceptron_tagger']
        
        for package in required_packages:
            try:
                if package == 'punkt':
                    nltk.data.find(f'tokenizers/{package}')
                else:
                    nltk.data.find(f'corpora/{package}')
            except LookupError:
                nltk.download(package, quiet=True)
        
        self.stop_words = set(nltk.corpus.stopwords.words('english'))
        self.lemmatizer = nltk.stem.WordNetLemmatizer()
    
    def _initialize_enhanced_spell_checker(self):
        """Initialize enhanced spell checking with custom vocabulary."""
        try:
            # Build custom vocabulary from common search terms
            self.vocabulary = set()
            for query in self.common_queries:
                self.vocabulary.update(query.lower().split())
            
            # Add technical terms
            technical_terms = {
                'tfidf', 'cosine', 'vector', 'indexing', 'crawler',
                'retrieval', 'algorithm', 'relevance', 'ranking',
                'semantic', 'syntactic', 'morphological', 'stemming',
                'lemmatization', 'tokenization', 'normalization',
                'programming', 'framework', 'scrapy', 'flask', 'python',
                'machine', 'learning', 'artificial', 'intelligence'
            }
            self.vocabulary.update(technical_terms)
            
            logger.info(f"Enhanced spell checker initialized with {len(self.vocabulary)} terms")
            
        except Exception as e:
            logger.warning(f"Enhanced spell checker initialization failed: {str(e)}")
    
    def validate_query(self, query: str) -> Dict[str, Any]:
        """Enhanced query validation with detailed analysis."""
        if not isinstance(query, str):
            return {
                'valid': False, 
                'message': 'Query must be a string',
                'error_code': 'INVALID_TYPE'
            }
        
        # Check empty query
        if not query.strip():
            return {
                'valid': False,
                'message': 'Query cannot be empty',
                'error_code': 'EMPTY_QUERY'
            }
        
        # Check query length
        if len(query) < self.min_query_length:
            return {
                'valid': False,
                'message': f'Query must be at least {self.min_query_length} character long',
                'error_code': 'QUERY_TOO_SHORT'
            }
        
        if len(query) > self.max_query_length:
            return {
                'valid': False,
                'message': f'Query cannot exceed {self.max_query_length} characters',
                'error_code': 'QUERY_TOO_LONG'
            }
        
        # Check for allowed characters
        if not re.match(self.allowed_chars, query):
            invalid_chars = self._find_invalid_characters(query)
            return {
                'valid': False,
                'message': f'Query contains invalid characters: {invalid_chars}',
                'error_code': 'INVALID_CHARACTERS',
                'invalid_chars': invalid_chars
            }
        
        # Clean and analyze query
        cleaned_query = self._clean_query(query)
        analysis = self._analyze_query(cleaned_query)
        
        # Enhanced spell checking
        spelling_result = self._enhanced_spell_check(cleaned_query)
        
        # Query expansion
        expansion_result = self._enhanced_query_expansion(cleaned_query)
        
        # Determine final query to use
        final_query = cleaned_query
        if spelling_result['has_corrections']:
            final_query = spelling_result['corrected_query']
        
        return {
            'valid': True,
            'message': 'Query is valid',
            'original_query': query,
            'cleaned_query': cleaned_query,
            'corrected_query': spelling_result.get('corrected_query', cleaned_query),
            'expanded_query': expansion_result.get('expanded_query', cleaned_query),
            'analysis': analysis,
            'spelling': spelling_result,
            'expansion': expansion_result,
            'suggested_query': expansion_result.get('expanded_query', final_query),
            'has_corrections': spelling_result['has_corrections'],
            'has_expansions': len(expansion_result.get('new_terms', [])) > 0
        }
    
    def _find_invalid_characters(self, query: str) -> List[str]:
        """Find and return invalid characters in query."""
        invalid_chars = []
        for char in query:
            if not re.match(r'[a-zA-Z0-9\s\.\,\-\?\!\"\'\:\;]', char):
                if char not in invalid_chars:
                    invalid_chars.append(char)
        return invalid_chars
    
    def _clean_query(self, query: str) -> str:
        """Enhanced query cleaning and normalization."""
        # Convert to lowercase
        query = query.lower()
        
        # Remove extra whitespace
        query = ' '.join(query.split())
        
        # Remove special characters (keep basic punctuation)
        query = re.sub(r'[^\w\s\.\,\-\?\!\"\'\:\;]', '', query)
        
        return query.strip()
    
    def _analyze_query(self, query: str) -> Dict[str, Any]:
        """Analyze query structure and content."""
        words = word_tokenize(query)
        unique_words = set(words)
        
        # POS tagging for query understanding
        pos_tags = nltk.pos_tag(words)
        
        return {
            'word_count': len(words),
            'unique_words': len(unique_words),
            'stop_words': [w for w in words if w in self.stop_words],
            'content_words': [w for w in words if w not in self.stop_words],
            'pos_tags': pos_tags,
            'query_type': self._classify_query_type(words, pos_tags)
        }
    
    def _classify_query_type(self, words: List[str], pos_tags: List[Tuple[str, str]]) -> str:
        """Classify query type based on content and structure."""
        nouns = [word for word, pos in pos_tags if pos.startswith('NN')]
        verbs = [word for word, pos in pos_tags if pos.startswith('VB')]
        adjectives = [word for word, pos in pos_tags if pos.startswith('JJ')]
        
        if len(words) == 1:
            return 'NAVIGATIONAL'
        elif len(nouns) > 2 and len(verbs) == 0:
            return 'INFORMATIONAL'
        elif any(word in ['how', 'what', 'why', 'when', 'where'] for word in words):
            return 'QUESTION'
        else:
            return 'TRANSACTIONAL'
    
    def _enhanced_spell_check(self, query: str) -> Dict[str, Any]:
        """Enhanced spell checking with context awareness."""
        words = word_tokenize(query)
        corrections = []
        corrected_words = []
        
        for word in words:
            if word in string.punctuation:
                corrected_words.append(word)
                continue
                
            if self._is_misspelled(word):
                correction = self._find_best_correction(word)
                if correction and correction != word:
                    corrections.append({
                        'original': word,
                        'corrected': correction,
                        'confidence': self._calculate_confidence(word, correction)
                    })
                    corrected_words.append(correction)
                else:
                    corrected_words.append(word)
            else:
                corrected_words.append(word)
        
        corrected_query = ' '.join(corrected_words)
        
        return {
            'has_corrections': len(corrections) > 0,
            'corrections': corrections,
            'corrected_query': corrected_query if corrections else query,
            'confidence_score': sum(c['confidence'] for c in corrections) / len(corrections) if corrections else 1.0
        }
    
    def _is_misspelled(self, word: str) -> bool:
        """Check if a word is likely misspelled."""
        if word in self.stop_words or word in string.punctuation:
            return False
        
        # Check against vocabulary
        if word.lower() in self.vocabulary:
            return False
        
        # Check if it's a number
        if word.replace('.', '').isdigit():
            return False
            
        return True
    
    def _find_best_correction(self, word: str, max_candidates: int = 5) -> str:
        """Find the best correction for a misspelled word."""
        candidates = []
        
        # Generate candidate corrections
        for vocab_word in self.vocabulary:
            distance = edit_distance(word.lower(), vocab_word.lower())
            similarity = 1 - (distance / max(len(word), len(vocab_word)))
            
            if similarity > 0.6:  # Threshold for considering a correction
                heapq.heappush(candidates, (-similarity, vocab_word))
        
        # Return best candidate
        if candidates:
            best_similarity, best_candidate = heapq.heappop(candidates)
            return best_candidate
        
        return word  # Return original if no good correction found
    
    def _calculate_confidence(self, original: str, correction: str) -> float:
        """Calculate confidence score for a correction."""
        distance = edit_distance(original.lower(), correction.lower())
        max_len = max(len(original), len(correction))
        similarity = 1 - (distance / max_len)
        
        # Adjust confidence based on word length
        length_factor = min(len(original) / 10, 1.0)  # Longer words have higher confidence
        
        return similarity * length_factor
    
    def _enhanced_query_expansion(self, query: str) -> Dict[str, Any]:
        """Enhanced query expansion with semantic relationships."""
        if query in self.expansion_cache:
            return self.expansion_cache[query]
        
        words = word_tokenize(query)
        expanded_terms = set(words)
        expansion_details = []
        
        for word in words:
            if word in self.stop_words or word in string.punctuation:
                continue
                
            # Get synonyms
            synonyms = self._get_enhanced_synonyms(word)
            if synonyms:
                expanded_terms.update(synonyms)
                expansion_details.append({
                    'term': word,
                    'type': 'synonym',
                    'expansions': synonyms
                })
            
            # Get related terms (hyponyms, hypernyms)
            related = self._get_related_terms(word)
            if related:
                expanded_terms.update(related)
                expansion_details.append({
                    'term': word,
                    'type': 'related',
                    'expansions': related
                })
        
        # Create expanded query (original + new terms)
        original_terms = set(words)
        new_terms = expanded_terms - original_terms
        
        expanded_query = ' '.join(words) + ' ' + ' '.join(new_terms)
        expanded_query = ' '.join(expanded_query.split())  # Normalize whitespace
        
        result = {
            'original_terms': list(original_terms),
            'expanded_terms': list(expanded_terms),
            'new_terms': list(new_terms),
            'expansion_details': expansion_details,
            'expanded_query': expanded_query.strip(),
            'expansion_factor': len(expanded_terms) / len(original_terms) if original_terms else 1.0
        }
        
        self.expansion_cache[query] = result
        return result
    
    def _get_enhanced_synonyms(self, word: str, max_synonyms: int = 3) -> List[str]:
        """Get enhanced synonyms with filtering."""
        synonyms = set()
        
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonym = lemma.name().replace('_', ' ').lower()
                if (synonym != word and 
                    len(synonym.split()) == 1 and  # Single word synonyms
                    synonym not in self.stop_words and
                    len(synonym) > 2):  # Meaningful words only
                    synonyms.add(synonym)
                
                if len(synonyms) >= max_synonyms:
                    break
            if len(synonyms) >= max_synonyms:
                break
        
        return list(synonyms)
    
    def _get_related_terms(self, word: str) -> List[str]:
        """Get semantically related terms (hyponyms, hypernyms)."""
        related = set()
        
        for syn in wordnet.synsets(word):
            # Hyponyms (more specific)
            for hypo in syn.hyponyms()[:2]:
                for lemma in hypo.lemmas():
                    term = lemma.name().replace('_', ' ').lower()
                    if term != word and len(term.split()) == 1:
                        related.add(term)
            
            # Hypernyms (more general)
            for hyper in syn.hypernyms()[:2]:
                for lemma in hyper.lemmas():
                    term = lemma.name().replace('_', ' ').lower()
                    if term != word and len(term.split()) == 1:
                        related.add(term)
        
        return list(related)[:3]  # Limit to 3 related terms
    
    def get_enhanced_suggestions(self, query: str, max_suggestions: int = 5) -> List[Dict[str, Any]]:
        """Get enhanced query suggestions with relevance scores."""
        if len(query) < 2:
            return []
        
        suggestions = []
        query_lower = query.lower()
        
        # 1. Prefix-based suggestions from vocabulary
        vocab_suggestions = [
            term for term in self.vocabulary 
            if term.startswith(query_lower) and len(term) > len(query_lower)
        ][:max_suggestions]
        
        for term in vocab_suggestions:
            suggestions.append({
                'suggestion': term,
                'type': 'vocabulary',
                'score': 0.9,
                'source': 'vocabulary'
            })
        
        # 2. Common query suggestions
        common_suggestions = [
            q for q in self.common_queries 
            if query_lower in q.lower() and q.lower() != query_lower
        ][:max_suggestions]
        
        for q in common_suggestions:
            suggestions.append({
                'suggestion': q,
                'type': 'common_query',
                'score': 0.8,
                'source': 'common_queries'
            })
        
        # 3. Search history suggestions
        history_suggestions = [
            q for q in self.search_history 
            if query_lower in q.lower() and q.lower() != query_lower
        ][:max_suggestions]
        
        for q in history_suggestions:
            suggestions.append({
                'suggestion': q,
                'type': 'history',
                'score': 0.7,
                'source': 'search_history'
            })
        
        # 4. Spelling correction suggestions
        if len(query.split()) == 1:  # Single word queries
            correction = self._find_best_correction(query)
            if correction != query:
                suggestions.append({
                    'suggestion': correction,
                    'type': 'spelling_correction',
                    'score': 0.6,
                    'source': 'spell_check'
                })
        
        # Sort by score and remove duplicates
        seen = set()
        unique_suggestions = []
        for s in sorted(suggestions, key=lambda x: x['score'], reverse=True):
            if s['suggestion'] not in seen:
                seen.add(s['suggestion'])
                unique_suggestions.append(s)
        
        return unique_suggestions[:max_suggestions]
    
    def get_suggestions(self, query: str, max_suggestions: int = 5) -> List[str]:
        """Backward-compatible method that returns only suggestion strings."""
        enhanced_suggestions = self.get_enhanced_suggestions(query, max_suggestions)
        return [suggestion['suggestion'] for suggestion in enhanced_suggestions]

# Maintain backward compatibility
class QueryValidator(EnhancedQueryValidator):
    """Backward-compatible query validator."""
    pass