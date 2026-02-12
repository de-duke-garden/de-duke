from channels.generic.websocket import AsyncWebsocketConsumer
import json

from .payload import Payload
from functools import partial
from typing import Callable, Any


class AsyncWebsocketActionConsumer(AsyncWebsocketConsumer):
    """
    An asynchronous WebSocket consumer that routes incoming messages to specific action handlers.

    This class allows for registering and dispatching actions based on JSON payloads,
    providing a structured way to handle complex WebSocket communication.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure actions dict exists on the instance or class
        if not hasattr(self, "actions"):
            self.actions: dict[
                str,
                Callable[["AsyncWebsocketActionConsumer", Payload | int | None], Any],
            ] = {}

    async def connect(self):
        actions = getattr(self, "actions", {})
        if "$connect" in actions:
            await actions["$connect"](self, None)
        else:
            await super().connect()

    async def disconnect(self, close_code):
        actions = getattr(self, "actions", {})
        if "$disconnect" in actions:
            await actions["$disconnect"](self, close_code)
        else:
            await super().disconnect(close_code)

    async def send_payload(self, payload: Payload):
        await self.send(text_data=payload.to_json())

    async def send_group_payload(self, payload: Payload, room_group_name: str):
        await self.channel_layer.group_send(
            room_group_name,
            {
                "type": "group.payload.handler",
                "payload": payload.to_json(),
            },
        )

    async def group_payload_handler(self, event):
        payload = Payload.from_json(event["payload"])
        await self.send_payload(payload)

    async def receive(self, text_data):
        print("Actions: ", getattr(self, "actions", {}))
        try:
            payload = Payload.from_json(text_data)
        except json.JSONDecodeError:
            await self.send_payload(Payload.error("Invalid JSON format"))
            return

        actions = getattr(self, "actions", {})
        if payload.action in actions and not payload.action.startswith("$"):
            try:
                await actions[payload.action](self, payload)
            except Exception as e:
                await self.send_payload(Payload.error(str(e)))
        else:
            await self.send_payload(Payload.error("Invalid action"))

    def action(
        self,
        func: Callable[["AsyncWebsocketActionConsumer", Payload | int | None], Any]
        | None = None,
        *,
        name: str | None = None,
    ):
        print("Action registered: ", name, func)
        if func is None:
            return partial(self.action, name=name)

        func_name = name or func.__name__

        # Register on the class so it persists across instances created by as_asgi()
        cls = self.__class__
        if "actions" not in cls.__dict__:
            # If strictly class-level registration hasn't happened yet for this subclass
            cls.actions = {}

        cls.actions[func_name] = func
        return func
