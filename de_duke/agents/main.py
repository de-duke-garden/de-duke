from aws_cdk import (
    aws_bedrock as bedrock,
    aws_iam as iam,
)
from constructs import Construct
from typing import TypedDict
from pathlib import Path

from ..shared.main import Shared


class AgentsConfig(TypedDict):
    shared: Shared


class Agents(Construct):
    def __init__(self, scope: Construct, id: str, config: AgentsConfig) -> None:
        super().__init__(scope, id)

        self.embedding_model = bedrock.FoundationModel.from_foundation_model_id(
            self, "EmbeddingModel",
            foundation_model_id=bedrock.FoundationModelIdentifier.AMAZON_TITAN_EMBED_TEXT_V2_0
        )

        self.env_vars = {
            "EMBEDDING_MODEL_ID": self.embedding_model.model_id,
        }

    def grant_access(self, grantee: iam.IRole) -> None:
        grantee.add_to_principal_policy(iam.PolicyStatement(
            actions=["bedrock:InvokeModel"],
            resources=[self.embedding_model.model_arn],
        ))
