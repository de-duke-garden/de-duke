from constructs import Construct
from typing import TypedDict

from ..shared.main import Shared
from .landing import Landing


class UserInterfaceConfig(TypedDict):
    shared: Shared


class UserInterface(Construct):
    def __init__(self, scope: Construct, id: str, config: UserInterfaceConfig) -> None:
        super().__init__(scope, id)

        landing = Landing(
            self, "Landing",
            config={
                "shared": config["shared"],
            }
        )
