from __future__ import annotations

from datetime import datetime

from .base import WazzapiModel


class DeviceItem(WazzapiModel):
    id: str
    name: str
    session_name: str
    status: str
    is_primary: bool
    auto_warmer_enabled: bool
    total_messages_sent: int
    total_messages_received: int
    contacts_synced_count: int
    created_at: datetime
    updated_at: datetime
    phone_number: str | None = None
    last_connected_at: datetime | None = None
    last_health_check_at: datetime | None = None
    last_contact_sync_at: datetime | None = None
    last_contact_sync_status: str | None = None


class DeviceListResponse(WazzapiModel):
    devices: list[DeviceItem]
    total: int
    limit: int
    offset: int


class DeviceResponse(DeviceItem):
    timezone: str
    connection_attempts: int
    daily_message_limit: int
    message_delay_ms: int
    backend_id: str | None = None


__all__ = ["DeviceItem", "DeviceListResponse", "DeviceResponse"]