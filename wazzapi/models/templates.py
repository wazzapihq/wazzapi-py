from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from .base import WazzapiModel


class BuiltinVariableInfo(WazzapiModel):
    name: str
    description: str
    example: str


class BuiltinVariablesResponse(WazzapiModel):
    variables: list[BuiltinVariableInfo]


class TemplateCreateRequest(WazzapiModel):
    name: str
    content: str
    category: str = "marketing"
    media_type: str | None = None
    media_url: str | None = None


class TemplateItem(WazzapiModel):
    id: str
    name: str
    category: str
    content: str
    variables: list[str] = Field(default_factory=list)
    builtin_variables: list[str] = Field(default_factory=list)
    custom_variables: list[str] = Field(default_factory=list)
    media_type: str | None = None
    media_url: str | None = None
    times_used: int
    last_used_at: datetime | None = None
    created_at: datetime


class TemplateListResponse(WazzapiModel):
    data: list[TemplateItem]
    pagination: dict[str, Any]


class TemplatePreviewRequest(WazzapiModel):
    content: str | None = None
    template_id: str | None = None
    custom_variables: dict[str, Any] | None = None
    contact_id: str | None = None


class TemplatePreviewResponse(WazzapiModel):
    preview: str
    all_variables: list[str] = Field(default_factory=list)
    builtin_variables: list[str] = Field(default_factory=list)
    custom_variables: list[str] = Field(default_factory=list)
    missing_variables: list[str] = Field(default_factory=list)


class TemplateResponse(WazzapiModel):
    id: str
    name: str
    category: str
    content: str
    variables: list[str] = Field(default_factory=list)
    builtin_variables: list[str] = Field(default_factory=list)
    custom_variables: list[str] = Field(default_factory=list)
    media_type: str | None = None
    media_url: str | None = None
    is_active: bool
    times_used: int
    last_used_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class TemplateUpdateRequest(WazzapiModel):
    name: str | None = None
    content: str | None = None
    category: str | None = None
    is_active: bool | None = None
    media_type: str | None = None
    media_url: str | None = None


__all__ = [
    "BuiltinVariableInfo",
    "BuiltinVariablesResponse",
    "TemplateCreateRequest",
    "TemplateItem",
    "TemplateListResponse",
    "TemplatePreviewRequest",
    "TemplatePreviewResponse",
    "TemplateResponse",
    "TemplateUpdateRequest",
]
