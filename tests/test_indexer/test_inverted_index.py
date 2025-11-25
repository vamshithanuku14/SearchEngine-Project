import pytest
import tempfile
import os
from src.indexer.inverted_index import InvertedIndex

class TestInvertedIndex:
    
    def test_preprocess_text(self):
        """Test text preprocessing."""
        index = InvertedIndex()
        text = "This is a test document with multiple words."
        tokens = index.preprocess_text(text)
        
        assert isinstance(tokens, list)
        assert len(tokens) > 0
        # All tokens should be lowercase and stemmed
        assert all(token.islower() for token in tokens)
    
    def test_add_document(self):
        """Test adding documents to index."""
        index = InvertedIndex()
        document_id = "test_doc_1"
        content = "hello world test document"
        metadata = {"url": "http://example.com", "title": "Test Document"}
        
        index.add_document(document_id, content, metadata)
        
        assert document_id in index.document_metadata
        assert index.total_documents == 1
        assert len(index.vocabulary) > 0
    
    def test_save_load_index(self):
        """Test saving and loading index."""
        index = InvertedIndex()
        
        # Add a test document
        index.add_document("doc1", "test content", {"title": "Test"})
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            index.save_index(temp_path)
            
            # Create new index and load
            new_index = InvertedIndex()
            new_index.load_index(temp_path)
            
            assert new_index.total_documents == index.total_documents
            assert new_index.vocabulary == index.vocabulary
            
        finally:
            os.unlink(temp_path)