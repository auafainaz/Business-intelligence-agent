from typing import Any

from pydantic import BaseModel, Field


class RealtimeToolDefinition(BaseModel):
    type: str = "function"
    name: str
    description: str
    parameters: dict[str, Any] = Field(default_factory=dict)


class RealtimeSessionConfig(BaseModel):
    provider: str = "xai"
    model: str
    voice: str
    instructions: str
    tools: list[dict[str, Any]]
    metadata: dict[str, Any] = Field(default_factory=dict)
