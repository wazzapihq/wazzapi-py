# Client

`WazzapiClient` is the main entry point for all API calls.

## Initialize

```python
from wazzapi import WazzapiClient

client = WazzapiClient(api_key="your-api-key")
```

## Context manager

Always close the underlying HTTP client when you are done. The easiest way is to use the context manager:

```python
with WazzapiClient(api_key="your-api-key") as client:
    response = client.messages.list()
```

## Custom base URL

For testing or custom deployments:

```python
client = WazzapiClient(
    base_url="https://api.example.com",
    api_key="your-api-key",
)
```

## Custom timeout

```python
client = WazzapiClient(
    api_key="your-api-key",
    timeout=60.0,
)
```

## Bring your own httpx client

```python
import httpx

http = httpx.Client(timeout=120.0)
client = WazzapiClient(api_key="your-api-key", client=http)
```

## Resources

The client exposes resources as attributes:

| Resource | Description |
|----------|-------------|
| `client.contacts` | Contact and contact-group management |
| `client.groups` | WhatsApp group management |
| `client.messages` | Send and manage messages |
| `client.templates` | Message template management |
