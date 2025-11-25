#!/usr/bin/env python3
"""
Verify the pipeline fix is working.
"""

import os
import sys
from scrapy.utils.project import get_project_settings

def verify_pipeline_fix():
    """Verify the pipeline is now properly configured."""
    print("🔧 Verifying Pipeline Fix")
    print("=" * 50)
    
    try:
        settings = get_project_settings()
        pipelines = settings.get('ITEM_PIPELINES', {})
        
        print("ITEM_PIPELINES configuration:")
        for pipeline, priority in pipelines.items():
            print(f"  {pipeline}: {priority}")
        
        our_pipeline = 'src.crawler.pipelines.ContentProcessingPipeline'
        if our_pipeline in pipelines:
            print(f"✅ SUCCESS: Our pipeline is now enabled with priority {pipelines[our_pipeline]}")
            return True
        else:
            print(f"❌ FAILED: Our pipeline is still not in ITEM_PIPELINES")
            print("Available pipelines:")
            for pipeline in pipelines:
                print(f"  - {pipeline}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking settings: {e}")
        return False

if __name__ == "__main__":
    success = verify_pipeline_fix()
    
    if success:
        print("\n🎉 Pipeline fix verified! Now run:")
        print("1. python run_crawler.py")
        print("2. dir data\\raw_html (should show files)")
        print("3. python run_indexer.py")
        print("4. python run_processor.py")
    else:
        print("\n❌ Fix not working. The pipeline path might be wrong.")