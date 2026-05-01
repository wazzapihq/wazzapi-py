from __future__ import annotations

from typing import Any

import httpx


class WazzapiError(Exception):
    """Base exception for the WazzAPI SDK."""


class WazzapiAPIError(WazzapiError):
    """Raised when the WazzAPI API returns a non-success response."""

    def __init__(
        self,
        status_code: int,
        message: str,
        *,
        details: Any | None = None,
        response_text: str | None = None,
    ) -> None:
        super().__init__(f"WazzAPI API error {status_code}: {message}")
        self.status_code = status_code
        self.message = message
        self.details = details
        self.response_text = response_text

    @classmethod
    def from_response(cls, response: httpx.Response) -> "WazzapiAPIError":
        details: Any | None = None
        message = response.reason_phrase or "Request failed"

        try:
            payload = response.json()
        except ValueError:
            payload = None

        if isinstance(payload, dict):
            details = payload.get("detail", payload)
            if isinstance(details, str):
                message = details
            elif isinstance(details, list) and details:
                first_item = details[0]
                if isinstance(first_item, dict):
                    message = first_item.get("msg") or message
                else:
                    message = str(first_item)
            elif payload.get("message"):
                message = str(payload["message"])
        elif payload is not None:
            details = payload
            message = str(payload)

        return cls(
            response.status_code,
            message,
            details=details,
            response_text=response.text,
        )
