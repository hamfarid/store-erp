#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration loader for the Agricultural AI System.
Handles loading and merging configuration from different sources.
"""

import os
import json
import yaml
import logging
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, Union, List

from .env_loader import get_env_loader

logger = logging.getLogger('config_loader')

class ConfigLoader:
    """
    Configuration loader for the Agricultural AI System.
    
    This class handles:
    - Loading configuration from YAML/JSON files
    - Merging configurations from different sources
    - Substituting environment variables in configuration values
    - Validating configuration against schemas
    """
    
    def __init__(self, config_dir: Optional[str] = None, auto_reload: bool = False):
        """
        Initialize the configuration loader.
        
        Args:
            config_dir (str, optional): Path to the configuration directory.
                                       If None, uses the default config directory.
            auto_reload (bool, optional): Whether to automatically reload configuration when accessed.
        """
        self.env_loader = get_env_loader(auto_reload=auto_reload)
        self.auto_reload = auto_reload
        self.last_load_times = {}
        
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            # Default config directory is in project root
            self.config_dir = Path(__file__).parent.parent.parent.parent / 'config'
        
        logger.info(f"Configuration directory: {self.config_dir}")
    
    def load_config(self, config_file: Optional[str] = None, 
                   env: Optional[str] = None,
                   override_vars: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Load configuration from file.
        
        Args:
            config_file (str, optional): Path to the configuration file.
                                        If None, uses default.yaml in the config directory.
            env (str, optional): Environment name (e.g., 'dev', 'prod').
                                If provided, also loads environment-specific config.
            override_vars (dict, optional): Variables to override in the configuration.
                                
        Returns:
            dict: Merged configuration dictionary with environment variables substituted
        """
        # Load default configuration
        if not config_file:
            config_file = self.config_dir / 'default.yaml'
        else:
            config_file = Path(config_file)
            if not config_file.is_absolute():
                config_file = self.config_dir / config_file
        
        if not config_file.exists():
            logger.warning(f"Configuration file not found: {config_file}")
            config = {}
        else:
            logger.info(f"Loading configuration from {config_file}")
            config = self._load_file(config_file)
        
        # Load environment-specific configuration if provided
        if env:
            env_config_file = self.config_dir / f"{env}.yaml"
            if env_config_file.exists():
                logger.info(f"Loading environment-specific configuration from {env_config_file}")
                env_config = self._load_file(env_config_file)
                config = self._deep_merge(config, env_config)
            else:
                logger.warning(f"Environment-specific configuration file not found: {env_config_file}")
        
        # Override with variables if provided
        if override_vars:
            logger.info(f"Overriding configuration with {len(override_vars)} variables")
            config = self._deep_merge(config, override_vars)
        
        # Substitute environment variables in configuration values
        config = self.env_loader.substitute_env_vars(config)
        
        return config
    
    def load_configs(self, config_files: List[str], 
                    env: Optional[str] = None,
                    override_vars: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Load and merge multiple configuration files.
        
        Args:
            config_files (list): List of paths to configuration files.
            env (str, optional): Environment name (e.g., 'dev', 'prod').
                                If provided, also loads environment-specific config for each file.
            override_vars (dict, optional): Variables to override in the configuration.
                                
        Returns:
            dict: Merged configuration dictionary with environment variables substituted
        """
        if not config_files:
            return {}
        
        # Load first configuration file
        config = self.load_config(config_files[0], env, None)
        
        # Merge with remaining configuration files
        for config_file in config_files[1:]:
            next_config = self.load_config(config_file, env, None)
            config = self._deep_merge(config, next_config)
        
        # Override with variables if provided
        if override_vars:
            logger.info(f"Overriding configuration with {len(override_vars)} variables")
            config = self._deep_merge(config, override_vars)
        
        # Substitute environment variables in configuration values
        config = self.env_loader.substitute_env_vars(config)
        
        return config
    
    def _load_file(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Load configuration from file.
        
        Args:
            file_path (str or Path): Path to the configuration file
            
        Returns:
            dict: Configuration dictionary
        """
        file_path = Path(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if file_path.suffix.lower() in ('.yaml', '.yml'):
                    return yaml.safe_load(f) or {}
                elif file_path.suffix.lower() == '.json':
                    return json.load(f)
                else:
                    logger.warning(f"Unsupported configuration file format: {file_path}")
                    return {}
                    
            # Update last load time
            self.last_load_times[str(file_path)] = os.path.getmtime(file_path)
        except Exception as e:
            logger.error(f"Error loading configuration file {file_path}: {e}")
            return {}
    
    def _check_reload(self, file_path: Union[str, Path]) -> bool:
        """
        Check if configuration file has been modified and needs reload.
        
        Args:
            file_path (str or Path): Path to the configuration file
            
        Returns:
            bool: True if file has been modified, False otherwise
        """
        if not self.auto_reload:
            return False
        
        file_path = str(file_path)
        if not os.path.exists(file_path):
            return False
        
        current_mtime = os.path.getmtime(file_path)
        last_load_time = self.last_load_times.get(file_path, 0)
        
        return current_mtime > last_load_time
    
    def _deep_merge(self, dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deep merge two dictionaries.
        
        Args:
            dict1 (dict): First dictionary
            dict2 (dict): Second dictionary
            
        Returns:
            dict: Merged dictionary
        """
        result = dict1.copy()
        
        for key, value in dict2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def save_config(self, config: Dict[str, Any], file_path: Union[str, Path], 
                   format: str = 'yaml') -> bool:
        """
        Save configuration to file.
        
        Args:
            config (dict): Configuration dictionary
            file_path (str or Path): Path to the output file
            format (str, optional): Output format ('yaml' or 'json')
            
        Returns:
            bool: True if successful, False otherwise
        """
        file_path = Path(file_path)
        
        try:
            # Create parent directories if they don't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write to a temporary file first to avoid corruption if the process is interrupted
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=file_path.suffix) as temp_file:
                if format.lower() == 'yaml':
                    yaml.dump(config, temp_file, default_flow_style=False, sort_keys=False)
                elif format.lower() == 'json':
                    json.dump(config, temp_file, indent=2)
                else:
                    logger.error(f"Unsupported output format: {format}")
                    return False
            
            # Rename the temporary file to the target file
            os.replace(temp_file.name, file_path)
            
            logger.info(f"Configuration saved to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving configuration to {file_path}: {e}")
            return False
    
    def get_available_configs(self) -> List[str]:
        """
        Get list of available configuration files.
        
        Returns:
            list: List of configuration file names (without extension)
        """
        if not self.config_dir.exists():
            return []
        
        configs = []
        for file_path in self.config_dir.glob('*.yaml'):
            configs.append(file_path.stem)
        
        for file_path in self.config_dir.glob('*.yml'):
            configs.append(file_path.stem)
        
        for file_path in self.config_dir.glob('*.json'):
            configs.append(file_path.stem)
        
        return sorted(configs)
    
    def validate_config(self, config: Dict[str, Any], schema: Dict[str, Any]) -> bool:
        """
        Validate configuration against a schema.
        
        Args:
            config (dict): Configuration dictionary
            schema (dict): Schema dictionary
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            import jsonschema
            jsonschema.validate(config, schema)
            return True
        except ImportError:
            logger.warning("jsonschema package not installed, skipping validation")
            return True
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            return False


# Singleton instance
_config_loader = None

def get_config_loader(config_dir: Optional[str] = None, auto_reload: bool = False) -> ConfigLoader:
    """
    Get the singleton ConfigLoader instance.
    
    Args:
        config_dir (str, optional): Path to the configuration directory
        auto_reload (bool, optional): Whether to automatically reload configuration when accessed
        
    Returns:
        ConfigLoader: Singleton ConfigLoader instance
    """
    global _config_loader
    
    if _config_loader is None:
        _config_loader = ConfigLoader(config_dir, auto_reload)
    
    return _config_loader


def load_config(config_file: Optional[str] = None, 
               env: Optional[str] = None,
               config_dir: Optional[str] = None,
               override_vars: Optional[Dict[str, Any]] = None,
               auto_reload: bool = False) -> Dict[str, Any]:
    """
    Load configuration from file.
    
    This is a convenience function that uses the singleton ConfigLoader.
    
    Args:
        config_file (str, optional): Path to the configuration file
        env (str, optional): Environment name (e.g., 'dev', 'prod')
        config_dir (str, optional): Path to the configuration directory
        override_vars (dict, optional): Variables to override in the configuration
        auto_reload (bool, optional): Whether to automatically reload configuration when accessed
        
    Returns:
        dict: Configuration dictionary
    """
    config_loader = get_config_loader(config_dir, auto_reload)
    return config_loader.load_config(config_file, env, override_vars)
