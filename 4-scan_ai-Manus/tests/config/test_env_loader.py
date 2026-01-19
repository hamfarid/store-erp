#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test cases for the environment variables loader.
"""

import os
import sys
import unittest
import tempfile
from pathlib import Path

# Add parent directory to path to import modules
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.utils.config.env_loader import EnvLoader

class TestEnvLoader(unittest.TestCase):
    """Test cases for the EnvLoader class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary .env file for testing
        self.temp_env_file = tempfile.NamedTemporaryFile(delete=False)
        with open(self.temp_env_file.name, 'w', encoding='utf-8') as f:
            f.write("""
# Test .env file
TEST_STRING=hello_world
TEST_INT=42
TEST_FLOAT=3.14
TEST_BOOL_TRUE=true
TEST_BOOL_FALSE=false
TEST_LIST=item1,item2,item3
TEST_QUOTED="quoted value"
TEST_SINGLE_QUOTED='single quoted value'
            """)
        
        # Create EnvLoader instance with the temporary file
        self.env_loader = EnvLoader(self.temp_env_file.name)
    
    def tearDown(self):
        """Clean up after tests."""
        # Remove temporary file
        os.unlink(self.temp_env_file.name)
    
    def test_get_string(self):
        """Test getting string values."""
        self.assertEqual(self.env_loader.get('TEST_STRING'), 'hello_world')
        self.assertEqual(self.env_loader.get('NON_EXISTENT', 'default'), 'default')
    
    def test_get_int(self):
        """Test getting integer values."""
        self.assertEqual(self.env_loader.get_int('TEST_INT'), 42)
        self.assertEqual(self.env_loader.get_int('TEST_STRING', 0), 0)  # Not a valid int
        self.assertEqual(self.env_loader.get_int('NON_EXISTENT', 100), 100)
    
    def test_get_float(self):
        """Test getting float values."""
        self.assertEqual(self.env_loader.get_float('TEST_FLOAT'), 3.14)
        self.assertEqual(self.env_loader.get_float('TEST_STRING', 0.0), 0.0)  # Not a valid float
        self.assertEqual(self.env_loader.get_float('NON_EXISTENT', 2.71), 2.71)
    
    def test_get_bool(self):
        """Test getting boolean values."""
        self.assertTrue(self.env_loader.get_bool('TEST_BOOL_TRUE'))
        self.assertFalse(self.env_loader.get_bool('TEST_BOOL_FALSE'))
        self.assertTrue(self.env_loader.get_bool('NON_EXISTENT', True))
    
    def test_get_list(self):
        """Test getting list values."""
        self.assertEqual(self.env_loader.get_list('TEST_LIST'), ['item1', 'item2', 'item3'])
        self.assertEqual(self.env_loader.get_list('NON_EXISTENT', ['default']), ['default'])
    
    def test_quoted_values(self):
        """Test handling of quoted values."""
        self.assertEqual(self.env_loader.get('TEST_QUOTED'), 'quoted value')
        self.assertEqual(self.env_loader.get('TEST_SINGLE_QUOTED'), 'single quoted value')
    
    def test_substitute_env_vars(self):
        """Test substituting environment variables in configuration."""
        config = {
            'database': {
                'host': '${TEST_STRING}',
                'port': '${TEST_INT}',
                'settings': {
                    'timeout': '${TEST_FLOAT}'
                }
            },
            'features': ['${TEST_BOOL_TRUE}', '${TEST_BOOL_FALSE}'],
            'items': '${TEST_LIST}'
        }
        
        expected = {
            'database': {
                'host': 'hello_world',
                'port': '42',
                'settings': {
                    'timeout': '3.14'
                }
            },
            'features': ['true', 'false'],
            'items': 'item1,item2,item3'
        }
        
        result = self.env_loader.substitute_env_vars(config)
        self.assertEqual(result, expected)
    
    def test_substitute_env_in_string(self):
        """Test substituting environment variables in strings."""
        self.assertEqual(
            self.env_loader._substitute_env_in_string('Value: ${TEST_STRING}'),
            'Value: hello_world'
        )
        self.assertEqual(
            self.env_loader._substitute_env_in_string('${TEST_INT} and ${TEST_FLOAT}'),
            '42 and 3.14'
        )
        self.assertEqual(
            self.env_loader._substitute_env_in_string('${NON_EXISTENT}'),
            '${NON_EXISTENT}'  # Should keep placeholder for non-existent variables
        )


if __name__ == '__main__':
    unittest.main()
