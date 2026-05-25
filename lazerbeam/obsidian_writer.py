from __future__ import annotations

from pathlib import Path

from lazerbeam.models import OutputPlan


def write_note(markdown: str, plan: OutputPlan) -> Path:
    plan.note_path.parent.mkdir(parents=True, exist_ok=True)
    plan.media_folder.mkdir(parents=True, exist_ok=True)

    if plan.note_path.exists() and plan.duplicate_strategy == "append":
        with plan.note_path.open("a", encoding="utf-8") as handle:
            handle.write("\n\n---\n\n")
            handle.write(markdown)
    else:
        plan.note_path.write_text(markdown, encoding="utf-8")

    return plan.note_path
