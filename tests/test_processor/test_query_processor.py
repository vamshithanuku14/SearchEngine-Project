"""
Tests for the query processor component.
"""

import pytest

class TestQueryProcessor:
    """Test cases for query processing functionality."""
    
    def test_processor_import(self):
        """Test that processor components can be imported."""
        from src.processor.app import create_app
        from src.processor.query_validator import QueryValidator
        from src.processor.results_generator import ResultsGenerator
        
        assert create_app is not None
        assert QueryValidator is not None
        assert ResultsGenerator is not None
    
    def test_query_validation(self):
        """Test query validation functionality."""
        from src.processor.query_validator import QueryValidator
        
        validator = QueryValidator()
        
        # Test valid query
        result = validator.validate_query("search engine")
        assert result['valid'] == True
        assert 'cleaned_query' in result
        
        # Test empty query
        result = validator.validate_query("")
        assert result['valid'] == False
        
        # Test query with invalid characters
        result = validator.validate_query("search@engine")
        assert result['valid'] == False
    
    def test_query_suggestions(self):
        """Test query suggestions."""
        from src.processor.query_validator import QueryValidator
        
        validator = QueryValidator()
        
        suggestions = validator.get_suggestions("searc")
        
        assert isinstance(suggestions, list)
        # Should return some suggestions for partial query
        assert len(suggestions) > 0
        assert all(isinstance(s, str) for s in suggestions)
        
        # Test with empty query
        empty_suggestions = validator.get_suggestions("a")
        assert isinstance(empty_suggestions, list)
    
    def test_app_creation(self):
        """Test Flask app creation."""
        from src.processor.app import create_app
        
        app = create_app()
        
        assert app is not None
        # Test that app has expected configuration
        assert hasattr(app, 'config')