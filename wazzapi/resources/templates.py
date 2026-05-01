from __future__ import annotations

from typing import Any

from .. import models
from .base import BaseResource


class TemplatesResource(BaseResource):
    def builtin_variables(self) -> models.BuiltinVariablesResponse:
        return self._client._request(
            "GET",
            "/api/v1/templates/builtin-variables",
            response_model=models.BuiltinVariablesResponse,
        )

    def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        category: str | None = None,
        search: str | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
    ) -> models.TemplateListResponse:
        return self._client._request(
            "GET",
            "/api/v1/templates",
            params={
                "limit": limit,
                "offset": offset,
                "category": category,
                "search": search,
                "sort_by": sort_by,
                "sort_order": sort_order,
            },
            response_model=models.TemplateListResponse,
        )

    def create(
        self,
        payload: models.TemplateCreateRequest | dict[str, Any],
    ) -> models.TemplateResponse:
        return self._client._request(
            "POST",
            "/api/v1/templates",
            json_body=payload,
            response_model=models.TemplateResponse,
        )

    def get(self, template_id: str) -> models.TemplateResponse:
        return self._client._request(
            "GET",
            f"/api/v1/templates/{template_id}",
            response_model=models.TemplateResponse,
        )

    def update(
        self,
        template_id: str,
        payload: models.TemplateUpdateRequest | dict[str, Any],
    ) -> models.TemplateResponse:
        return self._client._request(
            "PATCH",
            f"/api/v1/templates/{template_id}",
            json_body=payload,
            response_model=models.TemplateResponse,
        )

    def delete(self, template_id: str) -> None:
        self._client._request("DELETE", f"/api/v1/templates/{template_id}")
        return None

    def preview(
        self,
        payload: models.TemplatePreviewRequest | dict[str, Any],
    ) -> models.TemplatePreviewResponse:
        return self._client._request(
            "POST",
            "/api/v1/templates/preview",
            json_body=payload,
            response_model=models.TemplatePreviewResponse,
        )


__all__ = ["TemplatesResource"]
