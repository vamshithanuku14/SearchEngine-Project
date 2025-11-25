#!/usr/bin/env python3
"""
Main script to run the query processor (Flask app).
"""

import os
import sys
import logging

# Add src to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

try:
    from common.config import Config
    from common.logger import setup_logger
    from src.processor.app import create_app
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all dependencies are installed and the project structure is correct.")
    sys.exit(1)

logger = setup_logger(__name__)

def main():
    """Main function to run the Flask application."""
    try:
        config = Config()
        
        # Create Flask app
        app = create_app()
        
        # Get server configuration
        host = config.get('processor.host', '0.0.0.0')
        port = config.get('processor.port', 5000)
        debug = config.get('processor.debug', False)
        
        logger.info(f"Starting Flask server on {host}:{port} (debug: {debug})")
        print(f"🚀 Search Engine starting on http://{host}:{port}")
        print("Press Ctrl+C to stop the server")
        
        # Run the application
        app.run(host=host, port=port, debug=debug)
        
    except Exception as e:
        logger.error(f"Error running processor: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()