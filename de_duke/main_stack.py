from aws_cdk import (
    Stack,
)
from constructs import Construct

from .shared.main import Shared
# from .user_interface.main import UserInterface
from .apis.main import Api
from .databases.main import Databases
from .stage import StageConfig
from typing import TypedDict
from .agents.main import Agents


class MainStackConfig(TypedDict):
    stage: StageConfig


class MainStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, stage: StageConfig, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        shared = Shared(
            self, "SharedResources",
            config={"stage": stage}
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
        # user_interface = UserInterface(
        #     self, "UserInterface",
        #     config={
        #         "shared": shared,
        #         "api": api,
        #     }
        # )
