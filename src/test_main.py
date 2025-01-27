from main import extract_title
import unittest

class TestMain(unittest.TestCase):

    def test_extract_title(self):
        md = """

# Title

paragraph here
"""
        self.assertEqual(extract_title(md), "Title", "Should be Title")
    def test_extract_title_error(self):
        md = """

## Title

paragraph here
"""
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_title2(self):
        md = """
## lele
# This is the Title

paragraph here
"""
        self.assertEqual(extract_title(md), "This is the Title")

if __name__ == "__main__":
    unittest.main()

