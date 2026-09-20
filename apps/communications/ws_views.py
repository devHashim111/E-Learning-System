from fapix.viewsets.websocket import WebSocketApiView, WebSocketModelViewSet, BroadcastScope
from apps.auth.permissions import IsAuthenticated
from .models import ChatRoom, Message
from .schemas import ChatRoomResponseSchema, WSSendMessageSchema, WSTypingIndicatorSchema


class ChatRoomWebSocketViewSet(WebSocketModelViewSet):
    model = ChatRoom
    schema = ChatRoomResponseSchema
    auto_broadcast = True
    broadcast_self = True
    broadcast_scope = BroadcastScope.GLOBAL


class LiveChatWebSocketView(WebSocketApiView):
    action_schemas = {
        "send_message": WSSendMessageSchema,
        "typing_indicator": WSTypingIndicatorSchema,
    }
    permission_classes = [IsAuthenticated]
    auto_broadcast = False
    broadcast_scope = BroadcastScope.GLOBAL

    async def action_send_message(self, payload: dict, params: dict = None):
        # FIX: Use self.ws instead of self.websocket
        user = getattr(self.ws.state, "user", None)
        room_id = payload.get("room_id")
        content = payload.get("content")

        message_obj = await Message.create(
            room_id=room_id,
            sender_id=user.id,
            content=content,
        )

        outbound_data = {
            "id": str(message_obj.id),
            "room_id": str(room_id),
            "sender_id": str(user.id),
            "sender_username": getattr(user, "username", None) or user.email,
            "content": content,
            "timestamp": message_obj.timestamp.isoformat(),
        }

        await self.manager.broadcast(
            message={"action": "new_message", "status": "success", "data": outbound_data},
            scope=self.broadcast_scope,
        )
        return outbound_data

    async def action_typing_indicator(self, payload: dict, params: dict = None):
        # FIX: Use self.ws instead of self.websocket
        user = getattr(self.ws.state, "user", None)
        outbound_data = {
            "room_id": payload.get("room_id"),
            "user_id": str(user.id),
            "username": getattr(user, "username", None) or user.email,
            "is_typing": payload.get("is_typing", False),
        }
        await self.manager.broadcast(
            message={"action": "user_typing", "status": "success", "data": outbound_data},
            scope=self.broadcast_scope,
        )
        return outbound_data