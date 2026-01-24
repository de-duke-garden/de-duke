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
)
from constructs import Construct
from pathlib import Path
from typing import TypedDict

from ..shared.main import Shared


class LandingConfig(TypedDict):
    shared: Shared


class Landing(Construct):
    def __init__(self, scope: Construct, id: str, config: LandingConfig) -> None:
        super().__init__(scope, id)

        landing_domain_name = config["shared"].domain_name

        # Create S3 bucket for hosting the landing page
        landing_bucket = s3.Bucket(
            self, "LandingBucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        # Create CloudFront distribution for the S3 bucket
        distribution = cloudfront.Distribution(
            self, "LandingDistribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=cloudfront_origins.S3BucketOrigin.with_origin_access_control(
                    landing_bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED
            ),
            default_root_object="index.html",
            error_responses=[
                cloudfront.ErrorResponse(
                    http_status=403,
                    response_http_status=200,
                    response_page_path="/index.html",
                    ttl=Duration.minutes(30)
                ),
                cloudfront.ErrorResponse(
                    http_status=404,
                    response_http_status=200,
                    response_page_path="/404.html",
                    ttl=Duration.minutes(30)
                )
            ],
            comment="CloudFront distribution for De-Duke landing page",
            domain_names=[landing_domain_name],
            certificate=config["shared"].certificate,
        )

        # Deploy static files to the S3 bucket
        s3_deploy.BucketDeployment(
            self, "DeployUserInterface",
            sources=[
                s3_deploy.Source.asset(
                    # path=str(Path(__file__).parent.joinpath("next-app/out").resolve())
                    path=str(Path(__file__).parent.joinpath(
                        "landing").resolve()),
                    bundling=BundlingOptions(
                        bundling_file_access=BundlingFileAccess.VOLUME_COPY,
                        image=_lambda.Runtime.NODEJS_LATEST.bundling_image,
                        command=[
                            "bash", "-c",
                            "npm install && npm run build && cp -r out/* /asset-output/"
                        ],
                        output_type=BundlingOutput.AUTO_DISCOVER,
                        security_opt="no-new-privileges:true",
                        network="host",
                        # environment={
                        #     "NEXT_PUBLIC_API_URL": config['api'].rest_api.api_url.rstrip("/"),
                        # },
                    ),
                    exclude=["**/node_modules/**", "**/.next/**", "**/out/**"],
                ),
            ],
            destination_bucket=landing_bucket,
            distribution=distribution,
            distribution_paths=["/*"],
        )

        route53.ARecord(
            self, "LandingARecord",
            zone=config["shared"].hosted_zone,
            record_name=landing_domain_name,
            target=route53.RecordTarget.from_alias(
                route53_targets.CloudFrontTarget(distribution)),
        )
        route53.AaaaRecord(
            self, "LandingAaaaRecord",
            zone=config["shared"].hosted_zone,
            record_name=landing_domain_name,
            target=route53.RecordTarget.from_alias(
                route53_targets.CloudFrontTarget(distribution)),
        )

        # Output the CloudFront distribution domain name
        CfnOutput(
            self, "LandingPageURL",
            value="https://" + landing_domain_name,
            description="URL of the De-Duke landing page",
        )
