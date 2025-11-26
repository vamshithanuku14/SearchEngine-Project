"""
Tests for the inverted index component.
"""

import pytest
import tempfile
import os
import json

class TestInvertedIndex:
    """Test cases for inverted index functionality."""
    
    def test_indexer_import(self):
        """Test that indexer components can be imported."""
        from indexer.inverted_index import InvertedIndex
        from indexer.tfidf_calculator import TFIDFCalculator
        
        assert InvertedIndex is not None
        assert TFIDFCalculator is not None
    
    def test_inverted_index_creation(self):
        """Test creating an inverted index."""
        from indexer.inverted_index import InvertedIndex
        
        index = InvertedIndex()
        
        # Test initial state
        assert index.total_documents == 0
        assert len(index.vocabulary) == 0
        assert len(index.index) == 0
    
    def test_add_document(self):
        """Test adding documents to index."""
        from indexer.inverted_index import InvertedIndex
        
        index = InvertedIndex()
        
        # Add a test document
        test_doc_id = "test_doc_1"
        test_content = "This is a test document about search engines and web crawling"
        test_metadata = {
            "url": "https://example.com/test",
            "title": "Test Document"
        }
        
        index.add_document(test_doc_id, test_content, test_metadata)
        
        # Verify document was added
        assert index.total_documents == 1
        assert test_doc_id in index.document_metadata
        assert len(index.vocabulary) > 0
    
    def test_text_preprocessing(self):
        """Test text preprocessing functionality."""
        from indexer.inverted_index import InvertedIndex
        
        index = InvertedIndex()
        
        test_text = "This is a TEST document with multiple words!"
        processed_tokens = index.preprocess_text(test_text)
        
        assert isinstance(processed_tokens, list)
        assert len(processed_tokens) > 0
        # All tokens should be lowercase and cleaned
        assert all(token.islower() for token in processed_tokens)
        assert all(token.isalnum() for token in processed_tokens)
    
    def test_save_load_index(self):
        """Test saving and loading index."""
        from indexer.inverted_index import InvertedIndex
        
        # Create test index
        index = InvertedIndex()
        index.add_document("doc1", "test content about search", {"title": "Test"})
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            index.save_index(temp_path)
            
            # Create new index and load
            new_index = InvertedIndex()
            new_index.load_index(temp_path)
            
            # Verify data integrity
            assert new_index.total_documents == index.total_documents
            assert new_index.vocabulary == index.vocabulary
            
        finally:
            # Cleanup
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_search_functionality(self):
        """Test basic search functionality."""
        from indexer.inverted_index import InvertedIndex
        
        index = InvertedIndex()
        
        # Add multiple test documents
        index.add_document("doc1", "search engine technology", {"title": "Doc 1"})
        index.add_document("doc2", "web crawling techniques", {"title": "Doc 2"})
        index.add_document("doc3", "information retrieval systems", {"title": "Doc 3"})
        
        # Test search
        results = index.search("search engine", top_k=5)
        
        assert isinstance(results, list)
        # Should find at least one document
        assert len(results) >= 1
    
    def test_index_statistics(self):
        """Test index statistics calculation."""
        from indexer.inverted_index import InvertedIndex
        
        index = InvertedIndex()
        index.add_document("doc1", "test content", {"title": "Test"})
        index.add_document("doc2", "more test content", {"title": "Test 2"})
        
        stats = index.get_statistics()
        
        assert isinstance(stats, dict)
        assert 'total_documents' in stats
        assert 'vocabulary_size' in stats
        assert 'total_terms' in stats
        assert stats['total_documents'] == 2