"""
Global Tools Package
Based on Global Professional Core Prompt v33.2

This package provides:
- lifecycle.py: The ONLY entry point for project lifecycle management
- librarian.py: File registry manager
- speckit_bridge.py: Spec file manager

Usage:
    from global.tools import lifecycle, librarian, speckit_bridge
    
    # Or run from command line:
    python3 global/tools/lifecycle.py "<Project Name>" "<Description>"
    python3 global/tools/librarian.py check <file_path>
    python3 global/tools/speckit_bridge.py create <feature_name>
"""

__version__ = '1.0.0'
__author__ = 'AI Agent'

from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TOOLS_DIR.parent.parent
