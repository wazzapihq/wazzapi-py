from __future__ import annotations

import json

import httpx
import pytest

from wazzapi import WazzapiAPIError, WazzapiClient
from wazzapi.models import ContactCreateRequest


def test_client_formats_bearer_auth_header() -> None:
    client = WazzapiClient(base_url="https://api.example.com", api_key="plain-token")
    try:
        assert client.http.headers["Authorization"] == "Bearer plain-token"
        assert client.http.headers["Accept"] == "application/json"
        assert client.http.headers["Content-Type"] == "application/json"
        assert client.devices is not None
    finally:
        client.close()


def test_client_uses_default_wazzapi_base_url() -> None:
    client = WazzapiClient(api_key="plain-token")
    try:
        assert str(client.http.base_url) == "https://api.wazzapi.com"
    finally:
        client.close()


def test_client_preserves_existing_bearer_prefix() -> None:
    client = WazzapiClient(base_url="https://api.example.com", api_key="Bearer already-set")
    try:
        assert client.http.headers["Authorization"] == "Bearer already-set"
    finally:
        client.close()


def test_client_serializes_models_and_filters_none_query_params() -> None:
    seen: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["query"] = dict(request.url.params)
        seen["body"] = json.loads(request.content.decode("utf-8"))
        return httpx.Response(
            201,
            json={
                "id": "contact_1",
                "phone_number": "+6281234567890",
                "source": "manual",
                "is_opted_out": False,
                "tags": [],
                "created_at": "2026-05-01T00:00:00Z",
                "updated_at": "2026-05-01T00:00:00Z",
            },
        )

    transport = httpx.MockTransport(handler)
    with WazzapiClient(base_url="https://api.example.com", transport=transport) as client:
        response = client._request(
            "POST",
            "/api/v1/contacts",
            params={"limit": 10, "search": None},
            json_body=ContactCreateRequest(phone_number="+6281234567890", name=None),
            response_model=None,
        )

    assert seen["query"] == {"limit": "10"}
    assert seen["body"] == {"phone_number": "+6281234567890"}
    assert response["id"] == "contact_1"


@pytest.mark.parametrize(
    ("payload", "expected_message"),
    [
        ({"detail": "Message not found"}, "Message not found"),
        ({"detail": [{"msg": "Invalid input"}]}, "Invalid input"),
        ({"message": "Rate limited"}, "Rate limited"),
    ],
)
def test_client_raises_api_error_with_parsed_message(payload: dict[str, object], expected_message: str) -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(400, json=payload)

    transport = httpx.MockTransport(handler)
    with WazzapiClient(base_url="https://api.example.com", transport=transport) as client:
        with pytest.raises(WazzapiAPIError) as exc_info:
            client._request("GET", "/api/v1/test")

    assert exc_info.value.message == expected_message
    assert exc_info.value.status_code == 400
