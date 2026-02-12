from utilities.websocket import AsyncWebsocketActionConsumer
from utilities.payload import Payload
from utilities.chat_helper import get_chat_recipients, get_chat_message_recipients
from asgiref.sync import sync_to_async
from .models import PropertyChat, PropertyChatMessage, Property
from .utility import build_request_from_scope
from .serializers import PropertyChatSerializer, PropertyChatMessageSerializer


consumer = AsyncWebsocketActionConsumer()


@consumer.action(name="$connect")
async def connect(self: AsyncWebsocketActionConsumer, payload: Payload | None):
    print("Connect from action")
    user = self.scope["user"]
    if user.is_authenticated:
        await self.accept()
        await self.channel_layer.group_add(user.id, self.channel_name)
    else:
        await self.close(reason="Unauthorized")


@consumer.action(name="$disconnect")
async def disconnect(self: AsyncWebsocketActionConsumer, close_code: int):
    pass


@consumer.action
async def greetings(self: AsyncWebsocketActionConsumer, payload: Payload):
    payload.data = {"message": "Hello"}
    await self.send_payload(payload)


@consumer.action
async def create_chat(self: AsyncWebsocketActionConsumer, payload: Payload):
    def process():
        property_id = payload.data.get("property_id")
        if not property_id:
            return Payload.error("Property ID is required")
        print("Property ids: ", Property.objects.all().values_list("id", flat=True))
        if not Property.objects.filter(id=property_id).exists():
            return Payload.error("Property not found")

        client_id = self.scope["user"].id
        request = build_request_from_scope(self.scope)
        chat, created = PropertyChat.objects.get_or_create(
            property_id=property_id,
            client_id=client_id,
        )
        if created:
            PropertyChatMessage.objects.create(
                chat=chat,
                sender_id=client_id,
                message="Hello, I am interested in this property.",
            )
        serializer = PropertyChatSerializer(chat, context={"request": request})
        payload.data = {"chat": serializer.data, "created": created}
        return payload, get_chat_recipients(chat.id)

    payload, recipients = await sync_to_async(process)()
    for recipient in recipients:
        print("Sending to: ", recipient)
        await self.send_group_payload(payload, recipient)


@consumer.action
async def get_chats(self: AsyncWebsocketActionConsumer, payload: Payload):
    def process():
        request = build_request_from_scope(self.scope)
        client_id = self.scope["user"].id
        chats = PropertyChat.objects.filter(client_id=client_id)
        serializer = PropertyChatSerializer(
            chats, many=True, context={"request": request}
        )
        payload.data = {"chats": serializer.data}
        return payload

    response_payload = await sync_to_async(process)()
    await self.send_payload(response_payload)


@consumer.action
async def create_chat_message(self: AsyncWebsocketActionConsumer, payload):
    def process():
        sender_id = self.scope["user"].id
        serializer = PropertyChatMessageSerializer(data=payload.data)
        if serializer.is_valid():
            serializer.save(sender_id=sender_id)
            payload.data = serializer.data
            return payload, get_chat_message_recipients(payload.data["id"])
        return Payload.error(serializer.errors), []

    response_payload, recipients = await sync_to_async(process)()
    if response_payload.is_error:
        await self.send_payload(response_payload)
    else:
        for recipient in recipients:
            await self.send_group_payload(response_payload, recipient)
