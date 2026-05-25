from __future__ import annotations

from abc import ABC, abstractmethod

from lazerbeam.models import CapturedItem, CaptureProfile


class SourceProvider(ABC):
    source_name: str

    @abstractmethod
    def can_handle(self, url: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def fetch(self, url: str, profile: CaptureProfile) -> CapturedItem:
        raise NotImplementedError
