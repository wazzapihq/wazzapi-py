# Authentication

The SDK authenticates using an API key. You can find yours in the WazzAPI dashboard.

## API key

Pass it directly to the client:

```python
from wazzapi import WazzapiClient

client = WazzapiClient(api_key="your-api-key")
```

Or set it via environment variable:

```python
import os
from wazzapi import WazzapiClient

client = WazzapiClient(api_key=os.environ["WAZZAPI_API_KEY"])
```

The SDK automatically prefixes the key with `Bearer ` if it is not already present.

## Webhook secret

If you plan to receive webhooks, you also need your webhook secret:

```python
from wazzapi import WebhookHandler

handler = WebhookHandler("your-webhook-secret")
```

You can find the webhook secret in the WazzAPI dashboard under Webhook settings.
