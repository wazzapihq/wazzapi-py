from __future__ import annotations

import json
import os

from wazzapi import WebhookHandler

secret = os.environ["WAZZAPI_WEBHOOK_SECRET"]
handler = WebhookHandler(secret)

raw_body = json.dumps(
    {
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
    },
    separators=(",", ":"),
)

headers = {
    "X-Wazzapi-Signature": handler.generate_signature(raw_body),
    "X-Wazzapi-Event": "message.received",
    "X-Wazzapi-Event-ID": "2e0b76fe-f5b4-4e50-80cb-ec7cce2c8fd5",
}

webhook = handler.verify_and_parse(raw_body, headers)
print(webhook.event_type)
print(webhook.data.model_dump())
