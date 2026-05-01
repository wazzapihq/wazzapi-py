from __future__ import annotations

import os

from wazzapi import TemplateCreateRequest, WazzapiClient

api_key = os.environ["WAZZAPI_API_KEY"]

with WazzapiClient(api_key=api_key) as client:
    response = client.templates.create(
        TemplateCreateRequest(
            name="welcome-message",
            category="marketing",
            content="Hi {{name}}, welcome to WazzAPI!",
        )
    )

print(response.model_dump())
