import os
import sys

# Add src to Python path
current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src_dir = os.path.join(current_dir, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from common.config import Config

config = Config()

# Scrapy settings
BOT_NAME = 'search_engine_crawler'

SPIDER_MODULES = ['src.crawler.spiders']
NEWSPIDER_MODULE = 'src.crawler.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests
CONCURRENT_REQUESTS = config.get('crawler.concurrent_requests', 16)
CONCURRENT_REQUESTS_PER_DOMAIN = 8

# Configure delay
DOWNLOAD_DELAY = config.get('crawler.download_delay', 1.0)
RANDOMIZE_DOWNLOAD_DELAY = True

# Autothrottle
AUTOTHROTTLE_ENABLED = config.get('crawler.auto_throttle', True)
AUTOTHROTTLE_START_DELAY = 1.0
AUTOTHROTTLE_MAX_DELAY = 10.0
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0

# Configure timeout
DOWNLOAD_TIMEOUT = config.get('crawler.timeout', 30)

# User agent
USER_AGENT = config.get('crawler.user_agent')

# Configure middlewares
DOWNLOADER_MIDDLEWARES = {
    'src.crawler.middlewares.RandomUserAgentMiddleware': 400,
    'src.crawler.middlewares.PoliteCrawlingMiddleware': 543,
    'src.crawler.middlewares.ContentFilterMiddleware': 600,
}

# Configure item pipelines - FIXED: Use the correct module path
ITEM_PIPELINES = {
    'crawler.pipelines.ContentProcessingPipeline': 300,
}

# Configure logging
LOG_LEVEL = 'INFO'

# Depth limit
DEPTH_LIMIT = config.get('crawler.max_depth', 3)

# Configure caching
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3600  # 1 hour

# Respect domains
if config.get('crawler.respected_domains'):
    allowed_domains = config.get('crawler.respected_domains')