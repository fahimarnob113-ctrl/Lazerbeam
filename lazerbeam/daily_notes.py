from __future__ import annotations

from datetime import date
from pathlib import Path


def append_daily_note(vault_path: Path, note_title: str, source: str, folder: str = "Daily Notes") -> Path:
    daily_path = vault_path / folder / f"{date.today().isoformat()}.md"
    daily_path.parent.mkdir(parents=True, exist_ok=True)
    with daily_path.open("a", encoding="utf-8") as handle:
        handle.write(f"- Captured [[{note_title}]] from {source}\n")
    return daily_path
