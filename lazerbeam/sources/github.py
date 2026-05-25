from __future__ import annotations

import json
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from lazerbeam.media_downloader import extract_markdown_media
from lazerbeam.models import CapturedItem, CaptureProfile
from lazerbeam.sources.base import SourceProvider


class GitHubProvider(SourceProvider):
    source_name = "github"

    def can_handle(self, url: str) -> bool:
        return urlparse(url).netloc.lower().endswith("github.com")

    def fetch(self, url: str, profile: CaptureProfile) -> CapturedItem:
        owner, repo = self._parse_repo(url)
        repo_api = f"https://api.github.com/repos/{owner}/{repo}"
        readme_api = f"https://api.github.com/repos/{owner}/{repo}/readme"
        metadata = self._get_json(repo_api)
        readme = self._get_json(readme_api)
        readme_url = readme.get("download_url", "")
        readme_text = self._get_text(readme_url) if readme_url else ""
        return CapturedItem(
            source="github",
            title=f"{owner}/{repo}",
            url=url,
            body=readme_text,
            author=owner,
            media=extract_markdown_media(readme_text, readme_url) if profile.include_media else [],
            metadata={
                "owner": owner,
                "repo": repo,
                "media_base_url": readme_url,
                "stars": metadata.get("stargazers_count", 0),
                "language": metadata.get("language", ""),
                "license": (metadata.get("license") or {}).get("spdx_id", ""),
            },
            tags=["github"],
        )

    def _parse_repo(self, url: str) -> tuple[str, str]:
        parts = [part for part in urlparse(url).path.split("/") if part]
        if len(parts) < 2:
            raise ValueError("GitHub URL must include owner and repository.")
        return parts[0], parts[1]

    def _get_json(self, url: str) -> dict:
        request = Request(url, headers={"User-Agent": "Lazerbeam Prototype"})
        with urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))

    def _get_text(self, url: str) -> str:
        request = Request(url, headers={"User-Agent": "Lazerbeam Prototype"})
        with urlopen(request, timeout=20) as response:
            return response.read().decode("utf-8", errors="replace")
