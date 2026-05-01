from __future__ import annotations

from typing import Any

from .. import models
from .base import BaseResource


class MessagesResource(BaseResource):
    def lookup(self, whatsapp_message_id: str) -> models.MessageResponse:
        return self._client._request(
            "GET",
            "/api/v1/messages/lookup",
            params={"whatsapp_message_id": whatsapp_message_id},
            response_model=models.MessageResponse,
        )

    def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        status: str | None = None,
        direction: str | None = None,
        whatsapp_account_id: str | None = None,
        search: str | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
    ) -> models.MessageListResponse:
        return self._client._request(
            "GET",
            "/api/v1/messages",
            params={
                "limit": limit,
                "offset": offset,
                "status": status,
                "direction": direction,
                "whatsapp_account_id": whatsapp_account_id,
                "search": search,
                "sort_by": sort_by,
                "sort_order": sort_order,
            },
            response_model=models.MessageListResponse,
        )

    def get(self, message_id: str) -> models.MessageResponse:
        return self._client._request(
            "GET",
            f"/api/v1/messages/{message_id}",
            response_model=models.MessageResponse,
        )

    def stats(self) -> models.MessageStatsResponse:
        return self._client._request(
            "GET",
            "/api/v1/messages/stats/summary",
            response_model=models.MessageStatsResponse,
        )

    def send(
        self,
        payload: models.SendMessageRequest | dict[str, Any],
    ) -> models.SendMessageResponse:
        return self._client._request(
            "POST",
            "/api/v1/messages/send",
            json_body=payload,
            response_model=models.SendMessageResponse,
        )

    def send_image(
        self,
        payload: models.SendMessageRequest | dict[str, Any],
    ) -> models.SendMessageResponse:
        return self._client._request(
            "POST",
            "/api/v1/messages/send/image",
            json_body=payload,
            response_model=models.SendMessageResponse,
        )

    def send_video(
        self,
        payload: models.SendMessageRequest | dict[str, Any],
    ) -> models.SendMessageResponse:
        return self._client._request(
            "POST",
            "/api/v1/messages/send/video",
            json_body=payload,
            response_model=models.SendMessageResponse,
        )

    def send_voice(
        self,
        payload: models.SendMessageRequest | dict[str, Any],
    ) -> models.SendMessageResponse:
        return self._client._request(
            "POST",
            "/api/v1/messages/send/voice",
            json_body=payload,
            response_model=models.SendMessageResponse,
        )

    def send_document(
        self,
        payload: models.SendMessageRequest | dict[str, Any],
    ) -> models.SendMessageResponse:
        return self._client._request(
            "POST",
            "/api/v1/messages/send/document",
            json_body=payload,
            response_model=models.SendMessageResponse,
        )

    def send_location(
        self,
        payload: models.SendMessageRequest | dict[str, Any],
    ) -> models.SendMessageResponse:
        return self._client._request(
            "POST",
            "/api/v1/messages/send/location",
            json_body=payload,
            response_model=models.SendMessageResponse,
        )

    def send_contact(
        self,
        payload: models.SendMessageRequest | dict[str, Any],
    ) -> models.SendMessageResponse:
        return self._client._request(
            "POST",
            "/api/v1/messages/send/contact",
            json_body=payload,
            response_model=models.SendMessageResponse,
        )

    def retry(self, message_id: str) -> models.RetryMessageResponse:
        return self._client._request(
            "POST",
            f"/api/v1/messages/{message_id}/retry",
            response_model=models.RetryMessageResponse,
        )

    def cancel(self, message_id: str) -> models.CancelMessageResponse:
        return self._client._request(
            "POST",
            f"/api/v1/messages/{message_id}/cancel",
            response_model=models.CancelMessageResponse,
        )

    def send_buttons(
        self,
        payload: models.ButtonReplyRequest | dict[str, Any],
    ) -> models.InteractiveMessageResponse:
        return self._client._request(
            "POST",
            "/api/v1/messages/send/interactive/buttons",
            json_body=payload,
            response_model=models.InteractiveMessageResponse,
        )

    def send_list(
        self,
        payload: models.ListReplyRequest | dict[str, Any],
    ) -> models.InteractiveMessageResponse:
        return self._client._request(
            "POST",
            "/api/v1/messages/send/interactive/list",
            json_body=payload,
            response_model=models.InteractiveMessageResponse,
        )


__all__ = ["MessagesResource"]
