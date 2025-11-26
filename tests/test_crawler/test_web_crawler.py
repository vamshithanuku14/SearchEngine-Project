"""
Tests for the web crawler component.
"""

import pytest
import tempfile
import os

class TestWebCrawler:
    """Test cases for web crawler functionality."""
    
    def test_crawler_import(self):
        """Test that crawler components can be imported."""
        # Test basic imports
        from crawler.items import WebDocumentItem
        from crawler.pipelines import ContentProcessingPipeline
        
        # Verify classes exist
        assert WebDocumentItem is not None
        assert ContentProcessingPipeline is not None
    
    def test_pipeline_functionality(self):
        """Test content processing pipeline."""
        from crawler.pipelines import ContentProcessingPipeline
        
        pipeline = ContentProcessingPipeline()
        
        # Test document ID generation
        test_url = "https://example.com/test"
        doc_id = pipeline.generate_document_id(test_url)
        
        assert doc_id is not None
        assert len(doc_id) == 32  # MD5 hash length
        assert doc_id.isupper()
    
    def test_item_structure(self):
        """Test WebDocumentItem structure."""
        from crawler.items import WebDocumentItem
        
        item = WebDocumentItem()
        
        # Test that required fields exist
        assert 'url' in item.fields
        assert 'title' in item.fields
        assert 'content' in item.fields
        assert 'html_content' in item.fields
        assert 'document_id' in item.fields
    
    def test_config_loading(self):
        """Test configuration loading."""
        from common.config import Config
        
        config = Config()
        
        # Test that config can be loaded
        assert config is not None
        assert config.get('project.name') == "SearchEngine-Project"