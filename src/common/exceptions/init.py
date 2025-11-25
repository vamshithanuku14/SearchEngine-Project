class SearchEngineError(Exception):
    """Base exception for search engine project."""
    pass

class CrawlerError(SearchEngineError):
    """Crawler related exceptions."""
    pass

class IndexerError(SearchEngineError):
    """Indexer related exceptions."""
    pass

class ProcessorError(SearchEngineError):
    """Processor related exceptions."""
    pass

class ConfigurationError(SearchEngineError):
    """Configuration related exceptions."""
    pass

class QueryValidationError(ProcessorError):
    """Query validation exceptions."""
    pass