from __future__ import annotations

import json
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from lazerbeam.markdown_cleaner import strip_basic_html
from lazerbeam.models import CapturedItem, CaptureProfile
from lazerbeam.sources.base import SourceProvider


class RedditProvider(SourceProvider):
    source_name = "reddit"

    def can_handle(self, url: str) -> bool:
        host = urlparse(url).netloc.lower()
        return host.endswith("reddit.com") or host.endswith("redd.it")

    def fetch(self, url: str, profile: CaptureProfile) -> CapturedItem:
        data = self._get_json(f"{url}.json")
        if self._is_wiki_url(url):
            return self._build_wiki_item(url, data)
        if not isinstance(data, list) or not data:
            raise ValueError("Reddit post response was not in the expected format.")

        try:
            post = data[0]["data"]["children"][0]["data"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ValueError("Reddit post response was not in the expected format.") from exc
        comments = []
        if profile.include_comments and len(data) > 1:
            comments = self._extract_comments(data[1]["data"]["children"], profile.max_comments)
        return CapturedItem(
            source="reddit",
            title=post.get("title", "Reddit Post"),
            url=url,
            body=strip_basic_html(post.get("selftext", "")),
            author=post.get("author", ""),
            comments=comments,
            metadata={
                "subreddit": post.get("subreddit", "reddit"),
                "score": post.get("score", 0),
                "comment_count": post.get("num_comments", 0),
            },
            tags=["reddit"],
        )

    def _get_json(self, url: str) -> list | dict:
        request = Request(url, headers={"User-Agent": "Lazerbeam Prototype"})
        with urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))

    def _is_wiki_url(self, url: str) -> bool:
        return "/wiki/" in urlparse(url).path.lower()

    def _build_wiki_item(self, url: str, data: list | dict) -> CapturedItem:
        if not isinstance(data, dict) or "data" not in data:
            raise ValueError("Reddit wiki response was not in the expected format.")

        page_data = data["data"]
        subreddit, page_name = self._parse_wiki_path(url)
        body = page_data.get("content_md") or page_data.get("content_html") or ""
        revision_by = page_data.get("revision_by") or {}

        return CapturedItem(
            source="reddit",
            title=f"{subreddit} wiki - {page_name}",
            url=url,
            body=strip_basic_html(body),
            author=revision_by.get("data", {}).get("name", ""),
            metadata={
                "subreddit": subreddit,
                "wiki_page": page_name,
                "content_type": "wiki",
                "score": 0,
                "comment_count": 0,
            },
            tags=["reddit", "wiki"],
        )

    def _parse_wiki_path(self, url: str) -> tuple[str, str]:
        parts = [part for part in urlparse(url).path.split("/") if part]
        subreddit = "reddit"
        page_name = "wiki"
        if len(parts) >= 2 and parts[0].lower() == "r":
            subreddit = parts[1]
        if "wiki" in [part.lower() for part in parts]:
            wiki_index = [part.lower() for part in parts].index("wiki")
            if len(parts) > wiki_index + 1:
                page_name = "/".join(parts[wiki_index + 1 :])
        return subreddit, page_name

    def _extract_comments(self, children: list[dict], limit: int) -> list[str]:
        comments: list[str] = []
        for child in children:
            if len(comments) >= limit:
                break
            if child.get("kind") != "t1":
                continue
            body = strip_basic_html(child.get("data", {}).get("body", ""))
            if body:
                comments.append(body)
        return comments
