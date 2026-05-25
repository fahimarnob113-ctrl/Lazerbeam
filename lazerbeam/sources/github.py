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
        if self._is_gist_url(url):
            return self._fetch_gist(url, profile)

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

    def _is_gist_url(self, url: str) -> bool:
        return urlparse(url).netloc.lower() == "gist.github.com"

    def _fetch_gist(self, url: str, profile: CaptureProfile) -> CapturedItem:
        owner, gist_id = self._parse_gist(url)
        gist_api = f"https://api.github.com/gists/{gist_id}"
        gist = self._get_json(gist_api)
        files = gist.get("files", {})
        body_parts: list[str] = []
        media = []

        for filename, file_data in files.items():
            content = file_data.get("content", "")
            raw_url = file_data.get("raw_url", "")
            body_parts.append(f"## {filename}\n\n{content}".strip())
            if profile.include_media:
                media.extend(extract_markdown_media(content, raw_url))

        title = gist.get("description") or self._first_filename(files) or gist_id
        return CapturedItem(
            source="github",
            title=f"{owner}/{title}",
            url=url,
            body="\n\n".join(body_parts),
            author=owner,
            media=media,
            metadata={
                "owner": owner,
                "repo": f"gist-{gist_id[:8]}",
                "gist_id": gist_id,
                "content_type": "gist",
                "media_base_url": "",
            },
            tags=["github", "gist"],
        )

    def _parse_repo(self, url: str) -> tuple[str, str]:
        parts = [part for part in urlparse(url).path.split("/") if part]
        if len(parts) < 2:
            raise ValueError("GitHub URL must include owner and repository.")
        return parts[0], parts[1]

    def _parse_gist(self, url: str) -> tuple[str, str]:
        parts = [part for part in urlparse(url).path.split("/") if part]
        if len(parts) < 2:
            raise ValueError("Gist URL must include owner and gist ID.")
        return parts[0], parts[1]

    def _first_filename(self, files: dict) -> str:
        for filename in files:
            return filename
        return ""

    def _get_json(self, url: str) -> dict:
        request = Request(url, headers={"User-Agent": "Lazerbeam Prototype"})
        with urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))

    def _get_text(self, url: str) -> str:
        request = Request(url, headers={"User-Agent": "Lazerbeam Prototype"})
        with urlopen(request, timeout=20) as response:
            return response.read().decode("utf-8", errors="replace")
