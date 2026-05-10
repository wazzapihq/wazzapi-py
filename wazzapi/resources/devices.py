from __future__ import annotations

from .. import models
from .base import BaseResource


class DevicesResource(BaseResource):
    def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        status: str | None = None,
        search: str | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
    ) -> models.DeviceListResponse:
        return self._client._request(
            "GET",
            "/api/v1/devices",
            params={
                "limit": limit,
                "offset": offset,
                "status": status,
                "search": search,
                "sort_by": sort_by,
                "sort_order": sort_order,
            },
            response_model=models.DeviceListResponse,
        )

    def get(self, device_id: str) -> models.DeviceResponse:
        return self._client._request(
            "GET",
            f"/api/v1/devices/{device_id}",
            response_model=models.DeviceResponse,
        )


__all__ = ["DevicesResource"]