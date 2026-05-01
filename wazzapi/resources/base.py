from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import WazzapiClient


class BaseResource:
    def __init__(self, client: "WazzapiClient") -> None:
        self._client = client


__all__ = ["BaseResource"]
