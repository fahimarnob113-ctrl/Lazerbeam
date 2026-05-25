import tempfile
import unittest
from pathlib import Path

from lazerbeam.history import CaptureHistory
from lazerbeam.models import CaptureHistoryEntry


class HistoryTests(unittest.TestCase):
    def test_find_duplicate(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            history = CaptureHistory(Path(temp_dir) / "history.json")
            history.add(
                CaptureHistoryEntry(
                    url="https://example.com?a=1",
                    cleaned_url="https://example.com",
                    source="web",
                    title="Example",
                    note_path="Example.md",
                    captured_at="now",
                    status="completed",
                )
            )
            self.assertIsNotNone(history.find_duplicate("https://example.com"))


if __name__ == "__main__":
    unittest.main()
