import os
import hashlib
import json
from urllib.parse import urlparse
import sys
import os

# Add src to Python path for imports
current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src_dir = os.path.join(current_dir, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from common.config import Config
from common.logger import setup_logger

logger = setup_logger(__name__)

class ContentProcessingPipeline:
    """Process and clean web content with enhanced multi-domain support."""
    
    def __init__(self):
        self.config = Config()
        self.raw_html_path = self.config.get('paths.data_raw')
        self.saved_count = 0
    
    def generate_document_id(self, url: str) -> str:
        """Generate unique document ID from URL."""
        return hashlib.md5(url.encode('utf-8')).hexdigest().upper()
    
    def process_item(self, item, spider):
        """Process crawled item with enhanced fields."""
        try:
            # Generate document ID if not present
            if 'document_id' not in item:
                item['document_id'] = self.generate_document_id(item['url'])
            
            # Save raw HTML content
            self._save_raw_html(item['document_id'], item['html_content'])
            
            # Clean and extract text content
            item['content'] = self._extract_clean_text(item['html_content'])
            
            # Add enhanced metadata - only use fields that exist in WebDocumentItem
            item['content_length'] = len(item['html_content'])
            
            # Calculate word count safely
            content_text = item.get('content', '')
            word_count = len(content_text.split()) if content_text else 0
            item['word_count'] = word_count
            
            # Ensure domain field is set
            if 'domain' not in item:
                item['domain'] = urlparse(item['url']).netloc
            
            # Set encoding if not present
            if 'encoding' not in item:
                item['encoding'] = 'utf-8'
            
            # Create metadata dictionary - store additional info here
            item['metadata'] = {
                'domain': item['domain'],
                'content_type': item.get('content_type', 'text/html'),
                'content_length': item['content_length'],
                'word_count': word_count,
                'depth': item.get('depth', 0),
                'timestamp': item.get('timestamp', ''),
                'has_meta_description': 'meta_description' in item
            }
            
            self.saved_count += 1
            logger.info(f"✅ Processed document: {item['document_id']} from {item['domain']} (Total: {self.saved_count})")
            return item
            
        except Exception as e:
            logger.error(f"Error processing item {item['url']}: {str(e)}")
            return item
    
    def _save_raw_html(self, document_id: str, html_content: str):
        """Save raw HTML to file."""
        filename = f"{document_id}.html"
        filepath = os.path.join(self.raw_html_path, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            file_size = os.path.getsize(filepath)
            logger.debug(f"💾 Saved: {filename} ({file_size} bytes)")
            
        except Exception as e:
            logger.error(f"Error saving HTML file {filename}: {str(e)}")
    
    def _extract_clean_text(self, html_content: str) -> str:
        """Extract clean text from HTML content."""
        try:
            from bs4 import BeautifulSoup
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer", "aside", "meta", "link"]):
                script.decompose()
            
            # Get text and clean it
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text
            
        except Exception as e:
            logger.error(f"Error extracting text from HTML: {str(e)}")
            return ""
    
    def close_spider(self, spider):
        """Called when spider closes."""
        logger.info(f"🏁 Pipeline processing completed. Total documents processed: {self.saved_count}")
        
        # Show summary of processed domains
        if hasattr(spider, 'allowed_domains'):
            logger.info(f"🌐 Domains processed: {spider.allowed_domains}")