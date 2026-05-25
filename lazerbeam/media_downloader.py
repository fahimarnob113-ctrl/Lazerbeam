from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

from lazerbeam.models import MediaItem
from lazerbeam.organizer import safe_filename


MEDIA_EXTENSIONS = {
    ".apng",
    ".avif",
    ".gif",
    ".jpeg",
    ".jpg",
    ".m4v",
    ".mov",
    ".mp4",
    ".png",
    ".svg",
    ".webm",
    ".webp",
}


def filename_from_url(url: str, fallback: str = "media") -> str:
    name = Path(urlparse(url).path).name
    return safe_filename(name or fallback)


def is_media_url(url: str) -> bool:
    return Path(urlparse(url).path).suffix.lower() in MEDIA_EXTENSIONS


def extract_markdown_media(markdown: str, base_url: str = "") -> list[MediaItem]:
    urls: list[str] = []
    urls.extend(re.findall(r"!\[[^\]]*\]\(([^)]+)\)", markdown))
    urls.extend(re.findall(r"<img[^>]+src=[\"']([^\"']+)[\"']", markdown, flags=re.IGNORECASE))

    media: list[MediaItem] = []
    for raw_url in urls:
        clean = raw_url.strip()
        if not clean or clean.startswith("data:"):
            continue
        resolved = _resolve_media_url(clean, base_url)
        if is_media_url(resolved):
            media.append(MediaItem(url=resolved))
    return _dedupe_media(media)


def prepare_media(media: list[MediaItem], max_items: int, filename_prefix: str = "") -> list[MediaItem]:
    prepared: list[MediaItem] = []
    used_names: set[str] = set()
    safe_prefix = safe_filename(filename_prefix).strip("_ ")
    for index, item in enumerate(media[:max_items], start=1):
        base_filename = item.filename or filename_from_url(item.url, f"media-{index}")
        if safe_prefix:
            base_filename = _prefixed_filename(base_filename, safe_prefix)
        item.filename = _unique_filename(base_filename, used_names)
        prepared.append(item)
    return prepared


def download_media(media: list[MediaItem], folder: Path, max_items: int, filename_prefix: str = "") -> list[MediaItem]:
    folder.mkdir(parents=True, exist_ok=True)
    downloaded: list[MediaItem] = []
    for item in prepare_media(media, max_items, filename_prefix):
        item.local_path = folder / item.filename
        _download_file(item.url, item.local_path)
        downloaded.append(item)
    return downloaded


def localize_markdown_media(markdown: str, media: list[MediaItem], base_url: str = "") -> str:
    filenames_by_url = {item.url: item.filename for item in media if item.filename}

    def replace_markdown(match: re.Match) -> str:
        original_url = match.group(2).strip()
        resolved = _resolve_media_url(original_url, base_url)
        filename = filenames_by_url.get(resolved)
        if not filename:
            return match.group(0)
        return f"![[{filename}]]"

    def replace_html(match: re.Match) -> str:
        original_url = match.group(1).strip()
        resolved = _resolve_media_url(original_url, base_url)
        filename = filenames_by_url.get(resolved)
        if not filename:
            return match.group(0)
        return f"![[{filename}]]"

    markdown = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", replace_markdown, markdown)
    return re.sub(r"<img[^>]+src=[\"']([^\"']+)[\"'][^>]*>", replace_html, markdown, flags=re.IGNORECASE)


def _download_file(url: str, destination: Path) -> None:
    request = Request(url, headers={"User-Agent": "Lazerbeam Prototype"})
    with urlopen(request, timeout=30) as response:
        destination.write_bytes(response.read())


def _resolve_media_url(url: str, base_url: str) -> str:
    if url.startswith("//"):
        return f"https:{url}"
    if urlparse(url).scheme:
        return url
    return urljoin(base_url, url)


def _dedupe_media(media: list[MediaItem]) -> list[MediaItem]:
    seen: set[str] = set()
    unique: list[MediaItem] = []
    for item in media:
        if item.url in seen:
            continue
        seen.add(item.url)
        unique.append(item)
    return unique


def _unique_filename(filename: str, used_names: set[str]) -> str:
    candidate = filename
    stem = Path(filename).stem or "media"
    suffix = Path(filename).suffix
    counter = 2
    while candidate.lower() in used_names:
        candidate = f"{stem}-{counter}{suffix}"
        counter += 1
    used_names.add(candidate.lower())
    return candidate


def _prefixed_filename(filename: str, prefix: str) -> str:
    path = Path(filename)
    stem = safe_filename(path.stem or "media")
    suffix = path.suffix
    if stem.lower().startswith(prefix.lower()):
        return f"{stem}{suffix}"
    return f"{prefix} - {stem}{suffix}"
