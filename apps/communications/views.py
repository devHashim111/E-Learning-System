from fapix.views import ModelViewSet
from apps.auth.permissions import IsAuthenticated, IsSuperUserOrRole
from .models import ChatRoom, Message
from .schemas import (
    ChatRoomResponseSchema,
    ChatRoomCreateSchema,
    MessageResponseSchema,
)


class ChatRoomViewSet(ModelViewSet):
    model = ChatRoom
    schema = ChatRoomResponseSchema
    action_schemas = {"create": ChatRoomCreateSchema}

    permission_classes = [IsAuthenticated]
    action_permissions = {
        "create": [IsSuperUserOrRole("admin", "teacher")],
        "destroy": [IsSuperUserOrRole("admin")],
    }

    filterset_fields = ["course_id"]


class MessageViewSet(ModelViewSet):
    model = Message
    schema = MessageResponseSchema

    permission_classes = [IsAuthenticated]
    filterset_fields = ["room_id", "sender_id"]
    ordering_fields = ["timestamp"]
    default_ordering = ["-timestamp"]