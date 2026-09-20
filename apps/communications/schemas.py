from uuid import UUID
from datetime import datetime
from typing import Optional, Any, Dict
from pydantic import BaseModel, ConfigDict
from apps.auth.schemas import UserRead


class ChatRoomCreateSchema(BaseModel):
    course_id: UUID
    name: str


class ChatRoomResponseSchema(BaseModel):
    id: UUID
    course_id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)


class MessageResponseSchema(BaseModel):
    id: UUID
    room_id: UUID
    sender: UserRead
    content: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


# --- WebSocket Frame Schemas ---
class WSSendMessageSchema(BaseModel):
    room_id: UUID
    content: str


class WSMessageBroadcastSchema(BaseModel):
    id: UUID
    room_id: UUID
    sender_id: UUID
    sender_username: str
    content: str
    timestamp: datetime


class WSTypingIndicatorSchema(BaseModel):
    room_id: UUID
    is_typing: bool


class WSNotificationEventSchema(BaseModel):
    event_type: str
    title: str
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime