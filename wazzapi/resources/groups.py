from __future__ import annotations

from typing import Any

from .. import models
from .base import BaseResource


class GroupsResource(BaseResource):
    def list(
        self,
        *,
        session_name: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> models.GroupListResponse:
        return self._client._request(
            "GET",
            "/api/v1/groups",
            params={
                "session_name": session_name,
                "limit": limit,
                "offset": offset,
            },
            response_model=models.GroupListResponse,
        )

    def get(
        self,
        group_jid: str,
        *,
        session_name: str,
    ) -> models.GroupDetailResponse:
        return self._client._request(
            "GET",
            f"/api/v1/groups/{group_jid}",
            params={"session_name": session_name},
            response_model=models.GroupDetailResponse,
        )

    def get_participants(
        self,
        group_jid: str,
        *,
        session_name: str,
    ) -> models.GroupParticipantsResponse:
        return self._client._request(
            "GET",
            f"/api/v1/groups/{group_jid}/participants",
            params={"session_name": session_name},
            response_model=models.GroupParticipantsResponse,
        )

    def create(
        self,
        payload: models.CreateGroupRequest | dict[str, Any],
    ) -> models.CreateGroupResponseModel:
        return self._client._request(
            "POST",
            "/api/v1/groups/create",
            json_body=payload,
            response_model=models.CreateGroupResponseModel,
        )

    def send_text(
        self,
        payload: models.SendGroupTextRequest | dict[str, Any],
    ) -> models.SendGroupResponse:
        return self._client._request(
            "POST",
            "/api/v1/groups/send",
            json_body=payload,
            response_model=models.SendGroupResponse,
        )

    def send_media(
        self,
        payload: models.SendGroupMediaRequest | dict[str, Any],
    ) -> models.SendGroupResponse:
        return self._client._request(
            "POST",
            "/api/v1/groups/send/media",
            json_body=payload,
            response_model=models.SendGroupResponse,
        )

    def update_participants(
        self,
        payload: models.UpdateParticipantsRequest | dict[str, Any],
    ) -> models.GroupOperationResponseModel:
        return self._client._request(
            "POST",
            "/api/v1/groups/participants",
            json_body=payload,
            response_model=models.GroupOperationResponseModel,
        )

    def add_participant(
        self,
        group_jid: str,
        *,
        session_name: str,
        participant_jid: str,
    ) -> models.GroupOperationResponseModel:
        return self._client._request(
            "POST",
            f"/api/v1/groups/{group_jid}/participants/add",
            params={
                "session_name": session_name,
                "participant_jid": participant_jid,
            },
            response_model=models.GroupOperationResponseModel,
        )

    def remove_participant(
        self,
        group_jid: str,
        *,
        session_name: str,
        participant_jid: str,
    ) -> models.GroupOperationResponseModel:
        return self._client._request(
            "POST",
            f"/api/v1/groups/{group_jid}/participants/remove",
            params={
                "session_name": session_name,
                "participant_jid": participant_jid,
            },
            response_model=models.GroupOperationResponseModel,
        )

    def get_invite_link(
        self,
        group_jid: str,
        *,
        session_name: str,
    ) -> models.GroupInviteLinkResponseModel:
        return self._client._request(
            "POST",
            f"/api/v1/groups/{group_jid}/invite-link",
            params={"session_name": session_name},
            response_model=models.GroupInviteLinkResponseModel,
        )

    def get_invite_info(
        self,
        payload: models.InviteInfoRequest | dict[str, Any],
    ) -> models.GroupInviteInfoResponseModel:
        return self._client._request(
            "POST",
            "/api/v1/groups/invite-info",
            json_body=payload,
            response_model=models.GroupInviteInfoResponseModel,
        )

    def join(
        self,
        payload: models.JoinGroupRequest | dict[str, Any],
    ) -> models.GroupOperationResponseModel:
        return self._client._request(
            "POST",
            "/api/v1/groups/join",
            json_body=payload,
            response_model=models.GroupOperationResponseModel,
        )

    def leave(
        self,
        group_jid: str,
        *,
        session_name: str,
    ) -> models.GroupOperationResponseModel:
        return self._client._request(
            "POST",
            f"/api/v1/groups/{group_jid}/leave",
            params={"session_name": session_name},
            response_model=models.GroupOperationResponseModel,
        )

    def set_name(
        self,
        group_jid: str,
        payload: models.SetGroupNameRequest | dict[str, Any],
    ) -> models.GroupOperationResponseModel:
        return self._client._request(
            "POST",
            f"/api/v1/groups/{group_jid}/name",
            json_body=payload,
            response_model=models.GroupOperationResponseModel,
        )

    def set_topic(
        self,
        group_jid: str,
        payload: models.SetGroupTopicRequest | dict[str, Any],
    ) -> models.GroupOperationResponseModel:
        return self._client._request(
            "POST",
            f"/api/v1/groups/{group_jid}/topic",
            json_body=payload,
            response_model=models.GroupOperationResponseModel,
        )

    def set_photo(
        self,
        group_jid: str,
        payload: models.SetGroupPhotoRequest | dict[str, Any],
    ) -> models.GroupOperationResponseModel:
        return self._client._request(
            "POST",
            f"/api/v1/groups/{group_jid}/photo",
            json_body=payload,
            response_model=models.GroupOperationResponseModel,
        )

    def remove_photo(
        self,
        group_jid: str,
        *,
        session_name: str,
    ) -> models.GroupOperationResponseModel:
        return self._client._request(
            "DELETE",
            f"/api/v1/groups/{group_jid}/photo",
            params={"session_name": session_name},
            response_model=models.GroupOperationResponseModel,
        )

    def set_announce(
        self,
        group_jid: str,
        payload: models.SetGroupAnnounceRequest | dict[str, Any],
    ) -> models.GroupOperationResponseModel:
        return self._client._request(
            "POST",
            f"/api/v1/groups/{group_jid}/announce",
            json_body=payload,
            response_model=models.GroupOperationResponseModel,
        )

    def set_locked(
        self,
        group_jid: str,
        payload: models.SetGroupLockedRequest | dict[str, Any],
    ) -> models.GroupOperationResponseModel:
        return self._client._request(
            "POST",
            f"/api/v1/groups/{group_jid}/locked",
            json_body=payload,
            response_model=models.GroupOperationResponseModel,
        )

    def set_ephemeral(
        self,
        group_jid: str,
        payload: models.SetGroupEphemeralRequest | dict[str, Any],
    ) -> models.GroupOperationResponseModel:
        return self._client._request(
            "POST",
            f"/api/v1/groups/{group_jid}/ephemeral",
            json_body=payload,
            response_model=models.GroupOperationResponseModel,
        )


__all__ = ["GroupsResource"]
