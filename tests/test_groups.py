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
            lambda client: client.groups.list(session_name="main", limit=25),
            "GET",
            "/api/v1/groups",
            models.GroupListResponse,
            {"groups": [], "total": 0},
        ),
        (
            lambda client: client.groups.get("123@g.us", session_name="main"),
            "GET",
            "/api/v1/groups/123@g.us",
            models.GroupDetailResponse,
            {"id": "123@g.us", "name": "Test Group"},
        ),
        (
            lambda client: client.groups.get_participants("123@g.us", session_name="main"),
            "GET",
            "/api/v1/groups/123@g.us/participants",
            models.GroupParticipantsResponse,
            {"participants": [{"id": "6281234567890@s.whatsapp.net", "is_admin": True}]},
        ),
        (
            lambda client: client.groups.create({"session_name": "main", "name": "New Group", "participants": ["6281234567890"]}),
            "POST",
            "/api/v1/groups/create",
            models.CreateGroupResponseModel,
            {"success": True, "jid": "456@g.us", "name": "New Group"},
        ),
        (
            lambda client: client.groups.send_text({"session_name": "main", "group_jid": "123@g.us", "text": "hello"}),
            "POST",
            "/api/v1/groups/send",
            models.SendGroupResponse,
            {"success": True, "message_id": "msg_1", "status": "queued"},
        ),
        (
            lambda client: client.groups.send_media({
                "session_name": "main",
                "group_jid": "123@g.us",
                "media_url": "https://example.com/img.jpg",
                "media_type": "image",
            }),
            "POST",
            "/api/v1/groups/send/media",
            models.SendGroupResponse,
            {"success": True, "message_id": "msg_2", "status": "queued"},
        ),
        (
            lambda client: client.groups.update_participants({
                "session_name": "main",
                "group_jid": "123@g.us",
                "action": "promote",
                "participants": ["6281234567890@s.whatsapp.net"],
            }),
            "POST",
            "/api/v1/groups/participants",
            models.GroupOperationResponseModel,
            {"success": True, "details": "done"},
        ),
        (
            lambda client: client.groups.add_participant("123@g.us", session_name="main", participant_jid="6281234567890@s.whatsapp.net"),
            "POST",
            "/api/v1/groups/123@g.us/participants/add",
            models.GroupOperationResponseModel,
            {"success": True, "details": "added"},
        ),
        (
            lambda client: client.groups.remove_participant("123@g.us", session_name="main", participant_jid="6281234567890@s.whatsapp.net"),
            "POST",
            "/api/v1/groups/123@g.us/participants/remove",
            models.GroupOperationResponseModel,
            {"success": True, "details": "removed"},
        ),
        (
            lambda client: client.groups.get_invite_link("123@g.us", session_name="main"),
            "POST",
            "/api/v1/groups/123@g.us/invite-link",
            models.GroupInviteLinkResponseModel,
            {"success": True, "invite_link": "https://chat.whatsapp.com/abc"},
        ),
        (
            lambda client: client.groups.get_invite_info({"session_name": "main", "invite_link": "https://chat.whatsapp.com/abc"}),
            "POST",
            "/api/v1/groups/invite-info",
            models.GroupInviteInfoResponseModel,
            {"success": True, "jid": "789@g.us", "name": "Invited Group"},
        ),
        (
            lambda client: client.groups.join({"session_name": "main", "invite_link": "https://chat.whatsapp.com/abc"}),
            "POST",
            "/api/v1/groups/join",
            models.GroupOperationResponseModel,
            {"success": True, "details": "joined"},
        ),
        (
            lambda client: client.groups.leave("123@g.us", session_name="main"),
            "POST",
            "/api/v1/groups/123@g.us/leave",
            models.GroupOperationResponseModel,
            {"success": True, "details": "left"},
        ),
        (
            lambda client: client.groups.set_name("123@g.us", {"session_name": "main", "name": "Renamed"}),
            "POST",
            "/api/v1/groups/123@g.us/name",
            models.GroupOperationResponseModel,
            {"success": True, "details": "name updated"},
        ),
        (
            lambda client: client.groups.set_topic("123@g.us", {"session_name": "main", "topic": "new topic"}),
            "POST",
            "/api/v1/groups/123@g.us/topic",
            models.GroupOperationResponseModel,
            {"success": True, "details": "topic updated"},
        ),
        (
            lambda client: client.groups.set_photo("123@g.us", {"session_name": "main", "image_data_uri": "data:image/png;base64,abc"}),
            "POST",
            "/api/v1/groups/123@g.us/photo",
            models.GroupOperationResponseModel,
            {"success": True, "details": "photo updated"},
        ),
        (
            lambda client: client.groups.set_announce("123@g.us", {"session_name": "main", "announce": True}),
            "POST",
            "/api/v1/groups/123@g.us/announce",
            models.GroupOperationResponseModel,
            {"success": True, "details": "announce set"},
        ),
        (
            lambda client: client.groups.set_locked("123@g.us", {"session_name": "main", "locked": True}),
            "POST",
            "/api/v1/groups/123@g.us/locked",
            models.GroupOperationResponseModel,
            {"success": True, "details": "locked set"},
        ),
        (
            lambda client: client.groups.set_ephemeral("123@g.us", {"session_name": "main", "duration": "24h"}),
            "POST",
            "/api/v1/groups/123@g.us/ephemeral",
            models.GroupOperationResponseModel,
            {"success": True, "details": "ephemeral set"},
        ),
    ],
)
def test_groups_methods_hit_expected_routes(
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


def test_groups_remove_photo_returns_operation_response() -> None:
    seen: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["method"] = request.method
        seen["path"] = request.url.path
        seen["query"] = dict(request.url.params)
        return httpx.Response(
            200,
            json={"success": True, "details": "photo removed"},
        )

    transport = httpx.MockTransport(handler)
    with WazzapiClient(base_url="https://api.example.com", transport=transport) as client:
        result = client.groups.remove_photo("123@g.us", session_name="main")

    assert seen["method"] == "DELETE"
    assert seen["path"] == "/api/v1/groups/123@g.us/photo"
    assert seen["query"] == {"session_name": "main"}
    assert isinstance(result, models.GroupOperationResponseModel)
    assert result.success is True


def test_groups_list_sends_query_params() -> None:
    seen: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["query"] = dict(request.url.params)
        return httpx.Response(200, json={"groups": [], "total": 0})

    transport = httpx.MockTransport(handler)
    with WazzapiClient(base_url="https://api.example.com", transport=transport) as client:
        client.groups.list(session_name="main", limit=10, offset=5)

    assert seen["query"] == {"session_name": "main", "limit": "10", "offset": "5"}


def test_groups_get_sends_session_name_query() -> None:
    seen: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["query"] = dict(request.url.params)
        return httpx.Response(200, json={"id": "123@g.us", "name": "Test"})

    transport = httpx.MockTransport(handler)
    with WazzapiClient(base_url="https://api.example.com", transport=transport) as client:
        client.groups.get("123@g.us", session_name="main")

    assert seen["query"] == {"session_name": "main"}


def test_groups_add_participant_sends_query_params() -> None:
    seen: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["query"] = dict(request.url.params)
        return httpx.Response(200, json={"success": True, "details": "added"})

    transport = httpx.MockTransport(handler)
    with WazzapiClient(base_url="https://api.example.com", transport=transport) as client:
        client.groups.add_participant(
            "123@g.us",
            session_name="main",
            participant_jid="6281234567890@s.whatsapp.net",
        )

    assert seen["query"] == {
        "session_name": "main",
        "participant_jid": "6281234567890@s.whatsapp.net",
    }


def test_groups_models_are_importable() -> None:
    from wazzapi.models import (
        CreateGroupRequest,
        CreateGroupResponseModel,
        GroupDetailResponse,
        GroupInviteInfoResponseModel,
        GroupInviteLinkResponseModel,
        GroupListItem,
        GroupListResponse,
        GroupOperationResponseModel,
        GroupParticipantItem,
        GroupParticipantsResponse,
        InviteInfoRequest,
        JoinGroupRequest,
        SendGroupMediaRequest,
        SendGroupResponse,
        SendGroupTextRequest,
        SetGroupAnnounceRequest,
        SetGroupEphemeralRequest,
        SetGroupLockedRequest,
        SetGroupNameRequest,
        SetGroupPhotoRequest,
        SetGroupTopicRequest,
        UpdateParticipantsRequest,
    )

    assert GroupListItem is not None
    assert CreateGroupResponseModel is not None
