from aws_cdk import (
    aws_s3 as s3,
    aws_s3_deployment as s3_deploy,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as cloudfront_origins,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
    aws_lambda as _lambda,
    BundlingOptions,
    BundlingFileAccess,
    BundlingOutput,
    RemovalPolicy,
    Duration,
    CfnOutput,
    ILocalBundling
)
from constructs import Construct
from pathlib import Path
from typing import TypedDict

from ..shared.main import Shared

import jsii
import subprocess
import shutil
import os


@jsii.implements(ILocalBundling)
class MyLocalBundler:
    def __init__(self, project_root):
        self.project_root = project_root

    def try_bundle(self, output_dir: str, options) -> bool:
        try:
            # 1. Install dependencies
            subprocess.run(["npm", "install"], cwd=self.project_root, check=True)
            # 2. Run the Next.js build
            subprocess.run(["npm", "run", "build"], cwd=self.project_root, check=True)
            # 3. Copy the 'out' folder contents to the CDK output directory
            dist_dir = os.path.join(self.project_root, "out")
            shutil.copytree(dist_dir, output_dir, dirs_exist_ok=True)
            return True
        except Exception as e:
            print(f"Local bundling failed: {e}")
            return False


class WebsiteConfig(TypedDict):
    shared: Shared


class Website(Construct):
    def __init__(self, scope: Construct, id: str, config: WebsiteConfig) -> None:
        super().__init__(scope, id)

        website_domain_name = config["shared"].domain_name

        # Create S3 bucket for hosting the website page
        # website_bucket = s3.Bucket(
        #     self, "WebsiteBucket",
        #     removal_policy=RemovalPolicy.DESTROY,
        #     auto_delete_objects=True,
        # )

        # project_path = str(Path(__file__).parent.joinpath("website").resolve())

        # # Create CloudFront distribution for the S3 bucket
        # distribution = cloudfront.Distribution(
        #     self, "WebsiteDistribution",
        #     default_behavior=cloudfront.BehaviorOptions(
        #         origin=cloudfront_origins.S3BucketOrigin.with_origin_access_control(
        #             website_bucket),
        #         viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
        #         cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED
        #     ),
        #     default_root_object="index.html",
        #     error_responses=[
        #         cloudfront.ErrorResponse(
        #             http_status=403,
        #             response_http_status=200,
        #             response_page_path="/index.html",
        #             ttl=Duration.minutes(30)
        #         ),
        #         cloudfront.ErrorResponse(
        #             http_status=404,
        #             response_http_status=200,
        #             response_page_path="/404.html",
        #             ttl=Duration.minutes(30)
        #         )
        #     ],
        #     comment="CloudFront distribution for De-Duke website page",
        #     domain_names=[website_domain_name],
        #     certificate=config["shared"].certificate,
        # )

        # # Deploy static files to the S3 bucket
        # s3_deploy.BucketDeployment(
        #     self, "DeployUserInterface",
        #     sources=[
        #         s3_deploy.Source.asset(
        #             path=project_path,
        #             bundling=BundlingOptions(
        #                 image=_lambda.Runtime.NODEJS_LATEST.bundling_image,
        #                 command=[
        #                     "bash", "-c",
        #                     "npm install && npm run build && cp -r out/* /asset-output/"
        #                 ],
        #                 # Pass an instance of your custom class here
        #                 local=MyLocalBundler(project_path)
        #             ),
        #             exclude=["**/node_modules/**", "**/.next/**", "**/out/**"],
        #         ),
        #     ],
        #     destination_bucket=website_bucket,
        #     distribution=distribution,
        #     distribution_paths=["/*"],
        # )

        # route53.ARecord(
        #     self, "WebsiteARecord",
        #     zone=config["shared"].hosted_zone,
        #     record_name=website_domain_name,
        #     target=route53.RecordTarget.from_alias(
        #         route53_targets.CloudFrontTarget(distribution)),
        # )
        # route53.AaaaRecord(
        #     self, "WebsiteAaaaRecord",
        #     zone=config["shared"].hosted_zone,
        #     record_name=website_domain_name,
        #     target=route53.RecordTarget.from_alias(
        #         route53_targets.CloudFrontTarget(distribution)),
        # )
        
        # Handover to Vercel for hosting the Next.js app
        route53.ARecord(
            self, "WebsiteARecord",
            zone=config["shared"].hosted_zone,
            record_name=website_domain_name,
            target=route53.RecordTarget.from_ip_addresses("216.198.79.1"),
        )

        # Output the CloudFront distribution domain name
        CfnOutput(
            self, "WebsitePageURL",
            value="https://" + website_domain_name,
            description="URL of the De-Duke website page",
        )