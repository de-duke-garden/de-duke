from aws_cdk import (
    aws_ec2 as ec2,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_s3_assets as s3_assets,
    aws_autoscaling as autoscaling,
    aws_secretsmanager as secretsmanager,
    aws_elasticloadbalancingv2 as elbv2,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
    Aws,
    Duration,
    CfnOutput,
)
from constructs import Construct
from typing import TypedDict
from pathlib import Path
from ..databases.main import Databases
from ..shared.main import Shared
from ..agents.main import Agents
import json


class DrfApiConfig(TypedDict):
    shared: Shared
    databases: Databases
    # authentications: Authentications
    agents: Agents


class DrfApi(Construct):
    def __init__(self, scope: Construct, id: str, config: DrfApiConfig) -> None:
        super().__init__(scope, id)

        # Define application code as an s3 asset
        app_asset = s3_assets.Asset(
            self, "AppAsset",
            path=str(Path(__file__).parent / "drf"),
            exclude=[
                "**/mediafiles",
                "**/staticfiles",
                "**/venv",
                "**/.secrets"
            ]
        )
        secret = secretsmanager.Secret(
            self, "DRFSecret",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template=json.dumps({}),
                generate_string_key="secretkey",
                exclude_characters="!@#$%^&*()_+"
            )
        )

        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            "sudo yum update -y",
            "sudo yum install -y docker",
            "sudo yum install -y make",
            "sudo mkdir -p /usr/libexec/docker/cli-plugins",
            "sudo curl -SL https://github.com/docker/compose/releases/download/v2.39.4/docker-compose-$(uname -s)-$(uname -m) -o /usr/libexec/docker/cli-plugins/docker-compose",
            "sudo chmod +x /usr/libexec/docker/cli-plugins/docker-compose",
            "sudo service docker start",
            "sudo usermod -aG docker $USER",
            # Download the application code from S3
            f"aws s3 cp {app_asset.s3_object_url} /tmp/app.zip",
            "unzip /tmp/app.zip -d /opt/app && rm /tmp/app.zip",
            "cd /opt/app",
            # Save environment variables into ./backend/.env.aws file
            f"""
cat <<EOF > ./backend/.env.aws
SECRET_KEY_ARN={secret.secret_arn}
CPLUS_INCLUDE_PATH=/usr/include/gdal
C_INCLUDE_PATH=/usr/include/gdal
GDAL_LIBRARY_PATH=/usr/lib/libgdal.so
DJANGO_SETTINGS_MODULE=main.settings.aws
{"\n".join([f"{key}={value}" for key,
                value in config['shared'].default_env_vars.items()])}
{"\n".join([f"{key}={value}" for key,
                    value in config['databases'].env_vars.items()])}
{"\n".join([f"{key}={value}" for key,
                        value in config['agents'].env_vars.items()])}
EOF
            """,
            # "sudo docker compose -f compose.aws.yaml up -d",
            "sudo make prod-start"
        )

        asg = autoscaling.AutoScalingGroup(
            self, "AutoScalingGroup",
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.T3,
                ec2.InstanceSize.MICRO,
            ),
            vpc=config['shared'].vpc,
            machine_image=ec2.MachineImage.latest_amazon_linux2023(),
            update_policy=autoscaling.UpdatePolicy.replacing_update(),
            user_data=user_data,
            min_capacity=1,
            max_capacity=2,
            desired_capacity=1,
        )

        asg.connections.allow_from_any_ipv4(
            ec2.Port.tcp(22), "Allow SSH Access")
        asg.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80), "Allow HTTP Access")
        secret.grant_read(asg)
        config['shared'].email_secret.grant_read(asg)
        config['shared'].gcp_secret.grant_read(asg)
        app_asset.grant_read(asg)
        config['databases'].grant_connect(asg)
        config['agents'].grant_access(asg.role)

        lb = elbv2.ApplicationLoadBalancer(
            self, "LoadBalancer",
            vpc=config['shared'].vpc,
            internet_facing=True,
        )

        route53.ARecord(
            self, "ApiARecord",
            zone=config['shared'].hosted_zone,
            record_name="api",
            target=route53.RecordTarget.from_alias(
                route53_targets.LoadBalancerTarget(lb)),
        )

        listener_80 = lb.add_listener(
            "Listener80",
            port=80
        )
        listener_80.add_targets(
            "TargetGroup80",
            port=80,
            targets=[asg]
        )

        listener_443 = lb.add_listener(
            "Listener443",
            port=443,
            certificates=[
                elbv2.ListenerCertificate.from_arn(
                    config['shared'].certificate.certificate_arn)
            ]
        )
        listener_443.add_targets(
            "TargetGroup443",
            port=80, # SSL termination at the load balancer
            targets=[asg]
        )

        CfnOutput(self, "AutoScalingGroupName",
                  value=asg.auto_scaling_group_name)
