#!/usr/bin/env python3
import os

try:
    import dotenv
    dotenv.load_dotenv()
except ImportError:
    print("dotenv not found. Skipping loading environment variables.")

import aws_cdk as cdk

from de_duke.main_stack import MainStack


env = cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"),
                      region=os.getenv("CDK_DEFAULT_REGION"))

app = cdk.App()
MainStack(
    app, "DeDukeDevStack",
    stage={
        "name": "dev",
        "version": "1.0.35",
    },
    env=env
)

app.synth()
