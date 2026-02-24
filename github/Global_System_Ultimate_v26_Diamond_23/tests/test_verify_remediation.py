import unittest
import os
import sys

# Add root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from verify_gap_remediation import verify

class TestVerifyRemediation(unittest.TestCase):
    def test_verify(self):
        # Basic smoke test
        try:
            verify()
        except Exception as e:
            self.fail(f"verify raised {e} unexpectedly!")

if __name__ == '__main__':
    unittest.main()
