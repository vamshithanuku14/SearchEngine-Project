"""
URL management utilities for the crawler.
"""

from urllib.parse import urlparse
from collections import deque
from common.logger import setup_logger

logger = setup_logger(__name__)

class URLManager:
    """Manage URLs for crawling with prioritization and deduplication."""
    
    def __init__(self, seed_urls: list, max_pages: int = 1000):
        self.seed_urls = seed_urls
        self.max_pages = max_pages
        self.visited_urls = set()
        self.url_queue = deque()
        self.domain_count = {}
        
        # Initialize with seed URLs
        for url in seed_urls:
            self.add_url(url, depth=0)
    
    def add_url(self, url: str, depth: int = 0, parent_url: str = None):
        """
        Add URL to crawl queue if it meets criteria.
        
        Args:
            url: URL to add
            depth: Current crawl depth
            parent_url: Parent URL for tracking
        """
        from . import is_valid_url, normalize_url
        
        normalized_url = normalize_url(url)
        
        # Check if we've already visited this URL
        if normalized_url in self.visited_urls:
            return False
        
        # Check if URL is valid
        if not is_valid_url(normalized_url):
            return False
        
        # Check if we've reached max pages
        if len(self.visited_urls) >= self.max_pages:
            return False
        
        # Check domain limits
        domain = urlparse(normalized_url).netloc
        if self.domain_count.get(domain, 0) >= self.max_pages // len(self.seed_urls):
            return False
        
        # Add to queue
        self.url_queue.append({
            'url': normalized_url,
            'depth': depth,
            'parent_url': parent_url
        })
        
        self.visited_urls.add(normalized_url)
        self.domain_count[domain] = self.domain_count.get(domain, 0) + 1
        
        logger.debug(f"Added URL to queue: {normalized_url} (depth: {depth})")
        return True
    
    def get_next_url(self) -> dict:
        """
        Get next URL from queue.
        
        Returns:
            URL info dictionary or None if queue is empty
        """
        if self.url_queue:
            return self.url_queue.popleft()
        return None
    
    def get_queue_size(self) -> int:
        """Get current queue size."""
        return len(self.url_queue)
    
    def get_visited_count(self) -> int:
        """Get count of visited URLs."""
        return len(self.visited_urls)
    
    def is_complete(self) -> bool:
        """Check if crawling is complete."""
        return len(self.visited_urls) >= self.max_pages or not self.url_queue