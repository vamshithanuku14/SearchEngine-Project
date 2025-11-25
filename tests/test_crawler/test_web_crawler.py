import pytest
import scrapy
from scrapy.http import Response, Request
from src.crawler.spiders.web_crawler import WebCrawlerSpider
from src.crawler.items import WebDocumentItem

class TestWebCrawler:
    
    def test_spider_initialization(self):
        """Test spider initialization with custom parameters."""
        spider = WebCrawlerSpider(seed_url='https://example.com', max_pages=100)
        assert spider.start_urls == ['https://example.com']
        assert spider.max_pages == 100
    
    def test_parse_page(self):
        """Test page parsing functionality."""
        spider = WebCrawlerSpider()
        
        # Create a mock response
        mock_response = scrapy.http.HtmlResponse(
            url='https://example.com',
            body='<html><title>Test Page</title><body>Test content</body></html>',
            encoding='utf-8'
        )
        mock_response.meta = {'depth': 1}
        
        # Parse the page
        results = list(spider.parse_page(mock_response))
        
        assert len(results) == 1
        item = results[0]
        assert isinstance(item, WebDocumentItem)
        assert item['url'] == 'https://example.com'
        assert item['title'] == 'Test Page'