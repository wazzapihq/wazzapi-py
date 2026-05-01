from __future__ import annotations

from typing import Any

from .. import models
from .base import BaseResource


class ContactsResource(BaseResource):
    def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        search: str | None = None,
        source: str | None = None,
        group_id: str | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
    ) -> models.ContactListResponse:
        return self._client._request(
            "GET",
            "/api/v1/contacts",
            params={
                "limit": limit,
                "offset": offset,
                "search": search,
                "source": source,
                "group_id": group_id,
                "sort_by": sort_by,
                "sort_order": sort_order,
            },
            response_model=models.ContactListResponse,
        )

    def create(
        self,
        payload: models.ContactCreateRequest | dict[str, Any],
    ) -> models.ContactResponse:
        return self._client._request(
            "POST",
            "/api/v1/contacts",
            json_body=payload,
            response_model=models.ContactResponse,
        )

    def bulk_delete(
        self,
        payload: models.BulkDeleteRequest | dict[str, Any],
    ) -> models.BulkDeleteResponse:
        return self._client._request(
            "POST",
            "/api/v1/contacts/bulk-delete",
            json_body=payload,
            response_model=models.BulkDeleteResponse,
        )

    def list_groups(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> models.ContactGroupListResponse:
        return self._client._request(
            "GET",
            "/api/v1/contacts/groups",
            params={"limit": limit, "offset": offset},
            response_model=models.ContactGroupListResponse,
        )

    def create_group(
        self,
        payload: models.ContactGroupCreateRequest | dict[str, Any],
    ) -> models.ContactGroupItem:
        return self._client._request(
            "POST",
            "/api/v1/contacts/groups",
            json_body=payload,
            response_model=models.ContactGroupItem,
        )

    def get_group(
        self,
        group_id: str,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> models.ContactGroupMembersResponse:
        return self._client._request(
            "GET",
            f"/api/v1/contacts/groups/{group_id}",
            params={"limit": limit, "offset": offset},
            response_model=models.ContactGroupMembersResponse,
        )

    def update_group(
        self,
        group_id: str,
        payload: models.ContactGroupUpdateRequest | dict[str, Any],
    ) -> models.ContactGroupItem:
        return self._client._request(
            "PATCH",
            f"/api/v1/contacts/groups/{group_id}",
            json_body=payload,
            response_model=models.ContactGroupItem,
        )

    def delete_group(self, group_id: str) -> None:
        self._client._request("DELETE", f"/api/v1/contacts/groups/{group_id}")
        return None

    def add_to_group(
        self,
        group_id: str,
        payload: models.AddToGroupRequest | dict[str, Any],
    ) -> models.AddToGroupResponse:
        return self._client._request(
            "POST",
            f"/api/v1/contacts/groups/{group_id}/members",
            json_body=payload,
            response_model=models.AddToGroupResponse,
        )

    def remove_from_group(
        self,
        group_id: str,
        payload: models.RemoveFromGroupRequest | dict[str, Any],
    ) -> models.AddToGroupResponse:
        return self._client._request(
            "DELETE",
            f"/api/v1/contacts/groups/{group_id}/members",
            json_body=payload,
            response_model=models.AddToGroupResponse,
        )

    def import_csv(
        self,
        payload: models.CSVImportRequest | dict[str, Any],
    ) -> models.CSVImportResponse:
        return self._client._request(
            "POST",
            "/api/v1/contacts/import/csv",
            json_body=payload,
            response_model=models.CSVImportResponse,
        )

    def export_csv(
        self,
        *,
        group_id: str | None = None,
        source: str | None = None,
    ) -> models.CSVExportResponse:
        return self._client._request(
            "GET",
            "/api/v1/contacts/export/csv",
            params={"group_id": group_id, "source": source},
            response_model=models.CSVExportResponse,
        )

    def sync(
        self,
        payload: models.ContactSyncRequest | dict[str, Any],
    ) -> models.ContactSyncResponse:
        return self._client._request(
            "POST",
            "/api/v1/contacts/sync",
            json_body=payload,
            response_model=models.ContactSyncResponse,
        )

    def sync_status(self) -> list[models.ContactSyncStatusResponse]:
        return self._client._request(
            "GET",
            "/api/v1/contacts/sync/status",
            response_model=list[models.ContactSyncStatusResponse],
        )

    def sync_history(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> models.ContactSyncHistoryResponse:
        return self._client._request(
            "GET",
            "/api/v1/contacts/sync/history",
            params={"limit": limit, "offset": offset},
            response_model=models.ContactSyncHistoryResponse,
        )

    def import_template(self) -> dict[str, Any]:
        return self._client._request(
            "GET",
            "/api/v1/contacts/import/template",
            response_model=dict[str, Any],
        )

    def get(self, contact_id: str) -> models.ContactResponse:
        return self._client._request(
            "GET",
            f"/api/v1/contacts/{contact_id}",
            response_model=models.ContactResponse,
        )

    def update(
        self,
        contact_id: str,
        payload: models.ContactUpdateRequest | dict[str, Any],
    ) -> models.ContactResponse:
        return self._client._request(
            "PATCH",
            f"/api/v1/contacts/{contact_id}",
            json_body=payload,
            response_model=models.ContactResponse,
        )

    def delete(self, contact_id: str) -> None:
        self._client._request("DELETE", f"/api/v1/contacts/{contact_id}")
        return None


__all__ = ["ContactsResource"]
