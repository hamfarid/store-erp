
import unittest
import os
from flask import Flask, render_template_string
from src.main import create_app

class TestSSTI(unittest.TestCase):
    def setUp(self):
        os.environ['FLASK_ENV'] = '{{ 7*7 }}' # Attempt to inject via env var
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_env_var_ssti(self):
        """Test if environment variable injection leads to SSTI"""
        # The '/' endpoint uses the 'environment' variable in the template.
        os.environ['FLASK_ENV'] = '{{ 1337*1337 }}'
        response = self.client.get('/')
        content = response.data.decode('utf-8')
        
        # If vulnerable, it would render '1787569'
        self.assertNotIn('1787569', content, "SSTI Detected! '{{ 1337*1337 }}' was executed.")
        # self.assertIn('{{ 1337*1337 }}', content, "Autoescaping should preserve the literal string.")

    def test_global_autoescape(self):
        """Verify global autoescape is enabled"""
        self.assertTrue(self.app.jinja_env.autoescape, "Global autoescape should be enabled")

if __name__ == '__main__':
    unittest.main()
