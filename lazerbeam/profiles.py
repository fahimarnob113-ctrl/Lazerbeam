from __future__ import annotations

from lazerbeam.models import CaptureProfile


BUILT_IN_PROFILES = {
    "Research": CaptureProfile(name="Research", include_media=True, include_comments=True),
    "Lightweight": CaptureProfile(
        name="Lightweight",
        include_media=False,
        include_comments=False,
        max_images=0,
        max_comments=0,
    ),
    "Archive": CaptureProfile(name="Archive", include_media=True, include_comments=True, max_images=100, max_comments=500),
    "Media Only": CaptureProfile(name="Media Only", include_media=True, include_comments=False, max_comments=0),
}
