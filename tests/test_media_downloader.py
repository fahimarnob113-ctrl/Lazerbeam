import unittest

from lazerbeam.media_downloader import extract_markdown_media, filename_from_url, prepare_media
from lazerbeam.models import MediaItem


class MediaDownloaderTests(unittest.TestCase):
    def test_extract_markdown_media_resolves_relative_urls(self):
        media = extract_markdown_media(
            "![Logo](assets/logo.png)\n<img src=\"https://example.com/banner.webp\">",
            "https://raw.githubusercontent.com/owner/repo/main/README.md",
        )

        self.assertEqual(media[0].url, "https://raw.githubusercontent.com/owner/repo/main/assets/logo.png")
        self.assertEqual(media[1].url, "https://example.com/banner.webp")

    def test_prepare_media_assigns_unique_prefixed_filenames(self):
        media = prepare_media(
            [
                MediaItem(url="https://example.com/image.png"),
                MediaItem(url="https://example.com/other/image.png"),
            ],
            max_items=10,
            filename_prefix="My Note",
        )

        self.assertEqual(media[0].filename, "My Note - image.png")
        self.assertEqual(media[1].filename, "My Note - image-2.png")

    def test_filename_from_url_ignores_query(self):
        self.assertEqual(filename_from_url("https://example.com/video.mp4?source=fallback"), "video.mp4")


if __name__ == "__main__":
    unittest.main()
