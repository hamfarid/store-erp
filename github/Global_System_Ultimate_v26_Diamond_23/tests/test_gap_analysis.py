import unittest
import os
import sys

# Add root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gap_analysis_check import check_files

class TestGapAnalysis(unittest.TestCase):
    def test_check_files(self):
        # This is a basic test to ensure the function runs without error
        # In a real scenario, we would mock the file system
        try:
            check_files()
        except Exception as e:
            self.fail(f"check_files raised {e} unexpectedly!")

if __name__ == '__main__':
    unittest.main()
