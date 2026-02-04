# conftest.py
"""Pytest configuration for multi-agent dev team tests."""

import sys
from pathlib import Path

# Add project root to Python path so tests can import utils module
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
