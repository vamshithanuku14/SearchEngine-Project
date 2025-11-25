#!/usr/bin/env python3
"""
Main script to run the web crawler.
"""

import os
import sys
import logging

# Add src to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

try:
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings
    from common.config import Config
    from common.logger import setup_logger
    from src.crawler.spiders.web_crawler import WebCrawlerSpider
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all dependencies are installed and the project structure is correct.")
    sys.exit(1)

logger = setup_logger(__name__)

def main():
    """Main function to run the crawler."""
    try:
        config = Config()
        
        # Get crawler settings
        settings = get_project_settings()
        
        # Create crawler process
        process = CrawlerProcess(settings)
        
        # Get parameters
        print("Web Crawler Configuration:")
        seed_url = input("Enter seed URL (press Enter for default Wikipedia pages): ").strip()
        max_pages = input("Enter maximum pages to crawl (default 100): ").strip()
        
        seed_urls = [seed_url] if seed_url else None
        max_pages = int(max_pages) if max_pages.isdigit() else 100
        
        logger.info("Starting web crawler...")
        logger.info(f"Seed URL: {seed_urls or 'Default Wikipedia pages'}")
        logger.info(f"Max pages: {max_pages}")
        
        # Start crawler
        process.crawl(WebCrawlerSpider, seed_url=seed_url, max_pages=max_pages)
        process.start()
        
        logger.info("Web crawling completed successfully")
        
    except KeyboardInterrupt:
        logger.info("Crawler interrupted by user")
    except Exception as e:
        logger.error(f"Error running crawler: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()