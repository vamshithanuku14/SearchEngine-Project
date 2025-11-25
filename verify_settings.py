#!/usr/bin/env python3
"""
Verify that Scrapy settings are correct.
"""

import os
import sys

# Add src to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

def check_scrapy_settings():
    """Check Scrapy settings with proper path setup."""
    try:
        # Set environment variable for Scrapy
        os.environ['SCRAPY_SETTINGS_MODULE'] = 'src.crawler.settings'
        
        from scrapy.utils.project import get_project_settings
        settings = get_project_settings()
        
        print("🔧 Scrapy Settings Verification")
        print("=" * 50)
        
        # Check pipelines
        pipelines = settings.get('ITEM_PIPELINES', {})
        print(f"ITEM_PIPELINES: {pipelines}")
        
        our_pipeline = 'src.crawler.pipelines.ContentProcessingPipeline'
        if our_pipeline in pipelines:
            print(f"✅ Our pipeline is ENABLED with priority: {pipelines[our_pipeline]}")
        else:
            print(f"❌ Our pipeline is NOT in ITEM_PIPELINES")
            print(f"   Available pipelines: {list(pipelines.keys())}")
        
        # Check other important settings
        print(f"\n📋 Other Settings:")
        print(f"   SPIDER_MODULES: {settings.get('SPIDER_MODULES')}")
        print(f"   BOT_NAME: {settings.get('BOT_NAME')}")
        
    except Exception as e:
        print(f"❌ Settings verification failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_scrapy_settings()