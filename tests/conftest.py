import os
import sys
import pytest

# Add src to Python path for tests
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
src_dir = os.path.join(project_root, 'src')
sys.path.insert(0, src_dir)
sys.path.insert(0, project_root)

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment before each test."""
    # Ensure data directories exist
    os.makedirs('tests/test_data', exist_ok=True)
    os.makedirs('tests/test_data/raw_html', exist_ok=True)
    os.makedirs('tests/test_data/index', exist_ok=True)
    yield
    # Cleanup after tests if needed