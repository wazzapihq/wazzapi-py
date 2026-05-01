from __future__ import annotations

import os

from wazzapi import WazzapiClient

api_key = os.environ["WAZZAPI_API_KEY"]

with WazzapiClient(api_key=api_key) as client:
    response = client.contacts.list(limit=20, search="alice")

for contact in response.contacts:
    print(contact.model_dump())

print({"total": response.total, "limit": response.limit, "offset": response.offset})
