import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
from common.config import Config
from common.logger import setup_logger
from crawler.items import WebDocumentItem

logger = setup_logger(__name__)

class WebCrawlerSpider(CrawlSpider):
    """Enhanced web crawler for search engine project with multi-domain support."""
    
    name = "web_crawler"
    
    def __init__(self, seed_url=None, max_pages=None, *args, **kwargs):
        super(WebCrawlerSpider, self).__init__(*args, **kwargs)
        
        self.config = Config()
        
        # Set starting URL - enhanced to handle multiple domains
        if seed_url:
            # Support comma-separated URLs
            if ',' in seed_url:
                self.start_urls = [url.strip() for url in seed_url.split(',')]
            else:
                self.start_urls = [seed_url]
        else:
            # Enhanced default seed URLs with multiple domains
            self.start_urls = [
                "https://en.wikipedia.org/wiki/Search_engine",
                "https://en.wikipedia.org/wiki/Information_retrieval",
                "https://en.wikipedia.org/wiki/Web_crawler"
            ]
        
        # Configure maximum pages
        self.max_pages = max_pages or self.config.get('crawler.max_pages', 100)
        self.pages_crawled = 0
        self.should_stop = False
        
        # Enhanced domain configuration - extract from start URLs
        config_domains = self.config.get('crawler.respected_domains', [])
        
        if config_domains:
            # Use domains from config if specified
            self.allowed_domains = config_domains
        else:
            # Extract domains from start URLs automatically
            self.allowed_domains = []
            for url in self.start_urls:
                domain = urlparse(url).netloc
                # Remove www. prefix and get base domain
                if domain.startswith('www.'):
                    domain = domain[4:]
                # Add both with and without www for flexibility
                if domain not in self.allowed_domains:
                    self.allowed_domains.append(domain)
        
        # Enhanced rules for better multi-domain crawling
        self.rules = (
            Rule(
                LinkExtractor(
                    allow_domains=self.allowed_domains,
                    deny_extensions=['pdf', 'doc', 'docx', 'zip', 'exe', 'jpg', 'png', 'gif', 'mp4', 'mp3', 'avi', 'mov'],
                    deny=(
                        r'/login', r'/signin', r'/register', r'/signup',
                        r'/api/', r'/ajax/', r'/cart', r'/checkout',
                        r'/search', r'/tag/', r'/category/'
                    )
                ),
                callback='parse_page',
                follow=True,
                process_request='process_request'
            ),
        )
        
        super()._compile_rules()
        
        logger.info(f" Enhanced crawler initialized with {len(self.start_urls)} seed URLs")
        logger.info(f" Allowed domains: {self.allowed_domains}")
        logger.info(f" Max pages: {self.max_pages}")
        logger.info(f" Seed URLs: {self.start_urls}")
    
    def process_request(self, request, response):
        """Process each request before it's downloaded with enhanced logging."""
        if self.should_stop:
            logger.debug(f"Spider stopping, skipping request: {request.url}")
            return None
        
        if self.pages_crawled >= self.max_pages:
            logger.info(f"Reached max pages limit ({self.max_pages}), stopping crawl")
            self.should_stop = True
            return None
        
        # Add depth tracking
        depth = response.meta.get('depth', 0) + 1 if response else 0
        request.meta['depth'] = depth
        
        # Add domain information for better logging
        domain = urlparse(request.url).netloc
        request.meta['domain'] = domain
        
        return request
    
    def parse_start_url(self, response):
        """Parse start URLs."""
        return self.parse_page(response)
    
    def parse_page(self, response):
        """Parse individual web page with enhanced multi-domain support."""
        if self.should_stop:
            logger.debug("Spider stopping, skipping page parsing")
            return
        
        if self.pages_crawled >= self.max_pages:
            if not self.should_stop:
                logger.info(f"Final page reached max limit ({self.max_pages}), stopping spider")
                self.should_stop = True
                self.crawler.engine.close_spider(self, 'max_pages_reached')
            return
        
        self.pages_crawled += 1
        domain = response.meta.get('domain', urlparse(response.url).netloc)
        
        logger.info(f" Crawling page {self.pages_crawled}/{self.max_pages} from {domain}: {response.url}")
        
        # Create document item
        item = WebDocumentItem()
        
        item['url'] = response.url
        item['html_content'] = response.text
        item['depth'] = response.meta.get('depth', 0)
        item['timestamp'] = response.headers.get('Date', b'').decode('utf-8')
        item['domain'] = domain
        
        # Enhanced title extraction
        title = (response.css('title::text').get() or 
                response.css('h1::text').get() or 
                response.css('h2::text').get() or 
                response.url)
        item['title'] = title.strip() if title else response.url
        
        # Enhanced content type detection
        content_type = response.headers.get('Content-Type', b'').decode('utf-8')
        item['content_type'] = content_type
        
        # Extract meta description for better snippets
        meta_desc = response.css('meta[name="description"]::attr(content)').get()
        if meta_desc:
            item['meta_description'] = meta_desc.strip()
        
        # Extract links only if we haven't reached the limit
        if not self.should_stop and self.pages_crawled < self.max_pages:
            links = []
            for link in response.css('a::attr(href)').getall():
                if link and link.startswith(('http://', 'https://')):
                    # Filter by allowed domains with better matching
                    link_domain = urlparse(link).netloc
                    if any(allowed_domain in link_domain for allowed_domain in self.allowed_domains):
                        links.append(link)
            item['links'] = links
        else:
            item['links'] = []
        
        content_length = len(item.get('html_content', ''))
        logger.debug(f"Extracted content from {response.url}: {content_length} characters")
        
        yield item
        
        # Force stop if we reached the limit after yielding
        if self.pages_crawled >= self.max_pages and not self.should_stop:
            logger.info(f" Reached max pages limit ({self.max_pages}), forcing spider stop")
            self.should_stop = True
            self.crawler.engine.close_spider(self, 'max_pages_reached')
    
    def closed(self, reason):
        """Called when spider closes with enhanced reporting."""
        logger.info(f" Crawler finished: {reason}")
        logger.info(f" Total pages crawled: {self.pages_crawled}")
        
        # Domain distribution report
        if hasattr(self, 'crawler') and hasattr(self.crawler.stats, 'stats'):
            stats = self.crawler.stats.stats
            logger.info(" Crawling Statistics:")
            for key, value in stats.items():
                logger.info(f"   {key}: {value}")
