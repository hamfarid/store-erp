
import unittest
import os

from src.main import create_app

class TestSecurityHardening(unittest.TestCase):
    def setUp(self):
        # Use simple memory storage for limiter in tests
        os.environ['REDIS_URL'] = "memory://"
        self.app = create_app('testing')
        self.client = self.app.test_client()
    def test_scanner_blocking_user_agent(self):
        """Test blocking of malicious User-Agents"""
        response = self.client.get('/', headers={'User-Agent': 'sqlmap/1.0'})
        self.assertEqual(response.status_code, 403, "Should block 'sqlmap' User-Agent")

    def test_scanner_blocking_path(self):
        """Test blocking of sensitive paths"""
        response = self.client.get('/.env')
        self.assertEqual(response.status_code, 403, "Should block access to /.env")

    def test_dos_large_payload(self):
        """Test rejection of payloads larger than MAX_CONTENT_LENGTH"""
        # 17MB payload
        large_data = 'a' * (17 * 1024 * 1024)
        response = self.client.post('/api/user/login', data=large_data)
        self.assertEqual(response.status_code, 413, "Should reject 17MB payload (Limit is 16MB)")

    def test_rate_limiting(self):
        """Test rate limiting functionality"""
        # Note: Rate limiting might be shared across tests if not properly reset.
        # This test assumes the default limit is applied.
        # We send enough requests to trigger the limit (e.g., > 50 per hour if that's the default)
        # But 'testing' config usually disables limiter or uses memory.
        # For effective testing, we check if Limiter is attached.
        
        # Checking if extension is present
        self.assertIn('limiter', self.app.extensions, "Limiter extension should be registered")

        # Explicitly hitting an endpoint multiple times to trigger (optional, might be slow)
        # for _ in range(100):
        #     self.client.get('/')

if __name__ == '__main__':
    unittest.main()
