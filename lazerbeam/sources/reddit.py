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
        post = data[0]["data"]["children"][0]["data"]
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

    def _get_json(self, url: str) -> list:
        request = Request(url, headers={"User-Agent": "Lazerbeam Prototype"})
        with urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))

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
