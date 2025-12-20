from aws_cdk import (
    aws_ec2 as ec2,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_s3_assets as s3_assets,
    aws_autoscaling as autoscaling,
    aws_secretsmanager as secretsmanager,
    Aws,
    Duration,
    CfnOutput,
)
from constructs import Construct
from typing import TypedDict
from pathlib import Path
from ..stage import StageNameEnum
from ..databases.main import Databases
from ..shared.main import Shared
import json


class DrfApiConfig(TypedDict):
    shared: Shared
    databases: Databases
    # authentications: Authentications


class DrfApi(Construct):
    def __init__(self, scope: Construct, id: str, config: DrfApiConfig) -> None:
        super().__init__(scope, id)

        name = f"drf-{config['shared'].stage['name']}-{config['shared'].stage['version']}"

        # Define application code as an s3 asset
        app_asset = s3_assets.Asset(
            self, "AppAsset",
            path=str(Path(__file__).parent / "drf"),
            asset_hash=name
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
            "sudo apt update -y",
            "sudo apt install -y python3 python3-pip unzip curl",
            "curl \"https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip\" -o \"awscliv2.zip\"",
            "unzip awscliv2.zip",
            "sudo ./aws/install",
            "sudo apt install -y gdal-bin libgdal-dev",
            # Download the application code from S3
            f"aws s3 cp {app_asset.s3_object_url} /tmp/app.zip",
            "unzip /tmp/app.zip -d /opt/app && rm /tmp/app.zip",
            # Install dependencies
            "mkdir -p /opt/app/pip_tmp",
            "export TMPDIR=/opt/app/pip_tmp",
            # "pip3 install --no-cache-dir -r /opt/app/requirements.txt",
            "pip3 install --no-cache-dir --default-timeout=100 --retries 5 -r /opt/app/requirements.txt",
            "rm -rf /opt/app/pip_tmp",  # Clean up after installation
            # Set up systemd service
            f"""
            cat <<EOF > /etc/systemd/system/django.service
            [Unit]
            Description=Gunicorn instance to serve Django
            After=network.target

            [Service]
            User=root
            Group=root
            WorkingDirectory=/opt/app
            Environment="PATH=/usr/bin"
            Environment="SECRET_KEY_ARN={secret.secret_arn}"
            # ... add other env vars here ...
            Environment="CPLUS_INCLUDE_PATH=/usr/include/gdal"
            Environment="C_INCLUDE_PATH=/usr/include/gdal"
            Environment="GDAL_LIBRARY_PATH=/usr/lib/libgdal.so"
            Environment="DJANGO_SETTINGS_MODULE=main.settings.aws"
            {"\n".join([f"Environment=\"{key}={value}\"" for key,
                        value in config['shared'].default_env_vars.items()])}
            {"\n".join([f"Environment=\"{key}={value}\"" for key,
                            value in config['databases'].env_vars.items()])}
            # Run migrations
            ExecStartPre=/usr/bin/python3 /opt/app/manage.py migrate
            ExecStart=/usr/local/bin/gunicorn --workers 3 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 main.asgi:application

            [Install]
            WantedBy=multi-user.target
            EOF
            """,
            "sudo systemctl start django",
            "sudo systemctl enable django"
        )

        asg = autoscaling.AutoScalingGroup(
            self, "AutoScalingGroup",
            auto_scaling_group_name=name,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.T3,
                ec2.InstanceSize.MICRO,
            ),
            vpc=config['shared'].vpc,
            machine_image=ec2.MachineImage.generic_linux(
                ami_map={
                    "af-south-1": "ami-0942f36ad098582d6"
                }
            ),
            user_data=user_data,
            min_capacity=1,
            max_capacity=2,
            desired_capacity=1,
            # key_name="vanguard-key",
        )

        asg.connections.allow_from_any_ipv4(
            ec2.Port.tcp(22), "Allow SSH Access")

        secret.grant_read(asg)
        config['shared'].email_secret.grant_read(asg)
        config['shared'].google_map_secret.grant_read(asg)
        app_asset.grant_read(asg)
        config['databases'].grant_connect(asg)

        CfnOutput(self, "AutoScalingGroupName",
                  value=asg.auto_scaling_group_name)
