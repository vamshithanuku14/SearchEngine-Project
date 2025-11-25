#!/usr/bin/env python3
"""
Setup script to configure the project environment.
"""

import os
import sys

def setup_environment():
    """Setup Python environment for the project."""
    
    # Add src to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(current_dir, 'src')
    
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
        print(f"Added {src_dir} to Python path")
    
    # Create necessary directories
    directories = [
        'data/raw_html',
        'data/processed', 
        'data/index',
        'data/queries',
        'data/results',
        'logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
    
    print("Project setup completed successfully!")
    print("\nNext steps:")
    print("1. Run: python run_crawler.py (to download web pages)")
    print("2. Run: python run_indexer.py (to build search index)")
    print("3. Run: python run_processor.py (to start search engine)")

if __name__ == "__main__":
    setup_environment()