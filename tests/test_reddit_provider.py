import unittest

from lazerbeam.models import CaptureProfile
from lazerbeam.sources.reddit import RedditProvider


class FakeRedditProvider(RedditProvider):
    def __init__(self, payload):
        self.payload = payload

    def _get_json(self, url):
        return self.payload


class RedditProviderTests(unittest.TestCase):
    def test_fetch_wiki_page(self):
        provider = FakeRedditProvider(
            {
                "kind": "wikipage",
                "data": {
                    "content_md": "# Video\n\nSome wiki content.",
                    "revision_by": {"data": {"name": "wiki_editor"}},
                },
            }
        )

        item = provider.fetch(
            "https://www.reddit.com/r/FREEMEDIAHECKYEAH/wiki/video",
            CaptureProfile(),
        )

        self.assertEqual(item.title, "FREEMEDIAHECKYEAH wiki - video")
        self.assertEqual(item.author, "wiki_editor")
        self.assertEqual(item.metadata["content_type"], "wiki")
        self.assertIn("Some wiki content.", item.body)

    def test_fetch_post_rejects_unexpected_shape(self):
        provider = FakeRedditProvider({"unexpected": True})

        with self.assertRaisesRegex(ValueError, "Reddit post response"):
            provider.fetch("https://www.reddit.com/r/test/comments/abc/title", CaptureProfile())

    def test_fetch_post_extracts_image_and_video_media(self):
        provider = FakeRedditProvider(
            [
                {
                    "data": {
                        "children": [
                            {
                                "data": {
                                    "title": "Media Post",
                                    "selftext": "![extra](https://example.com/extra.jpg)",
                                    "author": "op",
                                    "subreddit": "test",
                                    "score": 1,
                                    "num_comments": 0,
                                    "url_overridden_by_dest": "https://i.redd.it/image.png",
                                    "secure_media": {
                                        "reddit_video": {
                                            "fallback_url": "https://v.redd.it/abc/DASH_720.mp4?source=fallback"
                                        }
                                    },
                                }
                            }
                        ]
                    }
                }
            ]
        )

        item = provider.fetch("https://www.reddit.com/r/test/comments/abc/title", CaptureProfile())

        self.assertEqual(
            [media.url for media in item.media],
            [
                "https://i.redd.it/image.png",
                "https://v.redd.it/abc/DASH_720.mp4?source=fallback",
                "https://example.com/extra.jpg",
            ],
        )


if __name__ == "__main__":
    unittest.main()
