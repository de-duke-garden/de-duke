from main.settings.dev import *
import boto3
import os

import json

# Retrieve secret key from AWS Secrets Manager
try:
    SECRET_KEY_ARN = os.environ.get("SECRET_KEY_ARN")
    if SECRET_KEY_ARN:
        client = boto3.client(
            "secretsmanager", region_name=os.environ.get("AWS_REGION")
        )
        response = client.get_secret_value(SecretId=SECRET_KEY_ARN)
        secret_string = response.get("SecretString")
        secret_dict = json.loads(secret_string)
        SECRET_KEY = secret_dict.get("secretkey")
except Exception as e:
    print(f"Error retrieving SECRET_KEY: {e}")

INSTALLED_APPS += [
    "storages",
]

MEDIA_STORAGE_BUCKET_NAME = os.environ.get("MEDIA_STORAGE_BUCKET_NAME")
STATIC_STORAGE_BUCKET_NAME = os.environ.get("STATIC_STORAGE_BUCKET_NAME")
STORAGE_REGION = os.environ.get("AWS_REGION")

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "bucket_name": MEDIA_STORAGE_BUCKET_NAME,
            "region_name": STORAGE_REGION,
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "bucket_name": STATIC_STORAGE_BUCKET_NAME,
            "region_name": STORAGE_REGION,
        },
    },
}
MEDIA_URL = f"https://{MEDIA_STORAGE_BUCKET_NAME}.s3.{STORAGE_REGION}://"
STATIC_URL = f"https://{STATIC_STORAGE_BUCKET_NAME}.s3.{STORAGE_REGION}://"

# Retrieve database credentials from AWS Secrets Manager
try:
    DATABASE_CREDENTIALS_ARN = os.environ.get("DATABASE_CREDENTIALS_ARN")
    if DATABASE_CREDENTIALS_ARN:
        client = boto3.client(
            "secretsmanager", region_name=os.environ.get("AWS_REGION")
        )
        response = client.get_secret_value(SecretId=DATABASE_CREDENTIALS_ARN)
        secret_string = response.get("SecretString")
        secret_dict = json.loads(secret_string)
        DATABASES = {
            "default": {
                "ENGINE": "django.contrib.gis.db.backends.postgis",
                "NAME": secret_dict.get("dbname"),
                "USER": secret_dict.get("username"),
                "PASSWORD": secret_dict.get("password"),
                "HOST": secret_dict.get("host"),
                "PORT": secret_dict.get("port"),
            }
        }
except Exception as e:
    print(f"Error retrieving database credentials: {e}")

# Retrieve email credentials from AWS Secrets Manager
try:
    EMAIL_SECRET_ARN = os.environ.get("EMAIL_SECRET_ARN")
    if EMAIL_SECRET_ARN:
        client = boto3.client(
            "secretsmanager", region_name=os.environ.get("AWS_REGION")
        )
        response = client.get_secret_value(SecretId=EMAIL_SECRET_ARN)
        secret_string = response.get("SecretString")
        secret_dict = json.loads(secret_string)
        EMAIL_HOST = secret_dict.get("host")
        EMAIL_PORT = secret_dict.get("port")
        EMAIL_HOST_USER = secret_dict.get("username")
        EMAIL_HOST_PASSWORD = secret_dict.get("password")
        EMAIL_USE_TLS = secret_dict.get("tls") == "true"
        DEFAULT_FROM_EMAIL = secret_dict.get("from", "De-Duke")
except Exception as e:
    print(f"Error retrieving email host password: {e}")


# Retrieve Google Map credentials from AWS Secrets Manager
try:
    GCP_SECRET_ARN = os.environ.get("GCP_SECRET_ARN")
    if GCP_SECRET_ARN:
        client = boto3.client(
            "secretsmanager", region_name=os.environ.get("AWS_REGION")
        )
        response = client.get_secret_value(SecretId=GCP_SECRET_ARN)
        secret_string = response.get("SecretString")
        secret_dict = json.loads(secret_string)
        GOOGLE_MAP_API_KEY = secret_dict.get("mapApiKey")
        GEMINI_API_KEY = secret_dict.get("geminiApiKey")
        if "MAP_WIDGETS" in globals():
            MAP_WIDGETS["GoogleMap"]["apiKey"] = GOOGLE_MAP_API_KEY  # noqa: F405
        PAYSTACK_PUBLIC_KEY = secret_dict.get("paystackPublicKey")
        PAYSTACK_SECRET_KEY = secret_dict.get("paystackSecretKey")
except Exception as e:
    print(f"Error retrieving map API key: {e}")


DEBUG = True

# Allowed hosts
ALLOWED_HOSTS = ["api.de-duke.com", ".compute.amazonaws.com", ".elb.amazonaws.com"]

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://api.de-duke.com",
    "https://api.de-duke.com",
    "http://deduke-apisd-nued5aqqbedo-1798177952.af-south-1.elb.amazonaws.com",
]

# Trusted origins for CSRF and WebSocket origin checks
CSRF_TRUSTED_ORIGINS = [
    "https://api.de-duke.com",
    "http://api.de-duke.com",
    "http://deduke-apisd-nued5aqqbedo-1798177952.af-south-1.elb.amazonaws.com",
]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# Rest Framework settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # "django_cognito_jwt.JSONWebTokenAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# Cognito settings
COGNITO_AWS_REGION = os.getenv("AWS_REGION")
COGNITO_USER_POOL = os.getenv("COGNITO_USER_POOL")
COGNITO_AUDIENCE = os.getenv("COGNITO_AUDIENCE")

# Channels settings
REDIS_ENDPOINT = os.getenv("REDIS_ENDPOINT")
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            # "hosts": [f"rediss://{REDIS_ENDPOINT}:6379"],
            "hosts": [("redis", 6379)],
        },
    },
}
