# Devices

Use `client.devices` to list WhatsApp devices in your organization and inspect a single device in detail.

## List devices

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    response = client.devices.list(
        limit=50,
        status="connected",
        search="main",
        sort_by="created_at",
        sort_order="desc",
    )

for device in response.devices:
    print(device.name, device.session_name, device.status, device.phone_number)

print({"total": response.total, "limit": response.limit, "offset": response.offset})
```

Supported filters match the current WazzAPI API reference:

- `limit`
- `offset`
- `status`
- `search`
- `sort_by`
- `sort_order`

## Get a device

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    device = client.devices.get("device-id")

print(device.name)
print(device.session_name)
print(device.status)
print(device.timezone)
print(device.last_connected_at)
```
