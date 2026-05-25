import unittest
from pathlib import Path

from lazerbeam.config import AppConfig
from lazerbeam.models import CapturedItem, CaptureProfile
from lazerbeam.organizer import decide_output_plan, safe_filename


class OrganizerTests(unittest.TestCase):
    def test_safe_filename_replaces_windows_forbidden_chars(self):
        self.assertEqual(safe_filename('a:b/c*d?e"f'), "a_b_c_d_e_f")

    def test_github_auto_plan_uses_owner_repo(self):
        item = CapturedItem(
            source="github",
            title="owner/repo",
            url="https://github.com/owner/repo",
            metadata={"owner": "owner", "repo": "repo"},
        )
        plan = decide_output_plan(Path("Vault"), item, CaptureProfile(), AppConfig())
        self.assertEqual(plan.note_path, Path("Vault/github-notes/owner/repo/repo - Index.md"))
        self.assertIn("repo/owner/repo", plan.tags)

    def test_manual_mode_uses_manual_folder(self):
        item = CapturedItem(source="reddit", title="Post", url="https://reddit.com/x")
        config = AppConfig(organization_mode="manual", manual_folder="My Captures")
        plan = decide_output_plan(Path("Vault"), item, CaptureProfile(), config)
        self.assertEqual(plan.note_path, Path("Vault/My Captures/Post.md"))


if __name__ == "__main__":
    unittest.main()
