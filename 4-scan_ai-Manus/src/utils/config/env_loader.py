#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Environment variables loader for the Agricultural AI System.
Handles loading environment variables from .env file and substituting them in configuration.
"""

import os
import re
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List, Union, Set

logger = logging.getLogger('env_loader')

class EnvLoader:
    """
    Environment variables loader for the Agricultural AI System.
    
    This class handles:
    - Loading environment variables from .env file
    - Substituting environment variables in configuration values
    - Providing access to environment variables with type conversion
    """
    
    ENV_PATTERN = re.compile(r'\${([A-Za-z0-9_]+)(?::([^}]*))?}')
    
    def __init__(self, env_file: Optional[str] = None, auto_reload: bool = False):
        """
        Initialize the environment loader.
        
        Args:
            env_file (str, optional): Path to the .env file. If None, looks for .env in the project root.
            auto_reload (bool, optional): Whether to automatically reload environment variables when accessed.
        """
        self.env_vars = {}
        self.env_file = env_file
        self.auto_reload = auto_reload
        self.last_load_time = 0
        
        # Load environment variables from .env file
        self._load_env_file()
    
    def _load_env_file(self) -> None:
        """Load environment variables from .env file."""
        if not self.env_file:
            # Check if ENV_FILE environment variable is set
            env_file_path = os.environ.get('ENV_FILE')
            if env_file_path:
                self.env_file = env_file_path
            else:
                # Try to find .env file in project root
                project_root = Path(__file__).parent.parent.parent.parent
                self.env_file = project_root / '.env'
        
        if not os.path.exists(self.env_file):
            logger.warning(f".env file not found at {self.env_file}. Using only system environment variables.")
            return
        
        logger.info(f"Loading environment variables from {self.env_file}")
        
        try:
            with open(self.env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parse key-value pairs
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Remove quotes if present
                        if (value.startswith('"') and value.endswith('"')) or \
                           (value.startswith("'") and value.endswith("'")):
                            value = value[1:-1]
                        
                        # Store in env_vars dictionary
                        self.env_vars[key] = value
                        
                        # Also set as environment variable if not already set
                        if key not in os.environ:
                            os.environ[key] = value
                            
            # Update last load time
            self.last_load_time = os.path.getmtime(self.env_file)
        except Exception as e:
            logger.error(f"Error loading .env file: {e}")
    
    def _check_reload(self) -> None:
        """Check if .env file has been modified and reload if necessary."""
        if not self.auto_reload or not self.env_file or not os.path.exists(self.env_file):
            return
        
        current_mtime = os.path.getmtime(self.env_file)
        if current_mtime > self.last_load_time:
            logger.info(f".env file has been modified, reloading environment variables")
            self._load_env_file()
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get environment variable value.
        
        Args:
            key (str): Environment variable name
            default (Any, optional): Default value if not found
            
        Returns:
            Any: Environment variable value or default
        """
        # Check if reload is needed
        self._check_reload()
        
        # Check in loaded env vars first, then in system environment
        value = self.env_vars.get(key, os.environ.get(key, default))
        return value
    
    def get_str(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get environment variable as string.
        
        Args:
            key (str): Environment variable name
            default (str, optional): Default value if not found
            
        Returns:
            str: Environment variable value as string or default
        """
        value = self.get(key, default)
        if value is None:
            return default
        
        return str(value)
    
    def get_int(self, key: str, default: Optional[int] = None) -> Optional[int]:
        """
        Get environment variable as integer.
        
        Args:
            key (str): Environment variable name
            default (int, optional): Default value if not found or not convertible
            
        Returns:
            int: Environment variable value as integer or default
        """
        value = self.get(key, default)
        if value is None:
            return default
        
        try:
            return int(value)
        except (ValueError, TypeError):
            logger.warning(f"Environment variable {key} is not a valid integer: {value}")
            return default
    
    def get_float(self, key: str, default: Optional[float] = None) -> Optional[float]:
        """
        Get environment variable as float.
        
        Args:
            key (str): Environment variable name
            default (float, optional): Default value if not found or not convertible
            
        Returns:
            float: Environment variable value as float or default
        """
        value = self.get(key, default)
        if value is None:
            return default
        
        try:
            return float(value)
        except (ValueError, TypeError):
            logger.warning(f"Environment variable {key} is not a valid float: {value}")
            return default
    
    def get_bool(self, key: str, default: Optional[bool] = None) -> Optional[bool]:
        """
        Get environment variable as boolean.
        
        Args:
            key (str): Environment variable name
            default (bool, optional): Default value if not found
            
        Returns:
            bool: Environment variable value as boolean or default
        """
        value = self.get(key, default)
        if value is None:
            return default
        
        if isinstance(value, bool):
            return value
        
        if isinstance(value, str):
            return value.lower() in ('true', 'yes', '1', 'y', 'on')
        
        return bool(value)
    
    def get_list(self, key: str, default: Optional[list] = None, separator: str = ',') -> Optional[list]:
        """
        Get environment variable as list.
        
        Args:
            key (str): Environment variable name
            default (list, optional): Default value if not found
            separator (str, optional): Separator for list items
            
        Returns:
            list: Environment variable value as list or default
        """
        value = self.get(key, default)
        if value is None:
            return default
        
        if isinstance(value, list):
            return value
        
        if isinstance(value, str):
            return [item.strip() for item in value.split(separator)]
        
        return default
    
    def get_dict(self, key: str, default: Optional[dict] = None) -> Optional[dict]:
        """
        Get environment variable as dictionary (JSON).
        
        Args:
            key (str): Environment variable name
            default (dict, optional): Default value if not found or not convertible
            
        Returns:
            dict: Environment variable value as dictionary or default
        """
        value = self.get(key, default)
        if value is None:
            return default
        
        if isinstance(value, dict):
            return value
        
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                logger.warning(f"Environment variable {key} is not a valid JSON: {value}")
                return default
        
        return default
    
    def get_path(self, key: str, default: Optional[str] = None) -> Optional[Path]:
        """
        Get environment variable as Path.
        
        Args:
            key (str): Environment variable name
            default (str, optional): Default value if not found
            
        Returns:
            Path: Environment variable value as Path or default
        """
        value = self.get_str(key, default)
        if value is None:
            return None
        
        return Path(value)
    
    def get_set(self, key: str, default: Optional[Set] = None, separator: str = ',') -> Optional[Set]:
        """
        Get environment variable as set.
        
        Args:
            key (str): Environment variable name
            default (set, optional): Default value if not found
            separator (str, optional): Separator for set items
            
        Returns:
            set: Environment variable value as set or default
        """
        value_list = self.get_list(key, default, separator)
        if value_list is None:
            return default
        
        if isinstance(value_list, set):
            return value_list
        
        return set(value_list)
    
    def get_all(self) -> Dict[str, str]:
        """
        Get all environment variables.
        
        Returns:
            dict: Dictionary of all environment variables
        """
        # Check if reload is needed
        self._check_reload()
        
        # Merge system environment variables with loaded env vars
        result = os.environ.copy()
        result.update(self.env_vars)
        return result
    
    def get_keys(self) -> List[str]:
        """
        Get all environment variable keys.
        
        Returns:
            list: List of all environment variable keys
        """
        # Check if reload is needed
        self._check_reload()
        
        # Get unique keys from both sources
        return list(set(list(os.environ.keys()) + list(self.env_vars.keys())))
    
    def set(self, key: str, value: Any) -> None:
        """
        Set environment variable.
        
        Args:
            key (str): Environment variable name
            value (Any): Environment variable value
        """
        str_value = str(value)
        self.env_vars[key] = str_value
        os.environ[key] = str_value
    
    def substitute_env_vars(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Substitute environment variables in configuration values.
        
        Args:
            config (dict): Configuration dictionary
            
        Returns:
            dict: Configuration with environment variables substituted
        """
        if not isinstance(config, dict):
            return config
        
        result = {}
        
        for key, value in config.items():
            if isinstance(value, dict):
                # Recursively process nested dictionaries
                result[key] = self.substitute_env_vars(value)
            elif isinstance(value, list):
                # Process lists
                result[key] = [
                    self.substitute_env_vars(item) if isinstance(item, dict) else
                    self._substitute_env_in_string(item) if isinstance(item, str) else
                    item
                    for item in value
                ]
            elif isinstance(value, str):
                # Substitute environment variables in strings
                result[key] = self._substitute_env_in_string(value)
            else:
                # Keep other values as is
                result[key] = value
        
        return result
    
    def _substitute_env_in_string(self, value: str) -> str:
        """
        Substitute environment variables in a string.
        
        Args:
            value (str): String value
            
        Returns:
            str: String with environment variables substituted
        """
        if not isinstance(value, str):
            return value
        
        def replace_env_var(match):
            env_var_name = match.group(1)
            default_value = match.group(2)
            
            env_var_value = self.get(env_var_name)
            
            if env_var_value is None:
                if default_value is not None:
                    return default_value
                logger.warning(f"Environment variable {env_var_name} not found")
                return match.group(0)  # Return the original placeholder
            
            return str(env_var_value)
        
        return self.ENV_PATTERN.sub(replace_env_var, value)
    
    def export_to_file(self, file_path: Union[str, Path], include_system: bool = False) -> None:
        """
        Export environment variables to a file.
        
        Args:
            file_path (str or Path): Path to the output file
            include_system (bool, optional): Whether to include system environment variables
        """
        file_path = Path(file_path)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("# Environment variables exported by EnvLoader\n")
                f.write(f"# Generated on {Path.ctime(file_path)}\n\n")
                
                # Get all environment variables
                env_vars = self.env_vars.copy()
                if include_system:
                    for key, value in os.environ.items():
                        if key not in env_vars:
                            env_vars[key] = value
                
                # Write environment variables to file
                for key, value in sorted(env_vars.items()):
                    # Quote value if it contains spaces or special characters
                    if ' ' in value or '\t' in value or '\n' in value or '"' in value or "'" in value:
                        value = f'"{value}"'
                    
                    f.write(f"{key}={value}\n")
                
            logger.info(f"Environment variables exported to {file_path}")
        except Exception as e:
            logger.error(f"Error exporting environment variables to {file_path}: {e}")


# Singleton instance
_env_loader = None

def get_env_loader(env_file: Optional[str] = None, auto_reload: bool = False) -> EnvLoader:
    """
    Get the singleton EnvLoader instance.
    
    Args:
        env_file (str, optional): Path to the .env file
        auto_reload (bool, optional): Whether to automatically reload environment variables when accessed
        
    Returns:
        EnvLoader: Singleton EnvLoader instance
    """
    global _env_loader
    
    if _env_loader is None:
        _env_loader = EnvLoader(env_file, auto_reload)
    
    return _env_loader
