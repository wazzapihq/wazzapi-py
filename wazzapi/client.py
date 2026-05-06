from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import httpx
from pydantic import BaseModel, TypeAdapter

from .errors import WazzapiAPIError
from .resources import ContactsResource, GroupsResource, MessagesResource, TemplatesResource

DEFAULT_BASE_URL = "https://api.wazzapi.com"


class WazzapiClient:
    """Synchronous client for the WazzAPI API."""

    def __init__(
        self,
        *,
        base_url: str = DEFAULT_BASE_URL,
        api_key: str | None = None,
        timeout: float = 30.0,
        headers: Mapping[str, str] | None = None,
        client: httpx.Client | None = None,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        base_headers = self._build_headers(
            api_key=api_key,
            headers=headers,
        )

        self._owns_client = client is None
        self._client = client or httpx.Client(
            base_url=base_url.rstrip("/"),
            timeout=timeout,
            headers=base_headers,
            transport=transport,
        )

        self.contacts = ContactsResource(self)
        self.groups = GroupsResource(self)
        self.messages = MessagesResource(self)
        self.templates = TemplatesResource(self)

    @staticmethod
    def _build_headers(
        *,
        api_key: str | None,
        headers: Mapping[str, str] | None,
    ) -> dict[str, str]:
        merged_headers: dict[str, str] = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        if headers:
            merged_headers.update(dict(headers))

        if api_key:
            merged_headers["Authorization"] = (
                api_key if api_key.lower().startswith("bearer ") else f"Bearer {api_key}"
            )

        return merged_headers

    @property
    def http(self) -> httpx.Client:
        return self._client

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> "WazzapiClient":
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close()

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json_body: BaseModel | Mapping[str, Any] | None = None,
        response_model: Any | None = None,
    ) -> Any:
        response = self._client.request(
            method,
            path,
            params=self._filter_none(params),
            json=self._normalize_body(json_body),
        )

        if response.status_code >= 400:
            raise WazzapiAPIError.from_response(response)

        if response.status_code == 204 or not response.content:
            return None

        if response_model is None:
            return response.json()

        payload = response.json()
        return TypeAdapter(response_model).validate_python(payload)

    @staticmethod
    def _filter_none(data: Mapping[str, Any] | None) -> dict[str, Any] | None:
        if data is None:
            return None
        return {key: value for key, value in data.items() if value is not None}

    @staticmethod
    def _normalize_body(data: BaseModel | Mapping[str, Any] | None) -> dict[str, Any] | None:
        if data is None:
            return None
        if isinstance(data, BaseModel):
            return data.model_dump(mode="json", exclude_none=True)
        return {key: value for key, value in data.items() if value is not None}
