"""
File: examples/init_py_patterns/03_plugin_system/__init__.py
Pattern: Dynamic Plugin Discovery

Use Case:
- Extensible applications
- Plugin architectures
- Auto-discovery of modules

Real-world examples:
- pytest plugins
- Flask extensions
- Django apps
"""

import importlib
import pkgutil
from typing import Dict, Type, Protocol
from pathlib import Path


class Plugin(Protocol):
    """Plugin protocol - all plugins must implement this"""
    name: str
    version: str
    
    def initialize(self) -> None:
        """Initialize the plugin"""
        ...
    
    def execute(self, *args, **kwargs):
        """Execute plugin functionality"""
        ...


# Global plugin registry
_plugins: Dict[str, Type[Plugin]] = {}


def discover_plugins() -> None:
    """
    Automatically discover and register all plugins
    
    Looks for all Python modules in the plugins directory
    and registers those that have a 'register_plugin' function.
    """
    global _plugins
    
    # Get the package path
    package_path = Path(__file__).parent
    
    # Iterate through all modules in this package
    for _, module_name, is_pkg in pkgutil.iter_modules([str(package_path)]):
        # Skip __init__ and non-plugin modules
        if module_name.startswith('_'):
            continue
        
        # Import the module
        try:
            module = importlib.import_module(f'{__package__}.{module_name}')
            
            # Check if module has register_plugin function
            if hasattr(module, 'register_plugin'):
                plugin_class = module.register_plugin()
                _plugins[plugin_class.name] = plugin_class
                print(f"✅ Registered plugin: {plugin_class.name} v{plugin_class.version}")
        
        except Exception as e:
            print(f"❌ Failed to load plugin {module_name}: {e}")


def get_plugin(name: str) -> Type[Plugin] | None:
    """
    Get plugin by name
    
    Args:
        name: Plugin name
        
    Returns:
        Plugin class or None if not found
        
    Example:
        plugin_class = get_plugin('example')
        plugin = plugin_class()
        plugin.execute()
    """
    if not _plugins:
        discover_plugins()
    
    return _plugins.get(name)


def list_plugins() -> list[str]:
    """
    List all available plugins
    
    Returns:
        List of plugin names
    """
    if not _plugins:
        discover_plugins()
    
    return list(_plugins.keys())


def load_all_plugins() -> Dict[str, Plugin]:
    """
    Load and initialize all plugins
    
    Returns:
        Dictionary of initialized plugin instances
    """
    if not _plugins:
        discover_plugins()
    
    instances = {}
    for name, plugin_class in _plugins.items():
        try:
            instance = plugin_class()
            instance.initialize()
            instances[name] = instance
        except Exception as e:
            print(f"❌ Failed to initialize plugin {name}: {e}")
    
    return instances


# Public API
__all__ = [
    'Plugin',
    'discover_plugins',
    'get_plugin',
    'list_plugins',
    'load_all_plugins',
]

# Auto-discover on import (optional - can be disabled)
# discover_plugins()

