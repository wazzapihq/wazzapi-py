from __future__ import annotations

from datetime import datetime
from typing import Any

from .base import WazzapiModel


class GroupListItem(WazzapiModel):
    id: str
    name: str
    description: str | None = None
    owner: str | None = None
    participants_count: int = 0


class GroupListResponse(WazzapiModel):
    groups: list[GroupListItem]
    total: int


class GroupDetailResponse(WazzapiModel):
    id: str
    name: str
    description: str | None = None
    owner: str | None = None
    participants_count: int = 0


class GroupParticipantItem(WazzapiModel):
    id: str
    is_admin: bool = False
    is_super_admin: bool = False


class GroupParticipantsResponse(WazzapiModel):
    participants: list[GroupParticipantItem]


class GroupOperationResponseModel(WazzapiModel):
    success: bool
    details: str


class CreateGroupRequest(WazzapiModel):
    session_name: str
    name: str
    participants: list[str]


class CreateGroupResponseModel(WazzapiModel):
    success: bool
    jid: str
    name: str
    owner_jid: str | None = None
    group_created: str | None = None


class SendGroupTextRequest(WazzapiModel):
    session_name: str
    group_jid: str
    text: str
    message_id: str | None = None


class SendGroupMediaRequest(WazzapiModel):
    session_name: str
    group_jid: str
    media_url: str
    media_type: str
    caption: str | None = None
    filename: str | None = None


class SendGroupResponse(WazzapiModel):
    success: bool
    message_id: str
    status: str
    run_id: str | None = None


class UpdateParticipantsRequest(WazzapiModel):
    session_name: str
    group_jid: str
    action: str
    participants: list[str]


class GroupInviteLinkResponseModel(WazzapiModel):
    success: bool
    invite_link: str


class GroupInviteInfoResponseModel(WazzapiModel):
    success: bool
    jid: str
    name: str
    participants: int = 0
    owner_jid: str | None = None


class InviteInfoRequest(WazzapiModel):
    session_name: str
    invite_link: str


class JoinGroupRequest(WazzapiModel):
    session_name: str
    invite_link: str


class SetGroupNameRequest(WazzapiModel):
    session_name: str
    name: str


class SetGroupTopicRequest(WazzapiModel):
    session_name: str
    topic: str


class SetGroupPhotoRequest(WazzapiModel):
    session_name: str
    image_data_uri: str


class SetGroupAnnounceRequest(WazzapiModel):
    session_name: str
    announce: bool


class SetGroupLockedRequest(WazzapiModel):
    session_name: str
    locked: bool


class SetGroupEphemeralRequest(WazzapiModel):
    session_name: str
    duration: str


__all__ = [
    "CreateGroupRequest",
    "CreateGroupResponseModel",
    "GroupDetailResponse",
    "GroupInviteInfoResponseModel",
    "GroupInviteLinkResponseModel",
    "GroupListItem",
    "GroupListResponse",
    "GroupOperationResponseModel",
    "GroupParticipantItem",
    "GroupParticipantsResponse",
    "InviteInfoRequest",
    "JoinGroupRequest",
    "SendGroupMediaRequest",
    "SendGroupResponse",
    "SendGroupTextRequest",
    "SetGroupAnnounceRequest",
    "SetGroupEphemeralRequest",
    "SetGroupLockedRequest",
    "SetGroupNameRequest",
    "SetGroupPhotoRequest",
    "SetGroupTopicRequest",
    "UpdateParticipantsRequest",
]
