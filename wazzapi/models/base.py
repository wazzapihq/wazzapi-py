from pydantic import BaseModel, ConfigDict


class WazzapiModel(BaseModel):
    """Base model for SDK request and response payloads."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)


__all__ = ["WazzapiModel"]
