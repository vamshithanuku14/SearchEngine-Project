#!/usr/bin/env python3
"""
Debug why the pipeline isn't saving files.
"""

import os
import sys

# Add src to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

def test_pipeline_directly():
    """Test the pipeline directly."""
    try:
        from crawler.pipelines import ContentProcessingPipeline
        
        print(" Testing Pipeline Directly")
        print("=" * 50)
        
        # Create pipeline instance
        pipeline = ContentProcessingPipeline()
        print(f" Pipeline created")
        print(f"   Raw HTML path: {pipeline.raw_html_path}")
        print(f"   Directory exists: {os.path.exists(pipeline.raw_html_path)}")
        
        # Test saving a file directly
        test_url = "https://en.wikipedia.org/wiki/Test"
        test_html = "<html><body><h1>Test Page</h1><p>This is a test.</p></body></html>"
        
        document_id = pipeline.generate_document_id(test_url)
        print(f"   Generated document ID: {document_id}")
        
        # Test the save method
        success = pipeline._save_raw_html(document_id, test_html)
        print(f"   Save successful: {success}")
        
        # Check if file was created
        expected_file = os.path.join(pipeline.raw_html_path, f"{document_id}.html")
        print(f"   Expected file: {expected_file}")
        print(f"   File exists: {os.path.exists(expected_file)}")
        
        if os.path.exists(expected_file):
            file_size = os.path.getsize(expected_file)
            print(f"   File size: {file_size} bytes")
            
    except Exception as e:
        print(f" Pipeline test failed: {e}")
        import traceback
        traceback.print_exc()

def check_scrapy_settings():
    """Check if Scrapy is using our pipeline."""
    try:
        from scrapy.utils.project import get_project_settings
        settings = get_project_settings()
        
        print(f"\n Scrapy Settings Check")
        print("=" * 50)
        pipelines = settings.get('ITEM_PIPELINES', {})
        print(f"ITEM_PIPELINES: {pipelines}")
        
        our_pipeline = 'crawler.pipelines.ContentProcessingPipeline'
        if our_pipeline in pipelines:
            print(f" Our pipeline is enabled with priority: {pipelines[our_pipeline]}")
        else:
            print(f" Our pipeline is NOT in ITEM_PIPELINES")
            
    except Exception as e:
        print(f" Settings check failed: {e}")

if __name__ == "__main__":
    test_pipeline_directly()
    check_scrapy_settings()
