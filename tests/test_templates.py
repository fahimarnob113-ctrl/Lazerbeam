import unittest
from pathlib import Path

from lazerbeam.models import CapturedItem, OutputPlan
from lazerbeam.templates import render_markdown


class TemplateTests(unittest.TestCase):
    def test_render_markdown_includes_frontmatter_and_obsidian_media(self):
        item = CapturedItem(source="github", title="Repo", url="https://github.com/a/b", body="Body")
        plan = OutputPlan(note_path=Path("Repo.md"), media_folder=Path("_images"), tags=["lazerbeam", "github"])
        markdown = render_markdown(item, plan)
        self.assertIn("source: github", markdown)
        self.assertIn("# Repo", markdown)
        self.assertIn("Body", markdown)


if __name__ == "__main__":
    unittest.main()
