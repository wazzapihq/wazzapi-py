# WazzAPI Python SDK

Official Python SDK for the [WazzAPI](https://wazzapi.com) platform.

## What you can do

- Send direct WhatsApp messages (text, image, video, document, location, contact card, interactive buttons and lists)
- Manage WhatsApp groups (create, join, leave, participants, settings)
- Manage contacts and contact groups
- Create and preview message templates
- Verify and parse incoming webhooks
- Work with fully typed request and response models

## Requirements

- Python 3.10+
- A WazzAPI account
- A WazzAPI API key

## Install

```bash
pip install wazzapi
```

With uv:

```bash
uv add wazzapi
```

## Quick start

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

print(response.message_id)
```

## Topics

- [Authentication](authentication.md)
- [Client](client.md)
- [Messages](messages.md)
- [Groups](groups.md)
- [Contacts](contacts.md)
- [Templates](templates.md)
- [Webhooks](webhooks.md)
- [Media](media.md)
- [Errors](errors.md)
