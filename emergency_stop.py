#!/usr/bin/env python3
"""
Emergency script to stop the stuck crawler and create sample data.
"""

import os
import sys
import signal
import subprocess

def kill_scrapy_processes():
    """Kill any running Scrapy processes."""
    try:
        # For Windows
        if os.name == 'nt':
            result = subprocess.run(['tasklist', '/fi', 'imagename eq python.exe'], 
                                  capture_output=True, text=True)
            if 'scrapy' in result.stdout.lower():
                print("Killing Scrapy processes...")
                subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            # For Unix/Linux/Mac
            subprocess.run(['pkill', '-f', 'scrapy'], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print("✅ Stopped all Scrapy processes")
    except Exception as e:
        print(f"❌ Error stopping processes: {e}")

def create_immediate_samples():
    """Create immediate sample data for testing."""
    samples = [
        {
            "filename": "EMERGENCY_SAMPLE_1.html",
            "content": """<!DOCTYPE html>
<html>
<head><title>Search Engine Sample</title></head>
<body>
<h1>Search Engine Sample</h1>
<p>This is a sample document about search engines for testing.</p>
<p>Search engines use web crawlers and inverted indexes.</p>
</body>
</html>"""
        },
        {
            "filename": "EMERGENCY_SAMPLE_2.html", 
            "content": """<!DOCTYPE html>
<html>
<head><title>Web Crawling Sample</title></head>
<body>
<h1>Web Crawling Sample</h1>
<p>This is a sample document about web crawling for testing.</p>
<p>Web crawlers systematically browse the internet.</p>
</body>
</html>"""
        }
    ]
    
    os.makedirs('data/raw_html', exist_ok=True)
    
    for sample in samples:
        filepath = os.path.join('data/raw_html', sample['filename'])
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(sample['content'])
        print(f"✅ Created: {filepath}")
    
    print("📁 Created emergency sample files")

if __name__ == "__main__":
    print("🆘 EMERGENCY STOP SCRIPT")
    print("=" * 50)
    
    kill_scrapy_processes()
    create_immediate_samples()
    
    print("\n🎉 Emergency cleanup completed!")
    print("\nNow run:")
    print("1. python run_indexer.py")
    print("2. python run_processor.py")
    print("3. Visit: http://localhost:5000")