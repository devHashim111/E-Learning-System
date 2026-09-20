import uuid
from tortoise import fields, models


class ChatRoom(models.Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    course = fields.OneToOneField("models.Course", related_name="chat_room")
    name = fields.CharField(max_length=255)

    class Meta:
        table = "chat_rooms"


class Message(models.Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    room = fields.ForeignKeyField("models.ChatRoom", related_name="messages")
    sender = fields.ForeignKeyField("models.User", related_name="sent_messages")
    content = fields.TextField()
    timestamp = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "chat_messages"
        ordering = ["-timestamp"]