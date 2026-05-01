from __future__ import annotations

import json
from collections.abc import Callable

import httpx
import pytest

from wazzapi import WazzapiClient, models


@pytest.mark.parametrize(
    ("call_factory", "expected_method", "expected_path", "expected_response_type", "response_json"),
    [
        (
            lambda client: client.contacts.list(limit=25, search="alice"),
            "GET",
            "/api/v1/contacts",
            models.ContactListResponse,
            {
                "contacts": [],
                "total": 0,
                "limit": 25,
                "offset": 0,
            },
        ),
        (
            lambda client: client.contacts.create({"phone_number": "+6281234567890"}),
            "POST",
            "/api/v1/contacts",
            models.ContactResponse,
            {
                "id": "contact_1",
                "phone_number": "+6281234567890",
                "source": "manual",
                "is_opted_out": False,
                "tags": [],
                "created_at": "2026-05-01T00:00:00Z",
                "updated_at": "2026-05-01T00:00:00Z",
            },
        ),
        (
            lambda client: client.messages.send({
                "phone_number": "+6281234567890",
                "whatsapp_account_id": "wa_123",
                "content": "hello",
            }),
            "POST",
            "/api/v1/messages/send",
            models.SendMessageResponse,
            {
                "success": True,
                "message_id": "msg_1",
                "status": "queued",
                "run_id": None,
            },
        ),
        (
            lambda client: client.messages.stats(),
            "GET",
            "/api/v1/messages/stats/summary",
            models.MessageStatsResponse,
            {
                "total": 10,
                "by_status": {"queued": 5, "sent": 5},
                "by_direction": {"outbound": 10},
                "last_7_days": 10,
                "last_30_days": 10,
            },
        ),
        (
            lambda client: client.templates.list(limit=10, category="marketing"),
            "GET",
            "/api/v1/templates",
            models.TemplateListResponse,
            {
                "data": [],
                "pagination": {"limit": 10, "offset": 0, "total": 0},
            },
        ),
        (
            lambda client: client.templates.preview({"content": "Hi {{name}}"}),
            "POST",
            "/api/v1/templates/preview",
            models.TemplatePreviewResponse,
            {
                "preview": "Hi Alice",
                "all_variables": ["name"],
                "builtin_variables": [],
                "custom_variables": ["name"],
                "missing_variables": [],
            },
        ),
    ],
)
def test_resource_methods_hit_expected_routes(
    call_factory: Callable[[WazzapiClient], object],
    expected_method: str,
    expected_path: str,
    expected_response_type: type[object],
    response_json: dict[str, object],
) -> None:
    seen: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["method"] = request.method
        seen["path"] = request.url.path
        seen["query"] = dict(request.url.params)
        seen["body"] = json.loads(request.content.decode("utf-8")) if request.content else None
        status_code = 201 if request.method == "POST" else 200
        return httpx.Response(status_code, json=response_json)

    transport = httpx.MockTransport(handler)
    with WazzapiClient(base_url="https://api.example.com", transport=transport) as client:
        result = call_factory(client)

    assert seen["method"] == expected_method
    assert seen["path"] == expected_path
    assert isinstance(result, expected_response_type)


def test_delete_endpoints_return_none() -> None:
    seen_paths: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen_paths.append(request.url.path)
        return httpx.Response(204)

    transport = httpx.MockTransport(handler)
    with WazzapiClient(base_url="https://api.example.com", transport=transport) as client:
        assert client.contacts.delete("contact_1") is None
        assert client.templates.delete("template_1") is None

    assert seen_paths == ["/api/v1/contacts/contact_1", "/api/v1/templates/template_1"]


def test_sync_status_returns_typed_list() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json=[
                {
                    "account_id": "wa_123",
                    "account_name": "Primary Device",
                    "last_sync_at": "2026-05-01T00:00:00Z",
                    "last_sync_status": "completed",
                    "contacts_synced_count": 42,
                    "can_sync": True,
                }
            ],
        )

    transport = httpx.MockTransport(handler)
    with WazzapiClient(base_url="https://api.example.com", transport=transport) as client:
        result = client.contacts.sync_status()

    assert len(result) == 1
    assert isinstance(result[0], models.ContactSyncStatusResponse)
    assert result[0].account_id == "wa_123"
