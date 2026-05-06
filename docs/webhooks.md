# Webhooks

WazzAPI sends webhook events to your endpoint for incoming messages, message status updates, and device status changes.

## Verify and parse

Always verify the signature before parsing the payload:

```python
from wazzapi import WebhookHandler

handler = WebhookHandler("your-webhook-secret")
webhook = handler.verify_and_parse(raw_body, request.headers)

print(webhook.event_type)
print(webhook.data.model_dump())
```

## Headers

WazzAPI sends these headers with every webhook:

| Header | Description |
|--------|-------------|
| `X-Wazzapi-Signature` | HMAC-SHA256 signature of the raw body |
| `X-Wazzapi-Event` | Event type (e.g., `message.received`) |
| `X-Wazzapi-Event-ID` | Unique event ID |

## Supported events

### Message events

- `message.received` — incoming message
- `message.sent` — outbound message accepted by WhatsApp
- `message.delivered` — outbound message delivered
- `message.read` — outbound message read by recipient
- `message.failed` — outbound message failed

### Device events

- `device.connected` — WhatsApp device connected
- `device.disconnected` — WhatsApp device disconnected

## Working with message webhooks

```python
from wazzapi import WebhookHandler
from wazzapi.models import PublicMessageWebhook

handler = WebhookHandler("your-webhook-secret")
webhook = handler.verify_and_parse(raw_body, request.headers)

if isinstance(webhook, PublicMessageWebhook):
    print(webhook.data.phone_number)
    print(webhook.data.status)
    print(webhook.data.message_type)
```

## Working with device webhooks

```python
from wazzapi import WebhookHandler
from wazzapi.models import PublicDeviceWebhook

handler = WebhookHandler("your-webhook-secret")
webhook = handler.verify_and_parse(raw_body, request.headers)

if isinstance(webhook, PublicDeviceWebhook):
    print(webhook.data.status)
    print(webhook.data.reason)
```

## Parse only (without verification)

For debugging or if you handle verification separately:

```python
from wazzapi import WebhookHandler

handler = WebhookHandler("your-webhook-secret")
webhook = handler.parse(raw_body)
print(webhook.event_type)
```

## Low-level signature verification

```python
from wazzapi import generate_webhook_signature, verify_webhook_signature

expected = generate_webhook_signature(raw_body, "your-webhook-secret")
is_valid = verify_webhook_signature(raw_body, request.headers["X-Wazzapi-Signature"], "your-webhook-secret")
```
