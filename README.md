# WazzAPI Python SDK

Official Python SDK for WazzAPI.

Use it to send messages, manage contacts and templates, and verify incoming webhooks with a simple typed client.

## What you can do with this SDK

- send direct WhatsApp messages
- list, create, update, and delete contacts
- manage message templates and preview rendered content
- verify and parse incoming WazzAPI webhooks
- work with typed request and response models

## Requirements

- Python 3.10+
- a WazzAPI account
- a WazzAPI API key

## Install

From PyPI:

```bash
pip install wazzapi
```

With uv:

```bash
uv add wazzapi
```

Need a WazzAPI account first?

Sign up at `https://app.wazzapi.com` using your Google organization account. On first sign-in, WazzAPI creates a new workspace for you automatically.

## Configuration

For most integrations, you only need your API key:

- `WAZZAPI_API_KEY`

If you plan to receive webhooks, also configure:

- `WAZZAPI_WEBHOOK_SECRET`

The SDK uses `https://api.wazzapi.com` by default, so you do not need to set a base URL.

## Quick start

### Send a message

```python
from wazzapi import SendMessageRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    response = client.messages.send(
        SendMessageRequest(
            phone_number="+6281234567890",
            whatsapp_account_id="your-whatsapp-account-id",
            content="Hello from WazzAPI!",
        )
    )

print(response.model_dump())
```

## Error handling

When the API returns a non-success response, the SDK raises `WazzapiAPIError`.

```python
from wazzapi import WazzapiAPIError, WazzapiClient

try:
    with WazzapiClient(api_key="your-api-key") as client:
        client.messages.get("missing-message-id")
except WazzapiAPIError as exc:
    print(exc.status_code)
    print(exc.message)
```

## More usage examples

### List contacts

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    response = client.contacts.list(limit=20, search="alice")

for contact in response.contacts:
    print(contact.model_dump())
```

### Create a template

```python
from wazzapi import TemplateCreateRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    template = client.templates.create(
        TemplateCreateRequest(
            name="welcome-message",
            category="marketing",
            content="Hi {{name}}, welcome to WazzAPI!",
        )
    )

print(template.model_dump())
```

### Preview a template

```python
from wazzapi import TemplatePreviewRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    preview = client.templates.preview(
        TemplatePreviewRequest(
            content="Hi {{name}}, your code is {{code}}.",
            custom_variables={"name": "Alice", "code": "WZ-1234"},
        )
    )

print(preview.model_dump())
```

## Webhook verification

Use `WebhookHandler` to verify the raw request body against `X-Wazzapi-Signature` before parsing JSON.

```python
from wazzapi import WebhookHandler

handler = WebhookHandler("your-webhook-secret")
webhook = handler.verify_and_parse(raw_body, request.headers)

print(webhook.event_type)
print(webhook.data.model_dump())
```

WazzAPI webhook headers:

- `X-Wazzapi-Signature`
- `X-Wazzapi-Event`
- `X-Wazzapi-Event-ID`

Supported webhook event families:

- message events: `message.received`, `message.sent`, `message.delivered`, `message.read`, `message.failed`
- device events: `device.connected`, `device.disconnected`

## Examples

Ready-to-run examples live in `examples/`:

- `examples/list_contacts.py`
- `examples/send_message.py`
- `examples/create_template.py`
- `examples/preview_template.py`
- `examples/verify_webhook.py`

Run them with:

```bash
uv run python examples/list_contacts.py
uv run python examples/send_message.py
uv run python examples/create_template.py
uv run python examples/preview_template.py
uv run python examples/verify_webhook.py
```

## Release automation

This repository includes a GitHub Actions workflow that publishes to PyPI automatically when a tag matching `v*` is pushed.
