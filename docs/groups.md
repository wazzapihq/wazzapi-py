# Groups

Manage WhatsApp groups.

## List groups

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    response = client.groups.list(session_name="main", limit=50)

for group in response.groups:
    print(group.id, group.name, group.participants_count)
```

## Get a group

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    group = client.groups.get("123456789@g.us", session_name="main")
    print(group.name, group.description)
```

## Get group participants

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    response = client.groups.get_participants("123456789@g.us", session_name="main")

for p in response.participants:
    print(p.id, p.is_admin, p.is_super_admin)
```

## Create a group

```python
from wazzapi import CreateGroupRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    result = client.groups.create(
        CreateGroupRequest(
            session_name="main",
            name="My New Group",
            participants=["+6281234567890", "+6281234567891"],
        )
    )

print(result.jid)
```

## Send text to a group

```python
from wazzapi import SendGroupTextRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    result = client.groups.send_text(
        SendGroupTextRequest(
            session_name="main",
            group_jid="123456789@g.us",
            text="Hello everyone!",
        )
    )

print(result.message_id)
```

## Send media to a group

```python
from wazzapi import SendGroupMediaRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    result = client.groups.send_media(
        SendGroupMediaRequest(
            session_name="main",
            group_jid="123456789@g.us",
            media_url="https://example.com/image.jpg",
            media_type="image",
            caption="Group photo",
        )
    )

print(result.message_id)
```

## Add a participant

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    result = client.groups.add_participant(
        "123456789@g.us",
        session_name="main",
        participant_jid="6281234567890@s.whatsapp.net",
    )

print(result.details)
```

## Remove a participant

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    result = client.groups.remove_participant(
        "123456789@g.us",
        session_name="main",
        participant_jid="6281234567890@s.whatsapp.net",
    )

print(result.details)
```

## Update participants (promote/demote)

```python
from wazzapi import UpdateParticipantsRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    result = client.groups.update_participants(
        UpdateParticipantsRequest(
            session_name="main",
            group_jid="123456789@g.us",
            action="promote",  # or "demote", "add", "remove"
            participants=["6281234567890@s.whatsapp.net"],
        )
    )

print(result.details)
```

## Get invite link

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    result = client.groups.get_invite_link("123456789@g.us", session_name="main")
    print(result.invite_link)
```

## Get invite info

```python
from wazzapi import InviteInfoRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    result = client.groups.get_invite_info(
        InviteInfoRequest(
            session_name="main",
            invite_link="https://chat.whatsapp.com/AbCdEfGh",
        )
    )

print(result.jid, result.name)
```

## Join a group

```python
from wazzapi import JoinGroupRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    result = client.groups.join(
        JoinGroupRequest(
            session_name="main",
            invite_link="https://chat.whatsapp.com/AbCdEfGh",
        )
    )

print(result.details)
```

## Leave a group

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    result = client.groups.leave("123456789@g.us", session_name="main")
    print(result.details)
```

## Set group name

```python
from wazzapi import SetGroupNameRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    result = client.groups.set_name(
        "123456789@g.us",
        SetGroupNameRequest(session_name="main", name="New Group Name"),
    )

print(result.details)
```

## Set group topic

```python
from wazzapi import SetGroupTopicRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    result = client.groups.set_topic(
        "123456789@g.us",
        SetGroupTopicRequest(session_name="main", topic="New topic description"),
    )

print(result.details)
```

## Set group photo

```python
from wazzapi import SetGroupPhotoRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    result = client.groups.set_photo(
        "123456789@g.us",
        SetGroupPhotoRequest(
            session_name="main",
            image_data_uri="data:image/png;base64,iVBORw0KGgo...",
        ),
    )

print(result.details)
```

## Remove group photo

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    result = client.groups.remove_photo("123456789@g.us", session_name="main")
    print(result.details)
```

## Set announce mode

Only admins can send messages when announce mode is enabled.

```python
from wazzapi import SetGroupAnnounceRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    result = client.groups.set_announce(
        "123456789@g.us",
        SetGroupAnnounceRequest(session_name="main", announce=True),
    )

print(result.details)
```

## Set locked mode

Only admins can edit group info when locked mode is enabled.

```python
from wazzapi import SetGroupLockedRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    result = client.groups.set_locked(
        "123456789@g.us",
        SetGroupLockedRequest(session_name="main", locked=True),
    )

print(result.details)
```

## Set ephemeral messages

```python
from wazzapi import SetGroupEphemeralRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    result = client.groups.set_ephemeral(
        "123456789@g.us",
        SetGroupEphemeralRequest(session_name="main", duration="24h"),  # or "7d", "90d", "off"
    )

print(result.details)
```
