import json
import uuid
from decimal import Decimal
from typing import Any


class JSONv2Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


class Payload:
    def __init__(self, action: str, data: Any):
        self.action = action
        self.data = data

    @classmethod
    def from_json(cls, payload: str) -> "Payload":
        payload_data = json.loads(payload)
        return cls(payload_data["action"], payload_data.get("data"))

    @classmethod
    def error(cls, message: str) -> "Payload":
        return cls("$error", message)

    def to_json(self):
        return json.dumps(self.__dict__, cls=JSONv2Encoder)

    @property
    def is_error(self) -> bool:
        return self.action == "$error"
