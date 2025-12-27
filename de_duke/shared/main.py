from aws_cdk import (
    aws_ec2 as ec2,
    aws_lambda as _lambda,
    aws_secretsmanager as secretsmanager,
    aws_route53 as route53,
    aws_certificatemanager as acm,
    Aws,
    RemovalPolicy
)
from constructs import Construct
from ..layer import Layer, LayerConfig
from typing import TypedDict
from pathlib import Path
from ..stage import StageConfig
import json


class SharedConfig(TypedDict):
    stage: StageConfig


class Shared(Construct):
    def __init__(self, scope: Construct, id: str, config: SharedConfig) -> None:
        super().__init__(scope, id)

        self.email_secret = secretsmanager.Secret.from_secret_name_v2(
            self, "EmailSecret",
            secret_name="Email"
        )
        self.google_map_secret = secretsmanager.Secret.from_secret_name_v2(
            self, "GoogleMapSecret",
            secret_name="GoogleMap"
        )

        self.default_env_vars = {
            "LOG_LEVEL": "INFO",
            "POWERTOOLS_DEV": "true",
            "POWERTOOLS_TRACE_DISABLED": "true",
            "POWERTOOLS_LOGGER_LOG_EVENT": "true",
            "POWERTOOLS_SERVICE_NAME": f"{Aws.STACK_NAME}-service-{config['stage']['name']}",
            "EMAIL_SECRET_ARN": self.email_secret.secret_arn,
            "GOOGLE_MAP_SECRET_ARN": self.google_map_secret.secret_arn,
            "AWS_REGION": Aws.REGION,
        }
        self.removal_policy = RemovalPolicy.DESTROY
        self.vpc = ec2.Vpc.from_lookup(
            self, "DefaultVPC",
            is_default=True
        )
        self.vpc.add_gateway_endpoint(
            "S3GatewayEndpoint",
            service=ec2.GatewayVpcEndpointAwsService.S3
        )
        self.stage = config['stage']
        self.powertools_layer = _lambda.LayerVersion.from_layer_version_arn(
            self, "PowertoolsLayer",
            layer_version_arn=f"arn:{Aws.PARTITION}:lambda:{Aws.REGION}:017000801446:layer:AWSLambdaPowertoolsPythonV3-python312-x86_64:18"
        )
        self.common_layer = Layer(
            self, "CommonLayer",
            config=LayerConfig(
                runtime=_lambda.Runtime.PYTHON_3_12,
                architecture=_lambda.Architecture.X86_64,
                path=str(Path(__file__).parent.joinpath(
                    "layers/common").resolve()),
                auto_upgrade=True,
                layer_type="txt",
                stage=config['stage']
            )
        ).layer
        self.internal_layer = Layer(
            self, "InternalLayer",
            config=LayerConfig(
                runtime=_lambda.Runtime.PYTHON_3_12,
                architecture=_lambda.Architecture.X86_64,
                path=str(Path(__file__).parent.joinpath(
                    "layers/python_sdk/internal").resolve()),
                auto_upgrade=True,
                layer_type="toml",
                stage=config['stage']
            )
        ).layer

        self.hosted_zone = route53.HostedZone.from_lookup(
            self, "HostedZone",
            domain_name="de-duke.com"
        )

        self.certificate = acm.Certificate(
            self, "Certificate",
            domain_name="de-duke.com",
            subject_alternative_names=["*.de-duke.com"],
            allow_export=False,
            validation=acm.CertificateValidation.from_dns(self.hosted_zone)
        )
