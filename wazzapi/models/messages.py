from __future__ import annotations

from datetime import datetime
from typing import Any

from .base import WazzapiModel


class InteractiveButton(WazzapiModel):
    id: str
    title: str


class ButtonReplyRequest(WazzapiModel):
    phone_number: str
    body: str
    buttons: list[InteractiveButton]
    whatsapp_account_id: str
    footer: str | None = None
    contact_id: str | None = None


class CancelMessageResponse(WazzapiModel):
    success: bool
    message_id: str
    status: str


class InteractiveMessageResponse(WazzapiModel):
    success: bool
    message_id: str
    status: str
    run_id: str | None = None


class InteractiveRow(WazzapiModel):
    id: str
    title: str
    description: str | None = None


class InteractiveSection(WazzapiModel):
    title: str
    rows: list[InteractiveRow]


class ListReplyRequest(WazzapiModel):
    phone_number: str
    body: str
    button_text: str
    sections: list[InteractiveSection]
    whatsapp_account_id: str
    footer: str | None = None
    contact_id: str | None = None


class MessageItem(WazzapiModel):
    id: str
    phone_number: str
    content: str
    message_type: str = "text"
    media_type: str | None = None
    media_url: str | None = None
    status: str
    direction: str
    retry_count: int
    contact_id: str | None = None
    contact_name: str | None = None
    whatsapp_account_id: str
    campaign_id: str | None = None
    batch_id: str | None = None
    scheduled_for: datetime | None = None
    created_at: datetime
    sent_at: datetime | None = None
    delivered_at: datetime | None = None
    read_at: datetime | None = None


class MessageListResponse(WazzapiModel):
    messages: list[MessageItem]
    total_count: int
    has_more: bool
    current_page: int
    total_pages: int


class MessageResponse(WazzapiModel):
    id: str
    phone_number: str
    content: str
    message_type: str = "text"
    media_type: str | None = None
    media_url: str | None = None
    status: str
    direction: str
    failure_reason: str | None = None
    retry_count: int
    whatsapp_message_id: str | None = None
    variable_values: dict[str, Any] | None = None
    contact_id: str | None = None
    contact_name: str | None = None
    whatsapp_account_id: str
    campaign_id: str | None = None
    batch_id: str | None = None
    scheduled_for: datetime | None = None
    queued_at: datetime | None = None
    sent_at: datetime | None = None
    delivered_at: datetime | None = None
    read_at: datetime | None = None
    failed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class MessageStatsResponse(WazzapiModel):
    total: int
    by_status: dict[str, int]
    by_direction: dict[str, int]
    last_7_days: int
    last_30_days: int


class RetryMessageResponse(WazzapiModel):
    success: bool
    message_id: str
    run_id: str | None = None
    status: str


class SendMessageRequest(WazzapiModel):
    phone_number: str
    whatsapp_account_id: str
    content: str | None = None
    template_id: str | None = None
    custom_variables: dict[str, Any] | None = None
    message_type: str = "text"
    media_type: str | None = None
    media_url: str | None = None
    caption: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    location_title: str | None = None
    location_address: str | None = None
    contacts: list[dict[str, Any]] | None = None
    contact_id: str | None = None
    scheduled_for: datetime | None = None
    validate_phone: bool = False
    status_callback_url: str | None = None


class SendMessageResponse(WazzapiModel):
    success: bool
    message_id: str
    status: str
    run_id: str | None = None


__all__ = [
    "ButtonReplyRequest",
    "CancelMessageResponse",
    "InteractiveButton",
    "InteractiveMessageResponse",
    "InteractiveRow",
    "InteractiveSection",
    "ListReplyRequest",
    "MessageItem",
    "MessageListResponse",
    "MessageResponse",
    "MessageStatsResponse",
    "RetryMessageResponse",
    "SendMessageRequest",
    "SendMessageResponse",
]
