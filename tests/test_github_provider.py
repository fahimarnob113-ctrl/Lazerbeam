import unittest

from lazerbeam.models import CaptureProfile
from lazerbeam.sources.github import GitHubProvider


class FakeGitHubProvider(GitHubProvider):
    def __init__(self, payload):
        self.payload = payload

    def _get_json(self, url):
        return self.payload


class GitHubProviderTests(unittest.TestCase):
    def test_fetch_gist(self):
        provider = FakeGitHubProvider(
            {
                "description": "Useful gist",
                "files": {
                    "notes.md": {
                        "content": "# Notes\n\n![Logo](logo.png)",
                        "raw_url": "https://gist.githubusercontent.com/ongkiii/id/raw/hash/notes.md",
                    }
                },
            }
        )

        item = provider.fetch("https://gist.github.com/ongkiii/b40620d8d4a98ab17642858dce4cb2ec", CaptureProfile())

        self.assertEqual(item.title, "ongkiii/Useful gist")
        self.assertEqual(item.metadata["content_type"], "gist")
        self.assertEqual(item.metadata["gist_id"], "b40620d8d4a98ab17642858dce4cb2ec")
        self.assertIn("## notes.md", item.body)
        self.assertEqual(
            item.media[0].url,
            "https://gist.githubusercontent.com/ongkiii/id/raw/hash/logo.png",
        )


if __name__ == "__main__":
    unittest.main()
