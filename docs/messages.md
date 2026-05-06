# Messages

Send and manage WhatsApp messages.

## Send a text message

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

## Send media

```python
from wazzapi import SendMessageRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    # Image
    client.messages.send_image(
        SendMessageRequest(
            phone_number="+6281234567890",
            whatsapp_account_id="your-whatsapp-account-id",
            media_url="https://example.com/image.jpg",
            caption="Check this out",
        )
    )

    # Video
    client.messages.send_video(
        SendMessageRequest(
            phone_number="+6281234567890",
            whatsapp_account_id="your-whatsapp-account-id",
            media_url="https://example.com/video.mp4",
            caption="Watch this",
        )
    )

    # Document
    client.messages.send_document(
        SendMessageRequest(
            phone_number="+6281234567890",
            whatsapp_account_id="your-whatsapp-account-id",
            media_url="https://example.com/doc.pdf",
        )
    )

    # Voice note
    client.messages.send_voice(
        SendMessageRequest(
            phone_number="+6281234567890",
            whatsapp_account_id="your-whatsapp-account-id",
            media_url="https://example.com/voice.ogg",
        )
    )
```

## Send a location

```python
from wazzapi import SendMessageRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    client.messages.send_location(
        SendMessageRequest(
            phone_number="+6281234567890",
            whatsapi_account_id="your-whatsapp-account-id",
            latitude=-6.2088,
            longitude=106.8456,
            location_title="Jakarta",
            location_address="Indonesia",
        )
    )
```

## Send a contact card

```python
from wazzapi import SendMessageRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    client.messages.send_contact(
        SendMessageRequest(
            phone_number="+6281234567890",
            whatsapp_account_id="your-whatsapp-account-id",
            contacts=[{"name": "Alice", "phone_number": "+6281234567891"}],
        )
    )
```

## Send interactive buttons

```python
from wazzapi import ButtonReplyRequest, InteractiveButton, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    client.messages.send_buttons(
        ButtonReplyRequest(
            phone_number="+6281234567890",
            whatsapp_account_id="your-whatsapp-account-id",
            body="Choose an option:",
            buttons=[
                InteractiveButton(id="yes", title="Yes"),
                InteractiveButton(id="no", title="No"),
            ],
            footer="Powered by WazzAPI",
        )
    )
```

## Send an interactive list

```python
from wazzapi import InteractiveRow, InteractiveSection, ListReplyRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    client.messages.send_list(
        ListReplyRequest(
            phone_number="+6281234567890",
            whatsapp_account_id="your-whatsapp-account-id",
            body="Select a plan:",
            button_text="View plans",
            sections=[
                InteractiveSection(
                    title="Plans",
                    rows=[
                        InteractiveRow(id="basic", title="Basic", description="$9/mo"),
                        InteractiveRow(id="pro", title="Pro", description="$29/mo"),
                    ],
                )
            ],
        )
    )
```

## List messages

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    response = client.messages.list(limit=50, status="sent")

for msg in response.messages:
    print(msg.id, msg.status, msg.phone_number)
```

## Get a message

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    msg = client.messages.get("msg-id")
    print(msg.status, msg.content)
```

## Retry a failed message

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    result = client.messages.retry("msg-id")
    print(result.status)
```

## Cancel a scheduled message

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    result = client.messages.cancel("msg-id")
    print(result.status)
```

## Lookup by WhatsApp message ID

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    msg = client.messages.lookup("wamid.xxx")
    print(msg.id)
```

## Message stats

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    stats = client.messages.stats()
    print(stats.total, stats.by_status)
```
