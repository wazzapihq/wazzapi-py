from __future__ import annotations

import os

from wazzapi import SendMessageRequest, WazzapiClient

api_key = os.environ["WAZZAPI_API_KEY"]

with WazzapiClient(api_key=api_key) as client:
    response = client.messages.send(
        SendMessageRequest(
            phone_number="+6281234567890",
            whatsapp_account_id="your-whatsapp-account-id",
            content="Hello from the WazzAPI Python SDK",
        )
    )

print(response.model_dump())
