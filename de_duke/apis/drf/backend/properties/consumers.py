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
        property_ = payload.data.get("property")
        if not property_:
            return Payload.error("Property is required")

        try:
            property_instance = Property.objects.get(id=property_)
        except Property.DoesNotExist:
            return Payload.error("Property not found")

        # Validate property
        if not property_instance.is_verified():
            return Payload.error("Property is not verified")
        if not property_instance.is_active:
            return Payload.error("Property is not active")
        if property_instance.is_banned():
            return Payload.error("Property is banned")

        client = self.scope["user"]

        # Get or create chat
        chat, created = PropertyChat.objects.get_or_create(
            property=property_instance,
            client=client,
        )

        if created:
            PropertyChatMessage.objects.create(
                chat=chat,
                sender=client,
                message="Hello, I am interested in this property.",
            )

        request = build_request_from_scope(self.scope)
        serializer = PropertyChatSerializer(chat, context={"request": request})
        payload.data = serializer.data
        return payload, get_chat_recipients(chat.id)

    payload, recipients = await sync_to_async(process)()
    for recipient in recipients:
        # print("Sending to: ", recipient)
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
        sender = self.scope["user"]
        serializer = PropertyChatMessageSerializer(data=payload.data)
        if serializer.is_valid():
            serializer.save(sender=sender)
            payload.data = serializer.data
            return payload, get_chat_message_recipients(payload.data["id"])
        return Payload.error(serializer.errors), []

    response_payload, recipients = await sync_to_async(process)()
    if response_payload.is_error:
        await self.send_payload(response_payload)
    else:
        for recipient in recipients:
            await self.send_group_payload(response_payload, recipient)
