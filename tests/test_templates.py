import unittest
from pathlib import Path

from lazerbeam.models import CapturedItem, MediaItem, OutputPlan
from lazerbeam.templates import render_markdown


class TemplateTests(unittest.TestCase):
    def test_render_markdown_includes_frontmatter_and_obsidian_media(self):
        item = CapturedItem(source="github", title="Repo", url="https://github.com/a/b", body="Body")
        plan = OutputPlan(note_path=Path("Repo.md"), media_folder=Path("_images"), tags=["lazerbeam", "github"])
        markdown = render_markdown(item, plan)
        self.assertIn("source: github", markdown)
        self.assertIn("# Repo", markdown)
        self.assertIn("Body", markdown)

    def test_media_section_appears_near_top_before_body_and_source(self):
        item = CapturedItem(
            source="reddit",
            title="Post",
            url="https://reddit.com/r/test/comments/abc/post",
            body="Body",
            media=[MediaItem(url="https://example.com/image.png", filename="Post - image.png")],
        )
        plan = OutputPlan(note_path=Path("Post.md"), media_folder=Path("_media"), tags=["lazerbeam", "reddit"])
        markdown = render_markdown(item, plan)

        self.assertLess(markdown.index("## Media"), markdown.index("Body"))
        self.assertLess(markdown.index("## Media"), markdown.index("## Source"))
        self.assertIn("![[Post - image.png]]", markdown)

    def test_media_gallery_is_skipped_when_media_is_embedded_in_body(self):
        item = CapturedItem(
            source="github",
            title="Repo",
            url="https://github.com/a/b",
            body="Body ![[Repo - logo.svg]]",
            media=[MediaItem(url="https://example.com/logo.svg", filename="Repo - logo.svg")],
            metadata={"media_embedded_in_body": True},
        )
        plan = OutputPlan(note_path=Path("Repo.md"), media_folder=Path("_images"), tags=["lazerbeam", "github"])
        markdown = render_markdown(item, plan)

        self.assertNotIn("## Media", markdown)
        self.assertIn("Body ![[Repo - logo.svg]]", markdown)


if __name__ == "__main__":
    unittest.main()
