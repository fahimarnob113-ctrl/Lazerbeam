from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlretrieve

from lazerbeam.models import MediaItem
from lazerbeam.organizer import safe_filename


def filename_from_url(url: str, fallback: str = "media") -> str:
    name = Path(urlparse(url).path).name
    return safe_filename(name or fallback)


def download_media(media: list[MediaItem], folder: Path, max_items: int) -> list[MediaItem]:
    folder.mkdir(parents=True, exist_ok=True)
    downloaded: list[MediaItem] = []
    for item in media[:max_items]:
        item.filename = item.filename or filename_from_url(item.url)
        item.local_path = folder / item.filename
        urlretrieve(item.url, item.local_path)
        downloaded.append(item)
    return downloaded
