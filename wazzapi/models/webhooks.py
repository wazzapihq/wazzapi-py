from __future__ import annotations

from datetime import datetime
from typing import Literal

from .base import WazzapiModel

MessageWebhookEvent = Literal[
    "message.received",
    "message.sent",
    "message.delivered",
    "message.read",
    "message.failed",
]
DeviceWebhookEvent = Literal["device.connected", "device.disconnected"]
WebhookEvent = MessageWebhookEvent | DeviceWebhookEvent


class PublicWebhookMessageData(WazzapiModel):
    message_id: str
    whatsapp_message_id: str | None = None
    phone_number: str
    account_name: str | None = None
    status: str
    direction: str
    message_type: str
    failure_reason: str | None = None
    reason: str | None = None
    sent_at: datetime | None = None
    delivered_at: datetime | None = None
    read_at: datetime | None = None
    failed_at: datetime | None = None
    whatsapp_account_id: str
    campaign_id: str | None = None
    batch_id: str | None = None


class PublicWebhookDeviceData(WazzapiModel):
    message_id: str
    whatsapp_message_id: str | None = None
    phone_number: str
    account_name: str | None = None
    status: str
    direction: str
    message_type: str
    failure_reason: str | None = None
    reason: str | None = None
    sent_at: datetime | None = None
    delivered_at: datetime | None = None
    read_at: datetime | None = None
    failed_at: datetime | None = None
    whatsapp_account_id: str
    campaign_id: str | None = None
    batch_id: str | None = None


class PublicMessageWebhook(WazzapiModel):
    id: str
    event_type: MessageWebhookEvent
    timestamp: datetime
    organization_id: str
    webhook_id: str
    data: PublicWebhookMessageData


class PublicDeviceWebhook(WazzapiModel):
    id: str
    event_type: DeviceWebhookEvent
    timestamp: datetime
    organization_id: str
    webhook_id: str
    data: PublicWebhookDeviceData


WebhookPayload = PublicMessageWebhook | PublicDeviceWebhook


__all__ = [
    "DeviceWebhookEvent",
    "MessageWebhookEvent",
    "PublicDeviceWebhook",
    "PublicMessageWebhook",
    "PublicWebhookDeviceData",
    "PublicWebhookMessageData",
    "WebhookEvent",
    "WebhookPayload",
]
