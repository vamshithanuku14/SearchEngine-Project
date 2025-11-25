import random
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from common.logger import setup_logger

logger = setup_logger(__name__)

class RandomUserAgentMiddleware(UserAgentMiddleware):
    """Randomize user agents to avoid blocking."""
    
    def __init__(self, user_agent):
        self.user_agent = user_agent
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('USER_AGENT'))
    
    def process_request(self, request, spider):
        user_agents = [
            self.user_agent,
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        ]
        request.headers['User-Agent'] = random.choice(user_agents)

class PoliteCrawlingMiddleware:
    """Ensure polite crawling by respecting robots.txt and adding delays."""
    
    def __init__(self, download_delay):
        self.download_delay = download_delay
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('DOWNLOAD_DELAY', 1.0))
    
    def process_request(self, request, spider):
        # Respect robots.txt
        request.meta['dont_obey_robotstxt'] = False
        logger.debug(f"Processing request for: {request.url}")

class ContentFilterMiddleware:
    """Filter content by type and size."""
    
    def process_response(self, request, response, spider):
        content_type = response.headers.get('Content-Type', b'').decode('utf-8').lower()
        
        # Only process HTML content
        if 'text/html' not in content_type:
            logger.debug(f"Skipping non-HTML content: {request.url}")
            return response
        
        # Check content length (skip very large pages)
        content_length = len(response.body)
        if content_length > 10 * 1024 * 1024:  # 10MB
            logger.warning(f"Content too large ({content_length} bytes): {request.url}")
            return response
        
        return response