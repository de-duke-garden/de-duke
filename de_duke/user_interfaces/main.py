from constructs import Construct
from typing import TypedDict

from ..shared.main import Shared
from .website import Website


class UserInterfaceConfig(TypedDict):
    shared: Shared


class UserInterface(Construct):
    def __init__(self, scope: Construct, id: str, config: UserInterfaceConfig) -> None:
        super().__init__(scope, id)

        website = Website(
            self, "Website",
            config={
                "shared": config["shared"],
            }
        )
