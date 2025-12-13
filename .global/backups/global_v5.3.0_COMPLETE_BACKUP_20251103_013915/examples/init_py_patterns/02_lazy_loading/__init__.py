"""
File: examples/init_py_patterns/02_lazy_loading/__init__.py
Pattern: Lazy Loading for Performance

Use Case:
- Heavy modules that aren't always needed
- CLI tools with multiple commands
- Improves startup time significantly

Performance Impact:
- Without lazy loading: ~500ms import time
- With lazy loading: ~50ms import time
"""

from typing import TYPE_CHECKING

# Always imported (lightweight)
from .version import __version__
from .exceptions import ToolError

# Type hints only (no runtime cost)
if TYPE_CHECKING:
    from .analyzer import CodeAnalyzer
    from .formatter import CodeFormatter
    from .linter import CodeLinter

__all__ = [
    # Version
    '__version__',
    # Exceptions
    'ToolError',
    # Lazy-loaded (via functions)
    'get_analyzer',
    'get_formatter',
    'get_linter',
]


def get_analyzer():
    """
    Get CodeAnalyzer instance (lazy loaded)
    
    Returns:
        CodeAnalyzer: The analyzer instance
        
    Example:
        analyzer = get_analyzer()
        results = analyzer.analyze('/path/to/code')
    """
    from .analyzer import CodeAnalyzer
    return CodeAnalyzer()


def get_formatter():
    """
    Get CodeFormatter instance (lazy loaded)
    
    Returns:
        CodeFormatter: The formatter instance
    """
    from .formatter import CodeFormatter
    return CodeFormatter()


def get_linter():
    """
    Get CodeLinter instance (lazy loaded)
    
    Returns:
        CodeLinter: The linter instance
    """
    from .linter import CodeLinter
    return CodeLinter()


# Alternative: Lazy loading with __getattr__ (Python 3.7+)
def __getattr__(name: str):
    """
    Lazy load modules on attribute access
    
    This is called when an attribute is not found normally.
    Allows: from tools import CodeAnalyzer
    """
    if name == 'CodeAnalyzer':
        from .analyzer import CodeAnalyzer
        return CodeAnalyzer
    elif name == 'CodeFormatter':
        from .formatter import CodeFormatter
        return CodeFormatter
    elif name == 'CodeLinter':
        from .linter import CodeLinter
        return CodeLinter
    
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

