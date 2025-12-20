from constructs import Construct
from typing import TypedDict
from pathlib import Path

from ..shared.main import Shared
# from ..authentications.main import Authentications
from ..databases.main import Databases
from .drf_api import DrfApi

class ApiConfig(TypedDict):
    shared: Shared
    # authentications: Authentications
    databases: Databases


class Api(Construct):
    def __init__(self, scope: Construct, id: str, config: ApiConfig) -> None:
        super().__init__(scope, id)

        self.drf_api = DrfApi(
            self, "DrfApi",
            config=config
        )