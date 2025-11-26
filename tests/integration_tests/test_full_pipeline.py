"""
Integration tests for the full search engine pipeline.
"""

import pytest
import tempfile
import os

class TestFullPipeline:
    """Integration tests for complete search engine functionality."""
    
    def test_sample_data_creation(self):
        """Test creating and indexing sample data."""
        # This test verifies the complete pipeline works
        from indexer.inverted_index import InvertedIndex
        
        # Create a simple test index
        index = InvertedIndex()
        
        # Add sample documents similar to guaranteed samples
        sample_docs = [
            {
                "id": "sample1",
                "content": "Search engine technology uses web crawling and indexing",
                "metadata": {"title": "Search Tech", "url": "http://example.com/1"}
            },
            {
                "id": "sample2", 
                "content": "Information retrieval systems process user queries",
                "metadata": {"title": "IR Systems", "url": "http://example.com/2"}
            }
        ]
        
        for doc in sample_docs:
            index.add_document(doc["id"], doc["content"], doc["metadata"])
        
        # Test search functionality
        results = index.search("search engine")
        assert len(results) > 0
        
        # Verify statistics
        stats = index.get_statistics()
        assert stats['total_documents'] == 2
        assert stats['vocabulary_size'] > 0
    
    def test_configuration_loading(self):
        """Test that configuration loads correctly."""
        from common.config import Config
        
        config = Config()
        
        # Verify essential configuration sections exist
        assert config.get('project.name') is not None
        assert config.get('crawler.user_agent') is not None
        assert config.get('indexer.min_word_length') is not None
        assert config.get('processor.host') is not None
    
    def test_logging_setup(self):
        """Test that logging is properly configured."""
        from common.logger import setup_logger
        
        logger = setup_logger('test_logger')
        
        # Verify logger works without errors
        try:
            logger.info("Test log message")
            logger.error("Test error message")
            success = True
        except Exception:
            success = False
        
        assert success == True