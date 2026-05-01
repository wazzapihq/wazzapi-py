from __future__ import annotations

import os

from wazzapi import TemplatePreviewRequest, WazzapiClient

api_key = os.environ["WAZZAPI_API_KEY"]

with WazzapiClient(api_key=api_key) as client:
    preview = client.templates.preview(
        TemplatePreviewRequest(
            content="Hi {{name}}, your code is {{code}}.",
            custom_variables={"name": "Alice", "code": "WZ-1234"},
        )
    )

print(preview.model_dump())
