from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from lazerbeam.models import CaptureHistoryEntry


class CaptureHistory:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> list[CaptureHistoryEntry]:
        if not self.path.exists():
            return []
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return [CaptureHistoryEntry(**entry) for entry in data]

    def add(self, entry: CaptureHistoryEntry) -> None:
        entries = self.load()
        entries.append(entry)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps([asdict(item) for item in entries], indent=2),
            encoding="utf-8",
        )

    def find_duplicate(self, cleaned_url: str) -> CaptureHistoryEntry | None:
        for entry in reversed(self.load()):
            if entry.cleaned_url == cleaned_url and entry.status == "completed":
                return entry
        return None
