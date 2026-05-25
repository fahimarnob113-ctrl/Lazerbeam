import unittest

from lazerbeam.media_downloader import extract_markdown_media, filename_from_url, localize_markdown_media, prepare_media
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

    def test_extract_markdown_media_includes_svg(self):
        media = extract_markdown_media("![Repo](repo.svg)", "https://raw.githubusercontent.com/owner/repo/main/README.md")

        self.assertEqual(media[0].url, "https://raw.githubusercontent.com/owner/repo/main/repo.svg")

    def test_extract_reference_style_markdown_media(self):
        markdown = "![repo][repo.svg]\n[repo.svg]: icons/repo.svg"
        media = extract_markdown_media(markdown, "https://raw.githubusercontent.com/owner/repo/main/README.md")

        self.assertEqual(media[0].url, "https://raw.githubusercontent.com/owner/repo/main/icons/repo.svg")

    def test_localize_markdown_media_rewrites_markdown_and_html_images(self):
        markdown = "![Repo](repo.svg)\n<img src=\"open.svg\">"
        media = [
            MediaItem(
                url="https://raw.githubusercontent.com/owner/repo/main/repo.svg",
                filename="free-lunch - Index - repo.svg",
            ),
            MediaItem(
                url="https://raw.githubusercontent.com/owner/repo/main/open.svg",
                filename="free-lunch - Index - open.svg",
            ),
        ]

        localized = localize_markdown_media(markdown, media, "https://raw.githubusercontent.com/owner/repo/main/README.md")

        self.assertIn("![[free-lunch - Index - repo.svg]]", localized)
        self.assertIn("![[free-lunch - Index - open.svg]]", localized)

    def test_localize_reference_style_markdown_media(self):
        markdown = "[![repo][repo.svg]](https://github.com/example/repo) ![open][open.svg]\n[repo.svg]: icons/repo.svg\n[open.svg]: icons/open.svg"
        media = [
            MediaItem(
                url="https://raw.githubusercontent.com/owner/repo/main/icons/repo.svg",
                filename="free-lunch - Index - repo.svg",
            ),
            MediaItem(
                url="https://raw.githubusercontent.com/owner/repo/main/icons/open.svg",
                filename="free-lunch - Index - open.svg",
            ),
        ]

        localized = localize_markdown_media(markdown, media, "https://raw.githubusercontent.com/owner/repo/main/README.md")

        self.assertIn("[![[free-lunch - Index - repo.svg]]](https://github.com/example/repo)", localized)
        self.assertIn("![[free-lunch - Index - open.svg]]", localized)
        self.assertNotIn("![repo][repo.svg]", localized)


if __name__ == "__main__":
    unittest.main()
