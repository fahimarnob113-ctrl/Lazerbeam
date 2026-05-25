from __future__ import annotations

import re


def strip_basic_html(value: str) -> str:
    value = re.sub(r"<br\s*/?>", "\n", value, flags=re.IGNORECASE)
    return re.sub(r"<[^>]+>", "", value).strip()
