# Errors

The SDK raises typed exceptions for API and media errors.

## WazzapiAPIError

Raised when the API returns a non-2xx response:

```python
from wazzapi import WazzapiAPIError, WazzapiClient

try:
    with WazzapiClient(api_key="your-api-key") as client:
        client.messages.get("missing-message-id")
except WazzapiAPIError as exc:
    print(exc.status_code)  # 404
    print(exc.message)      # "Message not found"
```

## WazzapiMediaError

Raised when a media download fails:

```python
from wazzapi import WazzapiMediaError, download_media

try:
    download_media("https://example.com/missing.jpg")
except WazzapiMediaError as exc:
    print(exc.message)
```

## Exception hierarchy

```
WazzapiError
├── WazzapiAPIError
├── WazzapiMediaError
├── WazzapiWebhookError
│   ├── WazzapiWebhookVerificationError
│   └── WazzapiWebhookParseError
```
