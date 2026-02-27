from utilities.websocket import AsyncWebsocketActionConsumer
from utilities.payload import Payload
from utilities.chat_helper import (
    get_recipients_by_chat_id,
    get_recipients_by_chat_message_id,
)
from asgiref.sync import sync_to_async
from .models import PropertyChat, PropertyChatMessage, Property
from .utility import build_request_from_scope
from .serializers import PropertyChatSerializer, PropertyChatMessageSerializer
from payments.models import PropertyChatInvoice
from payments.serializers import (
    PropertyChatInvoiceCreateSerializer,
    PropertyChatInvoiceEditSerializer,
    PropertyChatInvoiceSealSerializer,
    PropertyChatInvoiceSerializer,
)
from payments.utility import create_property_chat_invoice_paystack_payment_link
from django.db.models import Q

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
async def ping(self: AsyncWebsocketActionConsumer, payload: Payload):
    payload.data = {"message": "pong"}
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
        return payload, get_recipients_by_chat_id(chat.id)

    payload, recipients = await sync_to_async(process)()
    for recipient in recipients:
        # print("Sending to: ", recipient)
        await self.send_group_payload(payload, recipient)


@consumer.action
async def get_chats(self: AsyncWebsocketActionConsumer, payload: Payload):
    def process():
        request = build_request_from_scope(self.scope)
        user = self.scope["user"]
        # return all chats for superuser and filtered chats for others
        if user.is_superuser:
            chats = PropertyChat.objects.all()
        else:
            chats = PropertyChat.objects.filter(
                Q(client=user) | Q(property__listed_by__user=user)
            )
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
            return payload, get_recipients_by_chat_message_id(payload.data["id"])
        return Payload.error(serializer.errors), []

    response_payload, recipients = await sync_to_async(process)()
    if response_payload.is_error:
        await self.send_payload(response_payload)
    else:
        for recipient in recipients:
            await self.send_group_payload(response_payload, recipient)


@consumer.action
async def allow_payment(self: AsyncWebsocketActionConsumer, payload: Payload):
    def process():
        property_chat_id = payload.data.get("property_chat")
        if not property_chat_id:
            return Payload.error("Property chat is required"), []
        try:
            print("Property chat id: ", property_chat_id)
            property_chat = PropertyChat.objects.get(id=property_chat_id)
            if property_chat.host != self.scope["user"]:
                print("You are not allowed to allow payment")
                return Payload.error("You are not allowed to allow payment"), []
        except PropertyChat.DoesNotExist:
            print("Property chat not found")
            return Payload.error("Property chat not found"), []
        property_chat.allow_payment = payload.data.get("allow_payment")
        property_chat.save()
        payload.data = {
            "property_chat": property_chat.id,
            "allow_payment": property_chat.allow_payment,
        }
        print("Payload data: ", payload.data)
        return payload, get_recipients_by_chat_id(property_chat.id)

    response_payload, recipients = await sync_to_async(process)()
    if response_payload.is_error:
        await self.send_payload(response_payload)
    else:
        for recipient in recipients:
            await self.send_group_payload(response_payload, recipient)


@consumer.action
async def create_invoice(self: AsyncWebsocketActionConsumer, payload):
    def process():
        serializer = PropertyChatInvoiceCreateSerializer(data=payload.data)
        if serializer.is_valid():
            property_chat = serializer.validated_data["property_chat"]
            if property_chat.client != self.scope["user"]:
                return Payload.error("You are not allowed to create an invoice"), []
            # if not property_chat.property.is_open_for_invoice:
            #     return Payload.error("Property is not open for invoice"), []
            # Decending order: last created invoice
            last_invoice = property_chat.property_chat_invoices.first()
            if last_invoice and last_invoice.status == "initiated":
                return Payload.error(
                    "There is an existing intiated invoice, please proceed with that one."
                ), []
            serializer.save(
                unit_amount=property_chat.property.unit_amount,
                payment_gateway="paystack",
            )
            payload.data = PropertyChatInvoiceSerializer(serializer.instance).data
            return payload, get_recipients_by_chat_id(property_chat.id)
        return Payload.error(serializer.errors), []

    response_payload, recipients = await sync_to_async(process)()
    if response_payload.is_error:
        await self.send_payload(response_payload)
    else:
        for recipient in recipients:
            await self.send_group_payload(response_payload, recipient)


@consumer.action
async def edit_invoice(self: AsyncWebsocketActionConsumer, payload):
    def process():
        inst = PropertyChatInvoice.objects.get(id=payload.data.get("id"))
        serializer = PropertyChatInvoiceEditSerializer(
            instance=inst, data=payload.data, partial=True
        )
        if serializer.is_valid():
            property_chat = serializer.instance.property_chat
            if property_chat.client != self.scope["user"]:
                return Payload.error("You are not allowed to edit the invoice"), []
            serializer.save()
            payload.data = PropertyChatInvoiceSerializer(serializer.instance).data
            return payload, get_recipients_by_chat_id(property_chat.id)
        return Payload.error(serializer.errors), []

    response_payload, recipients = await sync_to_async(process)()
    if response_payload.is_error:
        await self.send_payload(response_payload)
    else:
        for recipient in recipients:
            await self.send_group_payload(response_payload, recipient)


@consumer.action
async def seal_invoice(self: AsyncWebsocketActionConsumer, payload):
    def process():
        instance = PropertyChatInvoice.objects.get(id=payload.data.get("id"))
        serializer = PropertyChatInvoiceSealSerializer(instance, data=payload.data)
        if serializer.is_valid():
            print("Serializer is valid")
            property_chat = serializer.instance.property_chat
            if property_chat.host != self.scope["user"]:
                return Payload.error("You are not allowed to seal an invoice"), []
            # if not property_chat.property.is_open_for_invoice:
            #     return Payload.error("Property is not open for invoice"), []
            serializer.save()
            payload.data = PropertyChatInvoiceSerializer(serializer.instance).data
            return payload, get_recipients_by_chat_id(property_chat.id)
        return Payload.error(serializer.errors), []

    response_payload, recipients = await sync_to_async(process)()
    if response_payload.is_error:
        await self.send_payload(response_payload)
    else:
        for recipient in recipients:
            await self.send_group_payload(response_payload, recipient)


@consumer.action
async def pay_invoice(self: AsyncWebsocketActionConsumer, payload):
    def process():
        instance = PropertyChatInvoice.objects.get(id=payload.data.get("id"))
        if not instance.is_sealed:
            return Payload.error(
                "Invoice is not sealed. Please contact the host to seal the invoice."
            )
        if instance.status != "initiated":
            return Payload.error("Invoice is already processed")
        payment_link = create_property_chat_invoice_paystack_payment_link(instance)
        payload.data = {"payment_link": payment_link}
        # return payload, get_recipients_by_chat_id(instance.property_chat.id)
        return payload

    response_payload = await sync_to_async(process)()
    await self.send_payload(response_payload)
