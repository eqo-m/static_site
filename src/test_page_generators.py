import unittest
from page_generators import extract_title


class TestExtractTitle(unittest.TestCase):
    
    def test_extract_title_basic(self):
        markdown = "# Hello World\nSome content"
        result = extract_title(markdown)
        self.assertEqual(result, "Hello World")
    
    def test_extract_title_with_spaces(self):
        markdown = "#   Title with spaces   \nContent"
        result = extract_title(markdown)
        self.assertEqual(result, "Title with spaces")
    
    def test_extract_title_multiline(self):
        markdown = "Some text\n# Main Title\nMore content\n## Sub title"
        result = extract_title(markdown)
        self.assertEqual(result, "Main Title")
    
    def test_extract_title_no_title(self):
        markdown = "Just some content\nNo title here"
        with self.assertRaises(ValueError):
            extract_title(markdown)
    
    def test_extract_title_empty_string(self):
        markdown = ""
        with self.assertRaises(ValueError):
            extract_title(markdown)


if __name__ == '__main__':
    unittest.main()