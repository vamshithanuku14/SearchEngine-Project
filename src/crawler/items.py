import scrapy

class WebDocumentItem(scrapy.Item):
    """Scrapy item for web document data."""
    
    # Required fields
    document_id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    html_content = scrapy.Field()
    links = scrapy.Field()
    depth = scrapy.Field()
    timestamp = scrapy.Field()
    
    # Enhanced fields for multi-domain support
    domain = scrapy.Field()
    content_type = scrapy.Field()
    content_length = scrapy.Field()
    encoding = scrapy.Field()
    last_modified = scrapy.Field()
    meta_description = scrapy.Field()
    metadata = scrapy.Field()
    
    # Processing fields (added to fix the error)
    word_count = scrapy.Field()
    token_count = scrapy.Field()