import unittest

from lazerbeam.url_utils import clean_url, detect_source, parse_urls


class UrlUtilsTests(unittest.TestCase):
    def test_clean_url_removes_query_fragment_and_trailing_slash(self):
        self.assertEqual(
            clean_url("https://www.reddit.com/r/Obsidian/comments/abc/title/?context=3#x"),
            "https://www.reddit.com/r/Obsidian/comments/abc/title",
        )

    def test_detect_source(self):
        self.assertEqual(detect_source("https://github.com/openai/openai-python"), "github")
        self.assertEqual(detect_source("https://www.reddit.com/r/test/comments/1/a"), "reddit")
        self.assertEqual(detect_source("https://example.com"), "unknown")

    def test_parse_urls_ignores_blank_lines(self):
        self.assertEqual(parse_urls("https://a.com\n\n https://b.com "), ["https://a.com", "https://b.com"])


if __name__ == "__main__":
    unittest.main()
