from __future__ import annotations

from .base import WazzapiModel


class MediaDownloadResult(WazzapiModel):
    content: bytes
    mimetype: str
    file_name: str
    file_size: int


__all__ = ["MediaDownloadResult"]
