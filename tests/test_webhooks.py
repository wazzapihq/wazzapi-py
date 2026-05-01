from __future__ import annotations

import json

import pytest

from wazzapi import WebhookHandler, parse_webhook
from wazzapi.models import PublicDeviceWebhook, PublicMessageWebhook
from wazzapi.webhooks import (
    EVENT_HEADER,
    EVENT_ID_HEADER,
    SIGNATURE_HEADER,
    WazzapiWebhookParseError,
    WazzapiWebhookVerificationError,
    generate_webhook_signature,
    verify_webhook_signature,
)

SECRET = "super-secret"

MESSAGE_PAYLOAD = {
    "id": "97e1d724-f38d-46f6-bc4c-d9e0f4cf9285",
    "event_type": "message.received",
    "timestamp": "2026-04-26T09:15:30Z",
    "organization_id": "0f1d6e38-d6bc-49be-9c39-1fcf2f946d7e",
    "webhook_id": "a17d6351-d8f6-4cd8-ae0e-fce090afdb8f",
    "data": {
        "message_id": "f4fd147d-e2a8-4d52-9eb5-98a72f5b90ab",
        "whatsapp_message_id": "wamid.123",
        "phone_number": "6281234567890",
        "account_name": "Support Device",
        "status": "delivered",
        "direction": "inbound",
        "message_type": "text",
        "failure_reason": None,
        "reason": None,
        "sent_at": None,
        "delivered_at": "2026-04-26T09:15:29Z",
        "read_at": None,
        "failed_at": None,
        "whatsapp_account_id": "c053d8ef-6c19-4ecb-9cc5-a4a64be79d92",
        "campaign_id": None,
        "batch_id": None,
    },
}

DEVICE_PAYLOAD = {
    "id": "37d0d32f-75e7-4874-9875-e29442d7d37c",
    "event_type": "device.connected",
    "timestamp": "2026-04-26T11:00:00Z",
    "organization_id": "0f1d6e38-d6bc-49be-9c39-1fcf2f946d7e",
    "webhook_id": "a17d6351-d8f6-4cd8-ae0e-fce090afdb8f",
    "data": {
        "message_id": "",
        "whatsapp_message_id": None,
        "phone_number": "6281234567890",
        "account_name": "Primary Device",
        "status": "connected",
        "direction": "system",
        "message_type": "system",
        "failure_reason": None,
        "reason": "Connected",
        "sent_at": None,
        "delivered_at": None,
        "read_at": None,
        "failed_at": None,
        "whatsapp_account_id": "c053d8ef-6c19-4ecb-9cc5-a4a64be79d92",
        "campaign_id": None,
        "batch_id": None,
    },
}


def _encode(payload: dict[str, object]) -> bytes:
    return json.dumps(payload, separators=(",", ":")).encode("utf-8")


def test_generate_and_verify_signature() -> None:
    payload = _encode(MESSAGE_PAYLOAD)
    signature = generate_webhook_signature(payload, SECRET)

    assert signature.startswith("sha256=")
    assert verify_webhook_signature(payload, signature, SECRET) is True
    assert verify_webhook_signature(payload, "sha256=deadbeef", SECRET) is False


def test_handler_verifies_and_parses_message_webhook() -> None:
    payload = _encode(MESSAGE_PAYLOAD)
    handler = WebhookHandler(SECRET)
    headers = {
        SIGNATURE_HEADER: handler.generate_signature(payload),
        EVENT_HEADER: "message.received",
        EVENT_ID_HEADER: "2e0b76fe-f5b4-4e50-80cb-ec7cce2c8fd5",
    }

    parsed = handler.verify_and_parse(payload, headers)

    assert isinstance(parsed, PublicMessageWebhook)
    assert parsed.event_type == "message.received"
    assert parsed.data.phone_number == "6281234567890"


def test_handler_verifies_and_parses_device_webhook() -> None:
    payload = _encode(DEVICE_PAYLOAD)
    handler = WebhookHandler(SECRET)
    headers = {
        SIGNATURE_HEADER: handler.generate_signature(payload),
        EVENT_HEADER: "device.connected",
        EVENT_ID_HEADER: "2e0b76fe-f5b4-4e50-80cb-ec7cce2c8fd5",
    }

    parsed = parse_webhook(payload, headers, SECRET)

    assert isinstance(parsed, PublicDeviceWebhook)
    assert parsed.data.status == "connected"


@pytest.mark.parametrize(
    "headers",
    [
        {},
        {EVENT_HEADER: "message.received", EVENT_ID_HEADER: "abc"},
        {SIGNATURE_HEADER: "sha256=bad", EVENT_ID_HEADER: "abc"},
    ],
)
def test_handler_rejects_missing_or_invalid_headers(headers: dict[str, str]) -> None:
    payload = _encode(MESSAGE_PAYLOAD)
    handler = WebhookHandler(SECRET)

    with pytest.raises(WazzapiWebhookVerificationError):
        handler.verify_and_parse(payload, headers)


def test_handler_rejects_event_header_mismatch() -> None:
    payload = _encode(MESSAGE_PAYLOAD)
    handler = WebhookHandler(SECRET)
    headers = {
        SIGNATURE_HEADER: handler.generate_signature(payload),
        EVENT_HEADER: "message.failed",
        EVENT_ID_HEADER: "2e0b76fe-f5b4-4e50-80cb-ec7cce2c8fd5",
    }

    with pytest.raises(WazzapiWebhookVerificationError):
        handler.verify_and_parse(payload, headers)


def test_handler_rejects_invalid_json() -> None:
    handler = WebhookHandler(SECRET)
    bad_payload = b"not-json"
    headers = {
        SIGNATURE_HEADER: handler.generate_signature(bad_payload),
        EVENT_HEADER: "message.received",
        EVENT_ID_HEADER: "2e0b76fe-f5b4-4e50-80cb-ec7cce2c8fd5",
    }

    with pytest.raises(WazzapiWebhookParseError):
        handler.verify_and_parse(bad_payload, headers)
