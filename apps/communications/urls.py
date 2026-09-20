from fastapi import APIRouter, WebSocket
from fapix.router import DefaultRouter
from fapix.core.router import register_urlpatterns
from .views import ChatRoomViewSet, MessageViewSet
from .ws_views import ChatRoomWebSocketViewSet, LiveChatWebSocketView

router = APIRouter(prefix="/communications", tags=["Communications & Real-time Chat"])

# 1. HTTP REST Router
comm_router = DefaultRouter()
comm_router.register("rooms", ChatRoomViewSet, basename="chatroom")
comm_router.register("messages", MessageViewSet, basename="message")

urlpatterns = comm_router.generate_urlpatterns()
register_urlpatterns(router, urlpatterns)

# 2. WebSocket Endpoints
@router.websocket("/ws/rooms/")
async def chat_rooms_ws_endpoint(websocket: WebSocket):
    await ChatRoomWebSocketViewSet.handle_connection(websocket)

@router.websocket("/ws/chat/")
async def live_chat_ws_endpoint(websocket: WebSocket):
    await LiveChatWebSocketView.handle_connection(websocket)