#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test cases for the configuration loader.
"""

import os
import sys
import unittest
import tempfile
import yaml
from pathlib import Path

# Add parent directory to path to import modules
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.utils.config.config_loader import ConfigLoader
from src.utils.config.env_loader import EnvLoader

class TestConfigLoader(unittest.TestCase):
    """Test cases for the ConfigLoader class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for config files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_dir = Path(self.temp_dir.name)
        
        # Create a temporary .env file
        self.temp_env_file = tempfile.NamedTemporaryFile(delete=False)
        with open(self.temp_env_file.name, 'w', encoding='utf-8') as f:
            f.write("""
# Test .env file
DB_HOST=test-db-host
DB_PORT=5432
DB_USER=test-user
DB_PASSWORD=test-password
API_KEY=test-api-key
DEBUG_MODE=true
MAX_THREADS=8
            """)
        
        # Set environment variable to point to our test .env file
        os.environ['ENV_FILE'] = self.temp_env_file.name
        
        # Create default config file
        with open(self.config_dir / 'default.yaml', 'w', encoding='utf-8') as f:
            f.write("""
# Default configuration
database:
  host: "${DB_HOST}"
  port: ${DB_PORT}
  user: "${DB_USER}"
  password: "${DB_PASSWORD}"

api:
  key: "${API_KEY}"
  timeout: 30

system:
  debug: ${DEBUG_MODE}
  max_threads: ${MAX_THREADS}
  temp_dir: "temp"
            """)
        
        # Create environment-specific config file
        with open(self.config_dir / 'prod.yaml', 'w', encoding='utf-8') as f:
            f.write("""
# Production configuration
database:
  host: "prod-db-host"
  
system:
  debug: false
  log_level: "ERROR"
            """)
        
        # Create ConfigLoader instance with the temporary directory
        self.config_loader = ConfigLoader(self.config_dir)
    
    def tearDown(self):
        """Clean up after tests."""
        # Remove temporary files and directory
        os.unlink(self.temp_env_file.name)
        self.temp_dir.cleanup()
        
        # Remove environment variable
        if 'ENV_FILE' in os.environ:
            del os.environ['ENV_FILE']
    
    def test_load_default_config(self):
        """Test loading default configuration."""
        config = self.config_loader.load_config()
        
        # Check that environment variables were substituted
        self.assertEqual(config['database']['host'], 'test-db-host')
        self.assertEqual(config['database']['port'], '5432')
        self.assertEqual(config['database']['user'], 'test-user')
        self.assertEqual(config['database']['password'], 'test-password')
        self.assertEqual(config['api']['key'], 'test-api-key')
        self.assertEqual(config['system']['debug'], 'true')
        self.assertEqual(config['system']['max_threads'], '8')
        self.assertEqual(config['system']['temp_dir'], 'temp')
    
    def test_load_env_specific_config(self):
        """Test loading environment-specific configuration."""
        config = self.config_loader.load_config(env='prod')
        
        # Check that environment-specific values override defaults
        self.assertEqual(config['database']['host'], 'prod-db-host')
        self.assertEqual(config['system']['debug'], False)  # Boolean value, not string
        self.assertEqual(config['system']['log_level'], 'ERROR')
        
        # Check that non-overridden values are preserved
        self.assertEqual(config['database']['port'], '5432')
        self.assertEqual(config['database']['user'], 'test-user')
        self.assertEqual(config['api']['key'], 'test-api-key')
    
    def test_load_specific_config_file(self):
        """Test loading a specific configuration file."""
        # Create a specific config file
        with open(self.config_dir / 'specific.yaml', 'w', encoding='utf-8') as f:
            f.write("""
# Specific configuration
database:
  host: "specific-db-host"
  user: "${DB_USER}"
  
api:
  timeout: 60
            """)
        
        config = self.config_loader.load_config(config_file='specific.yaml')
        
        # Check that specific values are used
        self.assertEqual(config['database']['host'], 'specific-db-host')
        self.assertEqual(config['api']['timeout'], 60)
        
        # Check that environment variables are still substituted
        self.assertEqual(config['database']['user'], 'test-user')
    
    def test_deep_merge(self):
        """Test deep merging of configurations."""
        dict1 = {
            'a': 1,
            'b': {
                'c': 2,
                'd': 3
            },
            'e': [1, 2, 3]
        }
        
        dict2 = {
            'b': {
                'c': 4,
                'f': 5
            },
            'g': 6
        }
        
        expected = {
            'a': 1,
            'b': {
                'c': 4,
                'd': 3,
                'f': 5
            },
            'e': [1, 2, 3],
            'g': 6
        }
        
        result = self.config_loader._deep_merge(dict1, dict2)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
