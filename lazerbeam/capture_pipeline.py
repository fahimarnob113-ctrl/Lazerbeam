from __future__ import annotations

from pathlib import Path

from lazerbeam.config import AppConfig
from lazerbeam.history import CaptureHistory
from lazerbeam.media_downloader import download_media, prepare_media
from lazerbeam.models import CaptureHistoryEntry, CaptureProfile, CaptureResult
from lazerbeam.obsidian_writer import write_note
from lazerbeam.organizer import decide_output_plan
from lazerbeam.profiles import BUILT_IN_PROFILES
from lazerbeam.sources.github import GitHubProvider
from lazerbeam.sources.reddit import RedditProvider
from lazerbeam.templates import render_markdown
from lazerbeam.url_utils import clean_url, detect_source


PROVIDERS = {
    "github": GitHubProvider(),
    "reddit": RedditProvider(),
}


def capture_url(
    url: str,
    vault_path: Path,
    config: AppConfig,
    profile: CaptureProfile | None = None,
    dry_run: bool = False,
) -> CaptureResult:
    profile = profile or BUILT_IN_PROFILES["Research"]
    cleaned_url = clean_url(url)
    source = detect_source(cleaned_url)
    if source not in PROVIDERS:
        raise ValueError(f"Unsupported URL source: {cleaned_url}")

    history = CaptureHistory(vault_path / ".lazerbeam" / "history.json")
    duplicate = history.find_duplicate(cleaned_url)
    if duplicate and config.duplicate_strategy == "skip":
        raise ValueError(f"Already captured: {cleaned_url}")

    item = PROVIDERS[source].fetch(cleaned_url, profile)
    plan = decide_output_plan(vault_path, item, profile, config)
    if profile.include_media and item.media:
        if dry_run:
            item.media = prepare_media(item.media, profile.max_images)
        else:
            item.media = download_media(item.media, plan.media_folder, profile.max_images)
    markdown = render_markdown(item, plan)

    if not dry_run:
        note_path = write_note(markdown, plan)
        history.add(
            CaptureHistoryEntry(
                url=url,
                cleaned_url=cleaned_url,
                source=source,
                title=item.title,
                note_path=str(note_path),
                captured_at=item.captured_at,
                status="completed",
            )
        )

    return CaptureResult(item=item, output_plan=plan, markdown=markdown, dry_run=dry_run)
