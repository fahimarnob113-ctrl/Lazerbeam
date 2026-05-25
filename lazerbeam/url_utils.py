from __future__ import annotations

from urllib.parse import urlparse, urlunparse


def clean_url(url: str) -> str:
    parsed = urlparse(url.strip())
    path = parsed.path.rstrip("/")
    return urlunparse((parsed.scheme, parsed.netloc.lower(), path, "", "", ""))


def parse_urls(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def detect_source(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if host.endswith("github.com"):
        return "github"
    if host.endswith("reddit.com") or host.endswith("redd.it"):
        return "reddit"
    return "unknown"


def is_supported_url(url: str) -> bool:
    return detect_source(url) in {"github", "reddit"}
