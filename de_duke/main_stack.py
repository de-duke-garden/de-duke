from aws_cdk import (
    Stack,
)
from constructs import Construct

from .shared.main import Shared
from .apis.main import Api
from .databases.main import Databases
from typing import TypedDict
from .agents.main import Agents
from .user_interfaces.main import UserInterface


class MainStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        shared = Shared(
            self, "SharedResources",
        )
        databases = Databases(
            self, "Databases",
            config={
                "shared": shared,
            }
        )
        agents = Agents(
            self, "Agents",
            config={
                "shared": shared,
            }
        )
        api = Api(
            self, "Apis",
            config={
                "shared": shared,
                "databases": databases,
                "agents": agents,
            }
        )
        user_interface = UserInterface(
            self, "UserInterface",
            config={
                "shared": shared,
                "api": api,
            }
        )
