from __future__ import annotations

import hashlib
import hmac
import json
from collections.abc import Mapping
from typing import Any

from .models.webhooks import PublicDeviceWebhook, PublicMessageWebhook, WebhookPayload

SIGNATURE_HEADER = "X-Wazzapi-Signature"
EVENT_HEADER = "X-Wazzapi-Event"
EVENT_ID_HEADER = "X-Wazzapi-Event-ID"
_SIGNATURE_PREFIX = "sha256="


class WazzapiWebhookError(Exception):
    """Base exception for webhook helpers."""


class WazzapiWebhookVerificationError(WazzapiWebhookError):
    """Raised when webhook signature verification fails."""


class WazzapiWebhookParseError(WazzapiWebhookError):
    """Raised when a webhook payload cannot be parsed."""


def generate_webhook_signature(payload: bytes | str, secret: str) -> str:
    payload_bytes = _to_bytes(payload)
    digest = hmac.new(secret.encode("utf-8"), payload_bytes, hashlib.sha256).hexdigest()
    return f"{_SIGNATURE_PREFIX}{digest}"


def verify_webhook_signature(payload: bytes | str, signature: str, secret: str) -> bool:
    normalized_signature = signature.strip()
    expected = generate_webhook_signature(payload, secret)
    return hmac.compare_digest(expected, normalized_signature)


class WebhookHandler:
    """Verify and parse incoming WazzAPI webhook deliveries."""

    def __init__(self, secret: str) -> None:
        self.secret = secret

    def generate_signature(self, payload: bytes | str) -> str:
        return generate_webhook_signature(payload, self.secret)

    def verify_signature(self, payload: bytes | str, signature: str) -> bool:
        return verify_webhook_signature(payload, signature, self.secret)

    def verify_headers(self, payload: bytes | str, headers: Mapping[str, str]) -> None:
        signature = _get_header(headers, SIGNATURE_HEADER)
        if not signature:
            raise WazzapiWebhookVerificationError(
                f"Missing required webhook header: {SIGNATURE_HEADER}"
            )
        if not self.verify_signature(payload, signature):
            raise WazzapiWebhookVerificationError("Invalid webhook signature")

        if not _get_header(headers, EVENT_HEADER):
            raise WazzapiWebhookVerificationError(
                f"Missing required webhook header: {EVENT_HEADER}"
            )
        if not _get_header(headers, EVENT_ID_HEADER):
            raise WazzapiWebhookVerificationError(
                f"Missing required webhook header: {EVENT_ID_HEADER}"
            )

    def parse(self, payload: bytes | str) -> WebhookPayload:
        payload_bytes = _to_bytes(payload)
        try:
            raw_payload = json.loads(payload_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise WazzapiWebhookParseError("Webhook payload is not valid JSON") from exc

        if not isinstance(raw_payload, dict):
            raise WazzapiWebhookParseError("Webhook payload must be a JSON object")

        event_type = raw_payload.get("event_type")
        if not isinstance(event_type, str):
            raise WazzapiWebhookParseError("Webhook payload is missing event_type")

        if event_type.startswith("message."):
            return PublicMessageWebhook.model_validate(raw_payload)
        if event_type.startswith("device."):
            return PublicDeviceWebhook.model_validate(raw_payload)
        raise WazzapiWebhookParseError(f"Unsupported webhook event type: {event_type}")

    def verify_and_parse(self, payload: bytes | str, headers: Mapping[str, str]) -> WebhookPayload:
        self.verify_headers(payload, headers)
        parsed = self.parse(payload)
        header_event = _get_header(headers, EVENT_HEADER)
        if header_event and header_event != parsed.event_type:
            raise WazzapiWebhookVerificationError(
                "Webhook event header does not match payload event_type"
            )
        return parsed


def parse_webhook(payload: bytes | str, headers: Mapping[str, str], secret: str) -> WebhookPayload:
    return WebhookHandler(secret).verify_and_parse(payload, headers)


def _to_bytes(payload: bytes | str) -> bytes:
    if isinstance(payload, bytes):
        return payload
    return payload.encode("utf-8")


def _get_header(headers: Mapping[str, str], name: str) -> str | None:
    expected = name.lower()
    for key, value in headers.items():
        if key.lower() == expected:
            return value
    return None


__all__ = [
    "EVENT_HEADER",
    "EVENT_ID_HEADER",
    "SIGNATURE_HEADER",
    "WebhookHandler",
    "WazzapiWebhookError",
    "WazzapiWebhookParseError",
    "WazzapiWebhookVerificationError",
    "generate_webhook_signature",
    "parse_webhook",
    "verify_webhook_signature",
]
