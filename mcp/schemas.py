from datetime import datetime
from typing import Any

from pydantic import BaseModel as PydanticBase


class BaseModel(PydanticBase):
    pass


class MessageCreate(BaseModel):
    role: str
    content: str
    metadata: dict[str, Any] | None = None


class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    created_at: datetime
    metadata: dict[str, Any] | None = None


class ConversationCreate(BaseModel):
    user_id: str
    title: str | None = None


class ConversationResponse(BaseModel):
    id: int
    user_id: str
    title: str | None
    created_at: datetime
    updated_at: datetime
    is_active: bool
