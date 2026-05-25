from __future__ import annotations

import re
from pathlib import Path

from lazerbeam.config import AppConfig
from lazerbeam.models import CapturedItem, CaptureProfile, OutputPlan


WINDOWS_FORBIDDEN = r'<>:"/\|?*'


def safe_filename(value: str, fallback: str = "Untitled", max_length: int = 96) -> str:
    cleaned = "".join("_" if char in WINDOWS_FORBIDDEN else char for char in value)
    cleaned = re.sub(r"\s+", " ", cleaned).strip().strip(".")
    if not cleaned:
        cleaned = fallback
    return cleaned[:max_length].rstrip()


def decide_output_plan(
    vault_path: Path,
    item: CapturedItem,
    profile: CaptureProfile,
    config: AppConfig,
) -> OutputPlan:
    mode = config.organization_mode or profile.save_mode or "auto"
    title = safe_filename(item.title)

    if mode == "manual":
        base = vault_path / safe_filename(config.manual_folder, "lazerbeam-inbox")
        return OutputPlan(
            note_path=base / f"{title}.md",
            media_folder=base / "_media",
            tags=sorted(set(item.tags + ["lazerbeam", item.source])),
            duplicate_strategy=config.duplicate_strategy,
            organization_mode=mode,
        )

    if mode == "inbox":
        base = vault_path / "lazerbeam-inbox"
        return OutputPlan(
            note_path=base / f"{title}.md",
            media_folder=base / "_media",
            tags=sorted(set(item.tags + ["lazerbeam", item.source])),
            duplicate_strategy=config.duplicate_strategy,
            organization_mode=mode,
        )

    if item.source == "github":
        owner = safe_filename(str(item.metadata.get("owner", "unknown-owner")))
        repo = safe_filename(str(item.metadata.get("repo", title)))
        base = vault_path / "github-notes" / owner / repo
        return OutputPlan(
            note_path=base / f"{repo} - Index.md",
            index_note_path=base / f"{repo} - Index.md",
            media_folder=base / "_images",
            tags=sorted(set(item.tags + ["lazerbeam", "github", f"repo/{owner}/{repo}"])),
            duplicate_strategy=config.duplicate_strategy,
            organization_mode=mode,
        )

    if item.source == "reddit":
        subreddit = safe_filename(str(item.metadata.get("subreddit", "reddit")))
        base = vault_path / "reddit-notes" / subreddit
        media = vault_path / "reddit-media" / subreddit
        if int(item.metadata.get("comment_count", 0) or 0) >= 500:
            base = base / "megathreads"
        return OutputPlan(
            note_path=base / f"{title}.md",
            media_folder=media,
            tags=sorted(set(item.tags + ["lazerbeam", "reddit", f"reddit/{subreddit}"])),
            duplicate_strategy=config.duplicate_strategy,
            organization_mode=mode,
        )

    base = vault_path / "web-notes"
    return OutputPlan(
        note_path=base / f"{title}.md",
        media_folder=base / "_media",
        tags=sorted(set(item.tags + ["lazerbeam", item.source])),
        duplicate_strategy=config.duplicate_strategy,
        organization_mode=mode,
    )
