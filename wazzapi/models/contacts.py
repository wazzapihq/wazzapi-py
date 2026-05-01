from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from .base import WazzapiModel


class AddToGroupRequest(WazzapiModel):
    contact_ids: list[str]


class AddToGroupResponse(WazzapiModel):
    success: bool
    added: int
    member_count: int


class BulkDeleteRequest(WazzapiModel):
    contact_ids: list[str]


class BulkDeleteResponse(WazzapiModel):
    success: bool
    deleted: int


class CSVExportResponse(WazzapiModel):
    csv_data: str
    count: int
    filename: str


class CSVImportRequest(WazzapiModel):
    csv_content: str
    skip_duplicates: bool | None = None


class CSVImportResponse(WazzapiModel):
    success: bool
    imported: int
    updated: int
    errors: list[str] = Field(default_factory=list)
    rows_processed: int


class ContactCreateRequest(WazzapiModel):
    phone_number: str
    name: str | None = None
    email: str | None = None
    tags: list[str] | None = None
    custom_fields: dict[str, Any] | None = None


class ContactGroupCreateRequest(WazzapiModel):
    name: str
    description: str | None = None


class ContactGroupItem(WazzapiModel):
    id: str
    name: str
    description: str | None = None
    member_count: int
    created_at: datetime


class ContactGroupListResponse(WazzapiModel):
    groups: list[ContactGroupItem]
    total: int
    limit: int
    offset: int


class ContactItem(WazzapiModel):
    id: str
    phone_number: str
    name: str | None = None
    email: str | None = None
    whatsapp_name: str | None = None
    profile_picture_url: str | None = None
    source: str
    source_details: dict[str, Any] | None = None
    is_opted_out: bool
    tags: list[str] = Field(default_factory=list)
    last_message_at: datetime | None = None
    created_at: datetime


class ContactGroupMembersResponse(WazzapiModel):
    group: ContactGroupItem
    contacts: list[ContactItem]
    total: int
    limit: int
    offset: int


class ContactGroupUpdateRequest(WazzapiModel):
    name: str | None = None
    description: str | None = None


class ContactListResponse(WazzapiModel):
    contacts: list[ContactItem]
    total: int
    limit: int
    offset: int


class ContactResponse(WazzapiModel):
    id: str
    phone_number: str
    name: str | None = None
    email: str | None = None
    whatsapp_name: str | None = None
    profile_picture_url: str | None = None
    custom_fields: dict[str, Any] | None = None
    source: str
    source_details: dict[str, Any] | None = None
    is_opted_out: bool
    opted_out_at: datetime | None = None
    tags: list[str] = Field(default_factory=list)
    last_message_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class ContactSyncHistoryItem(WazzapiModel):
    id: str
    account_id: str
    account_name: str
    sync_type: str
    status: str
    contacts_count: int
    started_at: datetime
    completed_at: datetime | None = None
    error_message: str | None = None


class ContactSyncHistoryResponse(WazzapiModel):
    history: list[ContactSyncHistoryItem]
    total: int


class ContactSyncRequest(WazzapiModel):
    whatsapp_account_id: str
    sync_type: str | None = None


class ContactSyncResponse(WazzapiModel):
    success: bool
    job_id: str | None = None
    message: str
    status: str | None = None


class ContactSyncStatusResponse(WazzapiModel):
    account_id: str
    account_name: str
    last_sync_at: datetime | None = None
    last_sync_status: str | None = None
    contacts_synced_count: int
    can_sync: bool


class ContactUpdateRequest(WazzapiModel):
    name: str | None = None
    email: str | None = None
    tags: list[str] | None = None
    custom_fields: dict[str, Any] | None = None
    is_opted_out: bool | None = None


class RemoveFromGroupRequest(WazzapiModel):
    contact_ids: list[str]


__all__ = [
    "AddToGroupRequest",
    "AddToGroupResponse",
    "BulkDeleteRequest",
    "BulkDeleteResponse",
    "CSVExportResponse",
    "CSVImportRequest",
    "CSVImportResponse",
    "ContactCreateRequest",
    "ContactGroupCreateRequest",
    "ContactGroupItem",
    "ContactGroupListResponse",
    "ContactGroupMembersResponse",
    "ContactGroupUpdateRequest",
    "ContactItem",
    "ContactListResponse",
    "ContactResponse",
    "ContactSyncHistoryItem",
    "ContactSyncHistoryResponse",
    "ContactSyncRequest",
    "ContactSyncResponse",
    "ContactSyncStatusResponse",
    "ContactUpdateRequest",
    "RemoveFromGroupRequest",
]
