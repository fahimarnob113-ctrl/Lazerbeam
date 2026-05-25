import tempfile
import unittest
from pathlib import Path

from lazerbeam.models import OutputPlan
from lazerbeam.obsidian_writer import write_note


class ObsidianWriterTests(unittest.TestCase):
    def test_write_note_appends_existing_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            note = Path(temp_dir) / "Note.md"
            plan = OutputPlan(note_path=note, media_folder=Path(temp_dir) / "_media", tags=[])
            write_note("first\n", plan)
            write_note("second\n", plan)
            self.assertIn("first", note.read_text(encoding="utf-8"))
            self.assertIn("second", note.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
