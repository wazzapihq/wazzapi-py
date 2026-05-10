from __future__ import annotations

import os

from wazzapi import WazzapiClient

api_key = os.environ["WAZZAPI_API_KEY"]

with WazzapiClient(api_key=api_key) as client:
    response = client.devices.list(limit=20, status="connected")

for device in response.devices:
    print(device.model_dump())

print({"total": response.total, "limit": response.limit, "offset": response.offset})