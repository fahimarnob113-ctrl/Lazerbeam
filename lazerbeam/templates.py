from __future__ import annotations

import html
from string import Template

from lazerbeam.models import CapturedItem, OutputPlan


def render_frontmatter(item: CapturedItem, plan: OutputPlan) -> str:
    tags = "\n".join(f"  - {tag}" for tag in plan.tags)
    lines = [
        "---",
        f"source: {item.source}",
        f"url: {item.url}",
        f"captured_at: {item.captured_at}",
        "tags:",
        tags or "  - lazerbeam",
    ]
    for key, value in sorted(item.metadata.items()):
        if isinstance(value, (str, int, float, bool)) and key not in {"body"}:
            lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines)


def render_markdown(item: CapturedItem, plan: OutputPlan) -> str:
    comments = "\n\n".join(f"- {comment}" for comment in item.comments)
    media = "\n".join(f"![[{media.filename}]]" for media in item.media if media.filename)
    template = Template(
        "$frontmatter\n\n"
        "# $title\n\n"
        "$media_section"
        "$body\n\n"
        "$comments_section"
        "## Source\n\n"
        "$url\n"
    )
    return template.substitute(
        frontmatter=render_frontmatter(item, plan),
        title=html.escape(item.title),
        body=item.body.strip(),
        url=item.url,
        comments_section=f"## Comments\n\n{comments}\n\n" if comments else "",
        media_section=f"## Media\n\n{media}\n" if media else "",
    ).strip() + "\n"
