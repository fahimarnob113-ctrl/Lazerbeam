from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(slots=True)
class MediaItem:
    url: str
    filename: str = ""
    local_path: Path | None = None
    mime_type: str = ""


@dataclass(slots=True)
class CapturedItem:
    source: str
    title: str
    url: str
    body: str = ""
    author: str = ""
    created_at: str = ""
    captured_at: str = field(default_factory=utc_now_iso)
    comments: list[str] = field(default_factory=list)
    media: list[MediaItem] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)


@dataclass(slots=True)
class CaptureProfile:
    name: str = "Research"
    include_media: bool = True
    include_comments: bool = True
    max_images: int = 20
    max_comments: int = 100
    save_mode: str = "auto"
    append_daily_note: bool = False


@dataclass(slots=True)
class OutputPlan:
    note_path: Path
    media_folder: Path
    tags: list[str]
    index_note_path: Path | None = None
    daily_note_path: Path | None = None
    duplicate_strategy: str = "append"
    organization_mode: str = "auto"


@dataclass(slots=True)
class CaptureHistoryEntry:
    url: str
    cleaned_url: str
    source: str
    title: str
    note_path: str
    captured_at: str
    status: str


@dataclass(slots=True)
class CaptureResult:
    item: CapturedItem
    output_plan: OutputPlan
    markdown: str
    dry_run: bool = False
