#!/usr/bin/env python3
"""
Working crawler that bypasses Scrapy settings issues.
"""

import os
import sys
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Add src to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

class WorkingWebCrawler(scrapy.Spider):
    """Working web crawler with manual pipeline."""
    
    name = "working_crawler"
    
    def __init__(self, seed_url=None, max_pages=5, *args, **kwargs):
        super(WorkingWebCrawler, self).__init__(*args, **kwargs)
        
        # Set starting URL
        if seed_url:
            self.start_urls = [seed_url]
        else:
            self.start_urls = [
                "https://en.wikipedia.org/wiki/Search_engine",
                "https://en.wikipedia.org/wiki/Information_retrieval",
                "https://en.wikipedia.org/wiki/Web_crawler"
            ]
        
        self.max_pages = max_pages
        self.pages_crawled = 0
        self.should_stop = False
        
        # Import pipeline directly
        from crawler.pipelines import ContentProcessingPipeline
        self.pipeline = ContentProcessingPipeline()
        
        print(f"🚀 Working crawler initialized with {len(self.start_urls)} seed URLs")
        print(f"Max pages: {self.max_pages}")
    
    def parse(self, response):
        """Parse individual web page."""
        if self.should_stop or self.pages_crawled >= self.max_pages:
            return
        
        self.pages_crawled += 1
        print(f"📥 Crawling page {self.pages_crawled}/{self.max_pages}: {response.url}")
        
        # Create item manually
        item = {
            'url': response.url,
            'html_content': response.text,
            'title': response.css('title::text').get() or response.url,
            'depth': response.meta.get('depth', 0),
            'timestamp': response.headers.get('Date', b'').decode('utf-8'),
            'links': []
        }
        
        # Process item through pipeline manually
        processed_item = self.pipeline.process_item(item, self)
        
        # Extract and follow links
        if not self.should_stop and self.pages_crawled < self.max_pages:
            for link in response.css('a::attr(href)').getall():
                if link and link.startswith(('http://', 'https://')):
                    if 'wikipedia.org' in link:  # Only follow Wikipedia links
                        yield response.follow(link, self.parse)
        
        # Check if we should stop
        if self.pages_crawled >= self.max_pages and not self.should_stop:
            print(f"✅ Reached max pages limit ({self.max_pages})")
            self.should_stop = True

def main():
    """Main function to run the working crawler."""
    try:
        print("🌐 WORKING WEB CRAWLER")
        print("=" * 50)
        
        # Get user input
        seed_url = input("Enter seed URL (press Enter for default Wikipedia pages): ").strip()
        max_pages = input("Enter maximum pages to crawl (default 5): ").strip()
        
        seed_urls = [seed_url] if seed_url else None
        max_pages = int(max_pages) if max_pages.isdigit() else 5
        
        # Create custom settings
        settings = {
            'USER_AGENT': 'SearchEngineBot/1.0',
            'ROBOTSTXT_OBEY': True,
            'CONCURRENT_REQUESTS': 1,
            'DOWNLOAD_DELAY': 1.0,
            'DEPTH_LIMIT': 2,
            'LOG_LEVEL': 'INFO'
        }
        
        # Create and start crawler process
        process = CrawlerProcess(settings)
        process.crawl(WorkingWebCrawler, seed_url=seed_url, max_pages=max_pages)
        process.start()
        
        print(f"\n✅ Crawling completed! Check data/raw_html/ for downloaded files.")
        
    except KeyboardInterrupt:
        print("\n⏹️ Crawler stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()